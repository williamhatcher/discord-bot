import os
from sys import exit
import discord
from discord.ext import commands
from mongoengine import connect

from db import Server
from utils import log, DB, DEFAULT_PREFIX


async def prefix_callable(_bot: commands.Bot, message) -> [str]:
    """Returns list of prefixes for commands"""
    base = []
    if message.guild is None:
        base.append(DEFAULT_PREFIX)
    else:
        base.append(Server.objects.scalar('prefix').with_id(message.guild.id))
    return commands.when_mentioned_or(*base)(_bot, message)


bot = commands.Bot(command_prefix=prefix_callable)


@bot.event
async def on_ready():
    log.debug("Logged in as {0} {0.id}".format(bot.user))
    for g in bot.guilds:  # Add any added guilds to DB while bot was offline
        await on_guild_join(g)


@bot.event
async def on_guild_join(guild: discord.Guild):
    """Adds guild to database if not already in it"""
    if not await Server.get_server(guild):
        log.info(f"Adding {guild.name} to DB")
        s = Server()
        s.guild = guild.id
        s.save()


if __name__ == '__main__':
    connect(DB)

    try:
        bot.run(os.getenv("TOKEN"))
    except discord.errors.LoginFailure:
        log.fatal("Unable to log into bot. Please check TOKEN environment variable.")
        exit(1)
