import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

import asyncio

import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Bot
from discord import Object

intents = discord.Intents.all()
intents.message_content = True

active_matches = {}

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

class MatchView(discord.ui.View):
    def __init__(self, challanger, opponent):
        super().__init__(timeout=60)
        self.challanger = challanger
        self.opponent = opponent
    async def on_timeout(self):
        await self.message.edit(contents="Challange expired! No match started.", view=None)
    
    
    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def button_callback(self, interaction: discord.Interaction, button:discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("You were not challanged", ephemeral=True)
            return
        
        active_matches[self.challanger.id]= {
            "challanger": self.challanger.id,
            "opponent": self.opponent.id,
        }
        active_matches[self.opponent.id] = active_matches[self.challanger.id]

        print(active_matches)
        await interaction.response.send_message(f"Match started. {self.challanger.mention} vs {self.opponent.mention}")

@bot.tree.command(name="1v1me", description="Challange another user to a 1v1.", guild=GUILD_ID)
async def oneVsOne(interaction: discord.Interaction, opponent: discord.Member):

    if opponent == interaction.user:
        await interaction.response.send_message('You cannot fight yourself!', ephemeral=True)
        return

    if opponent.bot:
        await interaction.response.send_message("You cannot fight me!", ephemeral=True)
        return
    
    await interaction.response.send_message(f"{interaction.user.mention} has challanged {opponent.mention} to a 1v1!", view=MatchView(interaction.user, opponent))
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello! {message.author}')
    print(f'Message from {message.author}: {message.content}')

    await bot.process_commands(message)

bot.run(token)