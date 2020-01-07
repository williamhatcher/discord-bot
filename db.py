from __future__ import annotations

from typing import Union

import discord
from mongoengine import *


class Server(Document):
    """Object to store server/guild settings"""
    guild = IntField(primary_key=True)
    prefix = StringField(required=True, default='$')

    def __str__(self):
        return f"Server <{self.guild}>"

    @classmethod
    async def get_server(cls, guild: Union[int, discord.Guild]) -> Server:
        """Returns server object from guild object or guild id"""
        if type(guild) is discord.Guild:
            guild = guild.id
        return cls.objects.with_id(guild)
