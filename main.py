import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
from discord import Object

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=GUILD_ID)
    print(f'We have logged in as {bot.user}!')

@bot.command()
async def embed(ctx):
    help = discord.Embed(
        title="Help",
        description='Here are a list of commands and what they do:',
        color=discord.Color.blue()
    )
    await ctx.send(embed=help)

GUILD_ID = discord.Object(id=1386779222806106193)
    
@bot.tree.command(name="help", description="Brings out the help prompt and explains all the commands", guild=GUILD_ID)
async def slashHelp(interaction: discord.Interaction):
    await interaction.response.send_message("Here are a list of commands and what they do")

@bot.tree.command(name="1v1me", description="Challange another user to a 1v1.", guild=GUILD_ID)
async def oneVsOne(interaction: discord.Interaction):
    await interaction.followup(active_matches = {player1 : player2 })

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello! {message.author}')
    print(f'Message from {message.author}: {message.content}')

    if message.content.startswith('!help'):
        help = discord.Embed(
            title="Help",
        description='Here are a list of commands and what they do:',
        color=discord.Color.blue()
    )
    await message.channel.send(embed=help)
    await bot.process_commands(message)


bot.run(token)