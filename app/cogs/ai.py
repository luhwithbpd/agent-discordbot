from discord.ext import commands
from app.services.ai.chat import ChatService

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_service = ChatService()

    @commands.command()
    async def chat(self, ctx, *, message: str):
        response = await self.chat_service.generate_response(
            user_id=ctx.author.id,
            message=message
        )
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(AI(bot))