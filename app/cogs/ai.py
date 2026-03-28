import random
import time
from discord.ext import commands

from app.services.ai.chat import ChatService

MORI_CHANNEL_ID = 1414575528110854256

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_service = ChatService()

        self._last_auto_reply = 0.0
        self._cooldown_seconds = 45

    def _should_reply_to_mention(self, content: str) -> bool:
        c = content.lower()
        return ("totoro" in c) or ("mori" in c)

    def _can_auto_reply_now(self) -> bool:
        return (time.time() - self._last_auto_reply) >= self._cooldown_seconds

    def _should_auto_reply(self, message) -> bool:
        if message.guild is None:
            return False
        if message.author.bot:
            return False
        if not self._can_auto_reply_now():
            return False
        return random.random() < 0.02

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Só no canal do Mori/Totoro
        if message.channel.id != MORI_CHANNEL_ID:
            await self.bot.process_commands(message)
            return

        content = message.content.strip()

        # 1) Responde quando for citado pelo nome (ou marcado)
        mentioned_bot = self.bot.user in message.mentions if self.bot.user else False
        called = self._should_reply_to_mention(content) or mentioned_bot

        if called:
            async with message.channel.typing():
                reply = await self.chat_service.generate_response(
                    channel_id=message.channel.id,
                    user_id=message.author.id,
                    message=message.content
                )
            await message.reply(reply, mention_author=False)

        # 2) Resposta “por vontade própria” (opcional)
        elif self._should_auto_reply(message):
            self._last_auto_reply = time.time()
            async with message.channel.typing():
                reply = await self.chat_service.generate_response(
                    channel_id=message.channel.id,
                    user_id=message.author.id,
                    message=message.content
                )
            await message.channel.send(reply)

        # Mantém comandos funcionando
        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(AI(bot))