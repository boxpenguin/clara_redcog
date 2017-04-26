#/usr/bin/python3.5
import discord, os, math, re, requests, json, time
from discord.ext import commands

# Pre bot defs
def convert_size(size_bytes):
    """ Convert bytes to other IS values
    From: http://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    @James Sapam """
    if (size_bytes == 0):
       return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes/p, 2)
    return '%s %s' % (s, size_name[i])
def getdata(type):
    """ Access drawpile web admin JSON """
    url = ("http://localhost:8081/{0}/" .format(type))
    output = requests.get(url).text
    jsonoutout = json.loads(output)
    return output
def getip(ip):
    """ Using the awesome ipinfo to get ip data and related information """
    url = ("https://ipinfo.io/{0}/" .format(ip))
    output = requests.get(url).text
    return output
def gettime(lat,lng):
    """ Using geonames to grab time and date from the lat/lng in conjunction of getip """
    url = ("http://api.geonames.org/timezoneJSON?lat={0}&lng={1}&username=demo" .format(lat, lng))
    output = requests.get(url).text
    return output

class Drawpile:
    """
    Version 1.0 (20170426)
    @Rakunko, Jordan Uehara
    Red-bot custom cog
    """
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def drawpileadmin(self, type):
        """ direct access to the admin JSON """
        await self.bot.say("Getting information")
        await self.bot.say(getdata(type))
    @commands.command()
    async def drawpile(self):
        """ Look up running sessions and logged in users """
        usercount = 0
        await self.bot.say("Getting Drawpile Session info :desktop:")
        session_json = getdata("sessions")
        session_data = json.loads(session_json)
        for a in range(len(session_data)):
            await self.bot.say("Session #:\t\t {0}" .format(a+1))
            await self.bot.say("Title:\t\t\t\t  {0}" .format(session_data[a]['title']))
            await self.bot.say("Alias:\t\t\t\t {0}" .format(session_data[a]['alias']))
            await self.bot.say("Users:\t\t\t\t{0}" .format(session_data[a]['userCount']))
            usercount += session_data[a]['userCount']
            await self.bot.say("ID:\t\t\t\t\t  {0}" .format(session_data[a]['id']))
            await self.bot.say("Session Size:\t{0} / 15 MB" .format(convert_size(session_data[a]['size'])))
            await self.bot.say("_")
        user_json = getdata("users")
        users_data = json.loads(user_json)
        await self.bot.say("Getting Drawpile User info ~~~ {0} artist(s) online :pencil2:" .format(usercount))
        if usercount > 0:
            for b in range(len(users_data)):
                await self.bot.say("User:\t\t\t\t {0}" .format(users_data[b]['name']))
                userip = users_data[b]['ip']
                ip_json = getip(userip)
                ip_data = json.loads(ip_json)
                if ip_data['ip'] == "192.168.1.1": # checks if user is on local network to the server
                    await self.bot.say("IP:\t\t\t\t\t localhost")
                    await self.bot.say("Time:\t\t\t\t\t {0}" .format(time.strftime("%Y-%m-%d %H:%M"))) #2017-04-25 23:22
                else: # catch all other non local users
                    await self.bot.say("IP:\t\t\t\t\t {0}" .format(ip_data['ip']))
                    user_loc = ip_data['loc']
                    user_geo = user_loc.split(",")
                    user_time = gettime(user_geo[0],user_geo[1])
                    user_time_data = json.loads(user_time)
                    await self.bot.say("Local Time:\t{0}" .format(user_time_data['time']))
                usersession = users_data[b]['session'] # report user's session from the sessionid and return title TODO maybe make this a function?
                for c in range(len(session_data)):
                    if usersession == session_data[c]['id']:
                        await self.bot.say("Session:\t\t {0}" .format(session_data[c]['title']))
                        await self.bot.say("_")

    async def drawpilesessionsizes(self):
        """Get all sessions running sizes directly from server - depricated since version 1.0"""
        basedir = "/var/drawpile/sessions"
        with open("/var/drawpile/templates/drawpile.ini", "r") as a:
            file = a.readlines()
            a.close()
        for i, line in enumerate(file):
            if "sessionSizeLimit" in line:
                for l in file[i:i+1]:
                    sizelimit = l
        await self.bot.say("Drawpile Session information (depricated)")
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
