import logging
from settings import *
import discord
from utilities import *

#########################################
#                                       #
#                                       #
#           Setting up logging          #
#                                       #
#                                       #
#########################################
local_logger = logging.getLogger(__name__)
local_logger.setLevel(LOGGING_LEVEL)
local_logger.addHandler(LOGGING_HANDLER)
local_logger.info("Innitalized {} logger".format(__name__))


#########################################
#                                       #
#                                       #
#           Making commands             #
#                                       #
#                                       #
#########################################



class Role(commands.Cog):
    """role management utility. Requires a Gestion role"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @has_auth("admin")
    async def role(self, ctx):
        '''role management utility. Requires a Gestion role'''
        if ctx.invoked_subcommand is None:
            local_logger.warning("User didn't provide any subcommand")
            await ctx.send("NotEnoughArguments:\tYou must provide a subcommand")

    @role.command()
    async def add(self, ctx, member: discord.Member, *roles:discord.Role):
        '''Gives <member> listed <roles> roles'''
        if len(roles)==0:
            local_logger.warning("User didn't provide a role")
            await ctx.send("NotEnoughArguments:\tYou must provide at least one `role`")

        else:
            try:
                await member.add_roles(*roles)
                roles_str = ""
                for role in roles:
                    roles_str+= f" {role}"

                await ctx.send(f"You gave {member.name} {roles_str} role(s).")
            except Exception as e:
                local_logger.exception("Couldn't add {} to {}".format(roles, member))
                await ctx.send("An unexpected error occured !\nTraceback:```python\n{}```".format(e))

    @role.command()
    async def rm(self, ctx, member:discord.Member, *roles:discord.Role):
        '''Removes <member>'s <roles> roles'''
        if len(roles)==0:
            local_logger.warning("User didn't provide a role")
            await ctx.send("NotEnoughArguments:\tYou must provide at least one `role`")

        else:
            try:
                await member.remove_roles(*roles)
            except Exception as e:
                local_logger.exception("Couldn't remove roles ")
                await ctx.send("An unexpected error occured !\nTraceback:```python\n{}```".format(e))


def setup(bot):
    bot.add_cog(Role(bot))