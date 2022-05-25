# Libraries i may or may not use
import contextlib
import csv
import io
import json
import math
import os
import platform
import random
import textwrap
import traceback
from pathlib import Path
import asyncgTTS

import aiohttp
import discord
from discord.ext import commands
from num2words import num2words
from PIL import Image, ImageColor
from time import sleep

from utils.util import *

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

# Defines some stuff idk
secrets_file = json.load(open(cwd + "/secrets.json"))
command_prefix = "b:"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.config_token = secrets_file["token"]
us_words = []


# Are yah ready kids?
@bot.event
async def on_ready():
    print(
        f"Logged in as: {bot.user.name} : {bot.user.id}\n-----\nCurrent prefix: '{command_prefix}'"
    )

    with open("us_words.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            us_words.append(row[0])

    await bot.change_presence(activity=discord.Game(name="Undergoing Renovations"))


# Errors are not pog
@bot.event
async def on_command_error(ctx, error):
    ignored_errors = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored_errors):
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Stop it. Get some perms.", mention_author=False)

    return error


# Runs something whenever a message is sent
@bot.event
async def on_message(message):
    # You are a bold one!
    if "hello there" in message.content.lower():
        await message.channel.send("General Kenobi!")

    # Pingus pongus
    if (
        f"<@!{bot.user.id}>" in message.content
        or f"<@{bot.user.id}>" in message.content
    ):
        await message.reply(f"pingus pongus your mother is {random.choice(us_words)}")

    # Says goodnight to henry
    henry = bot.get_user(289180942583463938)
    goodnight_message = "gn guys!"

    if message.author == henry and message.content.lower() == goodnight_message:
        sleep(1)
        await message.channel.send("gn Henry!")

    await bot.process_commands(message)


# Command center
@bot.command(name="test")
async def test(ctx):
    """
    A simple test command
    """
    test_grades = ["an A", "a B", "a C", "a D", "an F"]

    await ctx.send(f"{ctx.author.mention} got {random.choice(test_grades)}")


@bot.command(name="info")
async def info(ctx):
    """
    Gives info about Botnobi
    """
    python_version = platform.python_version()
    dpy_version = discord.__version__
    server_count = len(bot.guilds)
    user_count = len(set(bot.get_all_members()))

    embed = discord.Embed(
        title=f":information_source: Botnobi",
        description="\uFEFF",
        color=ctx.guild.me.color,
        timestamp=ctx.message.created_at,
    )

    embed.add_field(
        name="<:github:842921746277203978>",
        value="[Repo](https://github.com/MysticalApple/Botnobi)",
    )
    embed.add_field(name="Python Version", value=python_version)
    embed.add_field(name="Discord.py Version", value=dpy_version)
    embed.add_field(name="Servers", value=server_count)
    embed.add_field(name="Users", value=user_count)
    embed.add_field(name="Bot Creator", value="<@!595719716560175149>")

    embed.set_footer(text=f"As of")
    embed.set_author(name=ctx.guild.me.display_name,
                     icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="disconnect")
@commands.is_owner()
async def disconnect(ctx):
    """
    Takes Botnobi offline
    """
    await ctx.send("Disconnecting...")
    await bot.logout()


@bot.command(name="eval")
@commands.is_owner()
async def eval(ctx, *, code):
    """
    Runs python code
    """
    code = clean_code(code)

    local_variables = {"discord": discord,
                       "commands": commands, "bot": bot, "ctx": ctx}

    stdout = io.StringIO()

    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}", local_variables)

            obj = await local_variables["func"]()
            result = f"py\n‌{stdout.getvalue()}\n"

    except Exception as e:
        result = "".join(traceback.format_exception(e, e, e.__traceback__))

    await ctx.send(f"```{result}```")


@bot.command(name="sheep")
async def sheep(ctx):
    """
    Sends a sheep
    """
    await ctx.send(
        "<a:seansheep:718186115294691482>```\n         ,ww\n   wWWWWWWW_)\n   `WWWWWW'\n    II  II```"
    )


@bot.command(name="emotize")
async def emotize(ctx, *, message):
    """
    Converts text into discord emojis
    """
    output = ""

    for l in message:
        if l == " ":
            output += l
        elif l == "\n":
            output += l
        elif l.isdigit():
            numword = num2words(l)
            output += f":{numword}:"
        elif l.isalpha():
            l = l.lower()
            output += f":regional_indicator_{l}:"

    await ctx.send(output)


