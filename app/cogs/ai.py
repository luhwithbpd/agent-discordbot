import random
import time
from discord.ext import commands

from app.services.ai.chat import ChatService

MORI_CHANNEL_ID = 1478396294593777707

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.chat_service = ChatService()

        # anti-spam básico
        self._last_auto_reply = 0.0
        self._cooldown_seconds = 45  # tempo mínimo entre respostas "por vontade"

    def _should_reply_to_mention(self, content: str) -> bool:
        c = content.lower()
        return "totoro" in c  # simples: contém a palavra mori

    def _can_auto_reply_now(self) -> bool:
        return (time.time() - self._last_auto_reply) >= self._cooldown_seconds

    def _should_auto_reply(self, message) -> bool:
        # regras para evitar ficar chato
        if message.guild is None:  # ignora DM por enquanto (opcional)
            return False
        if message.author.bot:
            return False
        if not self._can_auto_reply_now():
            return False

        # chance baixa de “vontade própria”
        # ajuste entre 0.01 e 0.05 (1% a 5%)
        return random.random() < 0.02

@commands.Cog.listener()
async def on_message(self, message):
    print(f"[on_message] got message in #{getattr(message.channel, 'id', None)} "
          f"from {message.author} ({message.author.id}): {message.content!r}")

    if message.author.bot:
        return

    print(f"[on_message] channel.id={message.channel.id} expected={MORI_CHANNEL_ID}")

    content = message.content.strip()

    called = self._should_reply_to_name(content) or (self.bot.user in message.mentions)
    if not called:
        return

    try:
        async with message.channel.typing():
            reply = await self.chat_service.generate_response(
                user_id=message.author.id,
                message=content
            )
        await message.reply(reply, mention_author=False)
    except Exception as e:
        print(f"[AI Cog] Error: {repr(e)}")
        await message.channel.send("Hm... tropecei numa raiz. Tenta de novo?")

async def setup(bot):
    await bot.add_cog(AI(bot))