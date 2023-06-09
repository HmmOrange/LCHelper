import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import Interaction, app_commands
from discord.app_commands import AppCommandError
import os
import asyncio
from dotenv import load_dotenv
from utils.asset import Assets
from pymongo import MongoClient
import traceback
load_dotenv()

intent = discord.Intents.all()
client = commands.Bot(command_prefix = os.getenv('BOT_PREFIX'), case_insensitive = True, intents = intent)
activity = discord.Activity(name = 'Lowie', type = discord.ActivityType.playing)
token = os.getenv('BOT_TOKEN')
tree = client.tree
DBClient = MongoClient(os.getenv('MONGODB_LOGIN_CRED'))
client.DBClient = DBClient

async def main():
    async with client:
        # Loading extensions
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await client.load_extension(f'cogs.{filename[:-3]}')
                    print(f"{filename}: ok!")
                except Exception as e:
                    print(f"{filename}: not ok!! - {e}")
        await client.load_extension("jishaku")

        # Loading Discord client
        await client.start(token)

@tree.error
async def on_app_command_error(interaction: Interaction, error: AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.followup.send("You don't have the permission to execute this command")
    elif isinstance(error, app_commands.CommandNotFound):
        return
    else:
        await interaction.followup.send(f"```py\n{traceback.format_exc()}```")
    print(error)

asyncio.run(main())