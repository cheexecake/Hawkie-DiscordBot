import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.command
async def embed(ctx):
    help = discord.Embed(
        title="Help",
        description='Here are a list of commands and what they do:',
        color=discord.Color.blue()
    )
    await ctx.send(embed=help)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}!')
    


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