@bot.command(name="inspire")
async def inspire(ctx):
    """
    Uses InspiroBot to generate an inspirational quote"
    """
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://inspirobot.me/api?generate=true") as resp:
                r = await resp.text()
    await ctx.send(r)


@bot.command(name="color")
async def color(ctx, *, hex):
    """
    Sends a square of a solid color
    """
    try:
        color = ImageColor.getrgb(hex)

    except:
        await ctx.reply(
            "Valid color codes can be found here: https://pillow.readthedocs.io/en/stable/reference/ImageColor.html",
            mention_author=False,
        )

    img = Image.new("RGBA", (480, 480), color=color)
    img.save("color.png")
    await ctx.send(file=discord.File("color.png"))


@bot.command(name="stackify")
async def stackify(ctx, count: int):
    """
    Converts an item count into Minecraft stacks
    """
    stacks = math.floor(count / 64)
    items = count % 64
    await ctx.send(f"{count} items can fit into {stacks} stacks and {items} items.")


@bot.command(name="toggle")
# Checks that user is Newlandite
@commands.has_role(710933072664723486)
async def toggle(ctx, feature):
    """
    Toggles any boolean value in config.json
    """

    # Loads in config.json as a dict
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Toggles the value if it is a valid bool
    try:
        if type(config[feature]) == bool:
            config[feature] = not config[feature]

            with open("config.json", "w") as config_file:
                json.dump(config, config_file)

            await ctx.send(f"{feature} has been toggled to {config[feature]}")

        else:
            raise

    # Returns an error if the value is not a bool or if it does not exist
    except:
        await ctx.send(f"{feature} is not a valid toggleable value")


# Runs code whenever someone leaves the server
@bot.event
async def on_member_remove(member):
    # Checks that the leaver left the correct server
    if member.guild.id == 710932856251351111 and check_toggle("leave_log"):
        # Sets the channel to the one specificied in config.json
        channel = bot.get_channel(get_alerts_channel_id())
        join_date = member.joined_at

        # Creates an embed with info about who left and when
        # Format shamelessly stolen (and slightly changed) from https://github.com/ky28059
        embed = discord.Embed(
            description=f"{member.mention} {member}",
            color=member.color,
        )

        embed.set_author(name="Member left the server",
                         icon_url=member.avatar_url)
        embed.set_footer(
            text=f"Joined: {join_date.month}/{join_date.day}/{join_date.year}"
        )

        # Sends it
        await channel.send(embed=embed)


@bot.command(name="delete")
@commands.is_owner()
async def delete(ctx, channel_id: int, message_id: int):
    """
    Deletes a specified message in a specified channel
    """
    channel = bot.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    await message.delete()


@bot.command(name="join")
async def join(ctx):
    """
    Joins the voice channel that the user is in
    """
    if not ctx.message.author.voice:
        await ctx.reply("You should join a voice channel first", mention_author=False)

    else:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.guild.change_voice_state(
            channel=channel, self_mute=False, self_deaf=True
        )
        await ctx.message.add_reaction("⏫")


@bot.command(name="leave")
async def leave(ctx):
    """
    Leaves the voice channel that it is currently in
    """
    voice_client = ctx.guild.voice_client

    if voice_client:
        await voice_client.disconnect()
        await ctx.message.add_reaction("⏬")

    else:
        await ctx.reply("I'm not in a voice channel right now", mention_author=False)


@bot.command(name="say")
async def say(ctx, *, message):
    """
    Uses google text to speech to say something in a voice channel
    """
    voice_client = ctx.guild.voice_client

    if voice_client:
        async with aiohttp.ClientSession() as session:
            gtts = await asyncgTTS.setup(premium=False, session=session)
            tts = await gtts.get(text=message)

            with open("message.mp3", "wb") as f:
                f.write(tts)

            voice_client.play(
                discord.FFmpegPCMAudio(
                    executable="ffmpeg.exe", source="message.mp3")
            )
            await ctx.message.add_reaction("☑️")

    else:
        await ctx.reply("I'm not in a voice channel right now", mention_author=False)


@bot.command(name="perlin")
async def perlin(ctx):
    """
    Generates random perlin noise
    """
    seed = random.randint(-128, 128)
    os.system(f".\perlin.exe {seed}")

    perlin = Image.open("perlin.ppm")
    perlin.save("perlin.png")

    await ctx.send(file=discord.File("perlin.png"))


# Run the damn thing already
bot.run(bot.config_token)
