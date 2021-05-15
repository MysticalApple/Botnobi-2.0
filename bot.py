# Libraries i may or may not use
import discord
from discord.ext import commands
import logging
from pathlib import Path
import json
import random
import platform

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Defines some stuff idk
secrets_file = json.load(open(cwd+'/secrets.json'))
command_prefix = "b:"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.config_token = secrets_file['token']
logging.basicConfig(level=logging.INFO)

# Are yah ready kids?
@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nCurrent prefix: '{command_prefix}'")

    await bot.change_presence(activity=discord.Game(name='Undergoing Renovations'))

#errors are not pog
@bot.event
async def on_command_error(ctx, error):
    ignored_errors = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored_errors):
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Stop it. Get some perms.", mention_author=False)
   
    raise error

# Command center
@bot.command(name='test')
async def test(ctx):
    """
    A simple test command
    """
    test_grades = ["an A","a B","a C","a D","an F"]

    await ctx.send(f"{ctx.author.mention} got {random.choice(test_grades)}")

@bot.command(name='info')
async def info(ctx):
    """
    Gives info about Botnobi
    """
    python_version = platform.python_version()
    dpy_version = discord.__version__
    server_count = len(bot.guilds)
    user_count = len(set(bot.get_all_members()))

    embed = discord.Embed(title=f':information_source: Botnobi', description='\uFEFF', color=ctx.guild.me.color, timestamp=ctx.message.created_at)

    embed.add_field(name='<:github:842921746277203978>', value="[Repo](https://github.com/MysticalApple/Botnobi-2.0)")
    embed.add_field(name='Python Version', value=python_version)
    embed.add_field(name='Discord.py Version', value=dpy_version)
    embed.add_field(name='Servers', value=server_count)
    embed.add_field(name='Users', value=user_count)
    embed.add_field(name='Bot Creator', value="<@!595719716560175149>")

    embed.set_footer(text=f"As of")
    embed.set_author(name=ctx.guild.me.display_name, icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

@bot.command(name='disconnect')
@commands.is_owner()
async def disconnect(ctx):
    """
    Takes Botnobi offline
    """
    await ctx.send('Disconnecting...')
    await bot.logout()


# Run the damn thing already
bot.run(bot.config_token)