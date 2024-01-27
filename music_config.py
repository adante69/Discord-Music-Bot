import discord
import json
from discord.ext import commands
from googleapiclient.discovery import build
import yt_dlp as youtube_dl
with open("config.json", "r") as f:
    config = json.load(f)
    key_api = config["API_key"]
youtube = build('youtube', 'v3', developerKey=key_api)
class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.vc = None

    def find_vid(self,name):
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

    def search_yt(self, item):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info('ytsearch:%s' % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['url'], 'title': info['title']}


    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(executable='path/to/ffmpeg', source=m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):

        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc is None:
                    await ctx.send("Э бля не могу в канал зайти")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False

    @commands.command(name='play', help='играет выбранную песню с ютуба')
    async def play(self,ctx,*args):
        query = ' '.join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("сначала в канал зайди лошок бля")
        elif self.is_paused:
            self.vc.resume()
        else:
            if 'https://www.youtube.com/' in query:
                song = self.search_yt(query)
            else:
                song = self.search_yt(self.find_vid(query))

            if song is True:
                await ctx.send('не могу загрузить песню')
            else:
                await ctx.send('Песня добавлена в плейлист')
                print(song)
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name='pause',help='pauses song')
    async def pause(self,ctx,*args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

    @commands.command(name='resume', help='resumes song')
    async def resume(self,ctx,*args):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()


    @commands.command(name='skip', help='skips song')
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name='queue',help="all queued songs")
    async def queue(self,ctx):
        retval = ''

        for i in range (0,len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'
        if retval != '':
            await ctx.send(retval)
        else:
            await ctx.send("в плейлисте нет музыки")

    @commands.command(name='clear',help="clears")
    async def clear(self,ctx,*args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("плейлист пуст")

    @commands.command(name='leave',help="leaves")
    async def leave(self,ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
