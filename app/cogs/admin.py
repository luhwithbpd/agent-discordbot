from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        try:
            await self.bot.reload_extension(f"app.cogs.{extension}")
            await ctx.send(f"Cog `{extension}` recarregado com sucesso.")
        except Exception as e:
            await ctx.send(f"Erro ao recarregar: {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))