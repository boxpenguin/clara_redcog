import discord, requests
from discord.ext import commands
def getip(ip):
    url = ("https://ipinfo.io/{0}/" .format(ip))
    output = requests.get(url).text # displays content
    return output

class Ipinfo:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ipinfo(self, ip):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say(getip(ip))

def setup(bot):
    bot.add_cog(Ipinfo(bot))
