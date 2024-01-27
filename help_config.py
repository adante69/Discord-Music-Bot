
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_mes = '''
        Список комманд Скуф бота:
        >play - проигрывает песню в голосовом канале, также выходит из паузы
        >queue - показывает полный плейлист 
        >skip - пропускает текущую песню
        >clear - останавливает музыку и очищает очередь
        >leave - бот выходит из голосового канала
        >pause - ставит текущую песню на паузу
        >resume - продолжает проигрывание песни
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

