import os
import discord
import requests
from datetime import datetime, timedelta
from src import Session
from src.models import *


BASE_URL = 'http://api.vfan.vlive.tv/vproxy/channelplus'
APP_ID = os.environ['VLIVE_APP_ID']


def vlive_handler(sess, group: str):
    obj = sess.query(Group).filter(Group.name == group).first()
    payload = {
        'app_id': APP_ID,
        'channelSeq': obj.vlive_channel_seq,
        'maxNumOfRows': 10,
        'pageNo': 1,
    }
    res = requests.get(f"{BASE_URL}/getChannelVideoList", params=payload).json()
    channel_info = res['result']['channelInfo']
    video_list = res['result']['videoList']
    latest_vid = video_list[0]
    if latest_vid['videoSeq'] != obj.vlive_last_seq:
        obj.vlive_last_seq = latest_vid['videoSeq']
        sess.commit()
        release_timestamp = datetime.strptime(latest_vid['onAirStartAt'], '%Y-%m-%d %H:%M:%S')
        release_timestamp -= timedelta(hours=1)
        now_timestamp = datetime.now()
        delay_timestamp = now_timestamp - release_timestamp
        if delay_timestamp.seconds < 60:
            delay_text = f"{delay_timestamp.seconds}s"
        else:
            delay_text =  f"{delay_timestamp.seconds//60}min"
        embed = discord.Embed(
            title=latest_vid['title'],
            url=f"https://www.vlive.tv/video/{latest_vid['videoSeq']}",
            description = f"{obj.name.upper()} started streaming ({delay_text} ago)",
            timestamp=release_timestamp,
        )
        embed.set_author(
            name=f"{latest_vid['representChannelName']} - LIVE",
            icon_url=channel_info['channelProfileImage'],
            url=f"https://channels.vlive.tv/{channel_info['channelCode']}/home",
        )
        embed.set_image(url=f"{latest_vid['thumbnail']}?type=f886_499")
        embed.set_footer(
            text='VLIVE',
            icon_url='https://i.imgur.com/gHo7BTO.png',
        )
        return embed
