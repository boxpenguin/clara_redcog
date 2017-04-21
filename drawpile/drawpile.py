import discord, os
from discord.ext import commands

class Drawpile:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drawpilesessions(self):
    """Get all sessions running"""
    await self.bot.say("Drawpile Session information")
    sessions = os.listdir("/var/drawpile/sessions")
    await self.bot.say(sessions)

def setup(bot):
    bot.add_cog(Mycog(bot))
