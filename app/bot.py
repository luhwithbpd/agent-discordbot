import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load_extensions():
    for file in COGS_DIR.rglob("*.py"):
        if file.name != "__init__.py":
            module = ".".join(file.with_suffix("").relative_to(BASE_DIR).parts)
            await bot.load_extension(module)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

import asyncio
asyncio.run(main())