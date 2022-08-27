import aiohttp
import discord
from bot.api.internal import Api
from datetime import datetime, timedelta


async def vlive_handler(group: dict):
    obj = group
    if obj["vlive_channel_seq"] is None:
        return
    payload = {
        "app_id": "8c6cc7b45d2568fb668be6e05b6e5a3b",
        "channelSeq": obj["vlive_channel_seq"],
        "maxNumOfRows": 10,
        "pageNo": 1,
    }
    base_url = "http://api.vfan.vlive.tv/vproxy/channelplus"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/getChannelVideoList", params=payload) as res:
            if res.status >= 400:
                print("VLIVE retrieve failed.")
                return None
            res = await res.json()
            channel_info = res["result"]["channelInfo"]
            video_list = res["result"]["videoList"]
            latest_vid = video_list[0]
            if latest_vid["videoSeq"] != obj["vlive_last_seq"]:
                print(f'New VLIVE detected for {obj["name"]}')
                obj, _ = await Api.group(group["id"], "patch", dict(vlive_last_seq=latest_vid["videoSeq"]))
                release_timestamp = datetime.strptime(latest_vid["onAirStartAt"], "%Y-%m-%d %H:%M:%S")
                release_timestamp -= timedelta(hours=9)
                live = latest_vid["videoType"] == "LIVE"
                title = "**[LIVE]** " if live else "**[VOD]** "
                title += latest_vid["title"]
                name = latest_vid["representChannelName"]
                name += " Now Live!" if live else " New Upload"
                if live:
                    description = f"@here {obj['name']} started streaming!"
                else:
                    description = f"@here {obj['name']} uploaded a new video!"
                embed = discord.Embed(
                    title=title,
                    url=f"https://www.vlive.tv/video/{latest_vid['videoSeq']}",
                    description=description,
                    timestamp=release_timestamp,
                )
                embed.set_author(
                    name=name,
                    icon_url=channel_info["channelProfileImage"],
                    url=f"https://channels.vlive.tv/{channel_info['channelCode']}/home",
                )
                embed.set_image(url=f"{latest_vid['thumbnail']}?type=f886_499")
                embed.set_footer(
                    text="VLIVE",
                    icon_url="https://i.imgur.com/gHo7BTO.png",
                )
                return embed
