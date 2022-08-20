from discord import Forbidden, HTTPException
from discord.ext.tasks import loop
from discord.ext.commands import Bot, Cog
from typing import List
from utility.typed import PurgeList
import utility.request_handler as rh
import logging


class Automated(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.lifetime_inactive_users_removed = 0

    def cog_unload(self):
        pass

    @loop(seconds=86400)
    async def purge(self):
        purge_list: List[PurgeList] = rh.get_purge_list()['list']
        users_removed = 0

        for entry in purge_list:
            self.bot.get_guild(entry['guild_id']).kick(entry['member_id'])
            rh.remove_from_list(entry['member_id'])
            users_remove += 1

        self.lifetime_inactive_users_removed += users_removed

    @purge.before_loop
    async def before_purge(self):
        logging.info('Performing daily purge.')

    @purge.after_loop
    async def after_purge(self):
        logging.info(f'Purge complete. {self.users_removed} removed.')
        pass

    @purge.on_error
    async def purge_error(self, event, *args, **kwargs):
        pass
