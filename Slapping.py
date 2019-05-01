import discord
from settings import *
from checks import *


class Slapping(commands.Cog):
	"""a suite of commands meant to help moderators handle the server"""
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	@commands.has_any_role(*GESTION_ROLES)
	async def slap(self, ctx, member:discord.Member):
		'''Meant to give a warning to misbehavioring members. Cumulated slaps will result in warnings, role removal and eventually kick. Beware the slaps are loged throughout history and are cross-server'''
		to_write = ""
		slap_count=0

		#reads the file and prepares logging of slaps
		with open(SLAPPED_LOG_FILE, "r") as file:
			content = file.readlines()
			for line in content:
				if line.startswith(str(member.id)):
					slap_count = int(line.split(";")[1])+1
					to_write+= "{};{}\n".format(member.id, slap_count)

				else:
					to_write += line

		#creates a log for the member if he's never been slapped
		if slap_count==0:
			slap_count = 1
			to_write += "{};{}\n".format(member.id, slap_count)


		await ctx.send("{} you've been slapped by {} because of your behavior! This is the {} time. Be careful, if you get slapped too much there *will* be consequences !".format(member.mention, ctx.message.author.mention, slap_count))

		#writes out updated data to the file
		with open(SLAPPED_LOG_FILE, "w") as file:
			file.write(to_write)			

	@commands.command()
	@commands.has_any_role(*GESTION_ROLES)
	async def pardon(self, ctx, member:discord.Member):
		'''Pardonning a member resets his slaps count.'''
		to_write = ""

		#reads the file and prepares logging of slaps
		with open(SLAPPED_LOG_FILE, "r") as file:
			content = file.readlines()
			for line in content:
				if not line.startswith(str(member.id)):
					to_write+=line

		#writting updated file
		with open(SLAPPED_LOG_FILE, "w") as file:
			file.write(to_write)

		await ctx.send("{} you've been pardonned by {}.".format(member.mention, ctx.author.mention))

def setup(bot):
	bot.add_cog(Slapping(bot))