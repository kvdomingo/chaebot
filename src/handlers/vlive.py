import aiohttp
import os
import discord
from datetime import datetime, timedelta
from src.models import *
from sqlalchemy.orm.session import Session
from typing import Optional


BASE_URL = 'http://api.vfan.vlive.tv/vproxy/channelplus'
APP_ID = os.environ['VLIVE_APP_ID']


async def loop_handler(sess: Session, group: str) -> Optional[discord.Embed]:
    obj = sess.query(Group).filter(Group.name == group).first()
    if obj.vlive_channel_seq is None:
        return
    payload = {
        'app_id': APP_ID,
        'channelSeq': obj.vlive_channel_seq,
        'maxNumOfRows': 10,
        'pageNo': 1,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/getChannelVideoList", params=payload) as res:
            if res.status//100 != 2:
                print("VLIVE retrieve failed.")
                return
            res = await res.json()
            channel_info = res['result']['channelInfo']
            video_list = res['result']['videoList']
            latest_vid = video_list[0]
            if latest_vid['videoSeq'] != obj.vlive_last_seq:
                print("New VLIVE detected")
                obj.vlive_last_seq = latest_vid['videoSeq']
                sess.commit()
                release_timestamp = datetime.strptime(latest_vid['onAirStartAt'], '%Y-%m-%d %H:%M:%S')
                release_timestamp -= timedelta(hours=1)
                # now_timestamp = datetime.now()
                release_timestamp -= timedelta(hours=8)
                # delay_timestamp = now_timestamp - release_timestamp
                live = latest_vid['videoType'] == 'LIVE'
                title = "**[LIVE]** " if live else "**[VOD]** "
                title += latest_vid['title']
                name = latest_vid['representChannelName']
                name += " Now Live!" if live else " New Upload"
                if live:
                    description = f"@everyone {obj.name.upper()} started streaming"
                else:
                    description = f"@everyone {obj.name.upper()} uploaded a new video"
                embed = discord.Embed(
                    title=title,
                    url=f"https://www.vlive.tv/video/{latest_vid['videoSeq']}",
                    description=description,
                    timestamp=release_timestamp,
                )
                embed.set_author(
                    name=name,
                    icon_url=channel_info['channelProfileImage'],
                    url=f"https://channels.vlive.tv/{channel_info['channelCode']}/home",
                )
                embed.set_image(url=f"{latest_vid['thumbnail']}?type=f886_499")
                embed.set_footer(
                    text='VLIVE',
                    icon_url='https://i.imgur.com/gHo7BTO.png',
                )
                return embed
