import discord
from discord.ext import commands
import json
import asyncio
import yt_dlp as youtube_dl
from googleapiclient.discovery import build
from help_config import HelpCog
from music_config import MusicCog

with open("config.json", "r") as f:
    config = json.load(f)
    token = config["token"]
    key_api = config["API_key"]

youtube = build('youtube', 'v3', developerKey=key_api)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)


bot.remove_command('help')

async def main():
    async with bot:
        await bot.add_cog(HelpCog(bot))
        await bot.add_cog(MusicCog(bot))
        await bot.start(token)


def find_vid(name):

        request = youtube.search().list(
            part='snippet',
            q=name,
            type='video',
            maxResults=1
        )
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            video_id = response['items'][0]['id']['videoId']
            url = f'https://www.youtube.com/watch?v={video_id}'
            return url
        else:
            return None


def search_yt(item):

    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info('ytsearch:%s' % item, download=False)['entries'][0]
    return info['title']


def file_changes():
    with open("config.json", "r") as f:
        con = json.load(f)

    return 'lol'


asyncio.run(main())
