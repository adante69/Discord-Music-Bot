
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_mes = '''
        List of commands:
        >play - plays music in voice channel and add some music to a queue
        >queue - shows you full playlist
        >skip - skip songs
        >clear - stop music and clear list of music from queue
        >leave - bot leaves the voice channel
        >pause - pause song
        >resume - resume song
        '''

        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)

        await self.send_to_all(self.help_mes)

    async def send_to_all(self,msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

