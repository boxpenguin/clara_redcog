import discord, os, math, re
from discord.ext import commands

def convert_size(size_bytes):
   if (size_bytes == 0):
       return '0B'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes/p, 2)
   return '%s %s' % (s, size_name[i])

class Drawpile:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drawpile(self):
        await self.bot.say("Testing")

    async def drawpilesessionsizes(self):
        """Get all sessions running"""
        basedir = "/var/drawpile/sessions"
        with open("/var/drawpile/templates/drawpile.ini", "r") as a:
            file = a.readlines()
            a.close()
        for i, line in enumerate(file):
            if "sessionSizeLimit" in line:
                for l in file[i:i+1]:
                    sizelimit = l
        await self.bot.say("Drawpile Session information")
        await self.bot.say(sizelimit)
        for f in os.listdir(basedir):
            path = os.path.join(basedir, f)
            if os.path.isfile(path):
                if re.search('.dprec', path):
                    size = os.path.getsize(path)
                    await self.bot.say("File:\t{0}" .format(path))
                    await self.bot.say("Size:\t{0}" .format(convert_size(size)))
def setup(bot):
    bot.add_cog(Drawpile(bot))
