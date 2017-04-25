#/usr/bin/python3.5
import discord, os, collections, math, re, requests, json
from discord.ext import commands
from requests.auth import HTTPBasicAuth

# Pre bot command funcs
def convert_size(size_bytes):
   if (size_bytes == 0):
       return '0B'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes/p, 2)
   return '%s %s' % (s, size_name[i])
def getdata(type):
    url = ("http://localhost:8081/{0}/" .format(type))
    output = requests.get(url, auth=HTTPBasicAuth('clara', 'amdk6-2')).text # displays content
    jsonoutout = json.loads(output)
    return output
def getip(ip):
    url = ("https://ipinfo.io/{0}/" .format(ip))
    output = requests.get(url).text # displays content
    return output

class Drawpile:
    def __init__(self, bot):
        self.bot = bot
    """
    What does this doo
    Using drawpiles admin webserver I can grab information however this is poorly documented
    and is not very clear for any platform. I will assume this means using any method to post
    to a http server will do the  trick
    https://github.com/drawpile/Drawpile/b/rutorrent/lob/master/doc/server-api.md
    Commands:
            drawpilegetsessions
                Returns all sessions running
                    GET /sessions/
                    [
                        {
                            "id": "uuid (unique session ID)",
                            "alias": "ID alias (if set)",
                            //"protocol": "session protocol version",
                            "userCount": "number of users",
                            //"founder": "name of the user who created the session",
                            "title": "session title",
                            //"hasPassword": true/false (is the session password protected),
                            //"closed": true/false (is the session closed to new users),
                            "persistent": true/false (is persistence enabled for this session),
                            "nsfm": true/false (does this session contain NSFM content),
                            "startTime": "timestamp",
                            "size": history size in bytes,
                        }, ...
                    ]
            drawpilegetusersadmin
                Returns all users all information
                    GET /users/
                    [
                        {
                            "session": "session ID (if empty, this user hasn't joined any session yet)",
                                translate this ID to title
                            "id": user ID (unique only within the session),
                            "name": "user name",
                            "ip": "IP address",
                            "auth": true/false (is authenticated),
                            "op": true/false (is session owner),
                            //"muted": true/false (is blocked from chat),
                            //"mod": true/false (is a moderator),
                            //"tls": true/false (is using a secure connection)
                        }
            drawpilegetusers
                Returns all users does not show ip
                    GET /users/
                    [
                        {
                            "session": "session ID (if empty, this user hasn't joined any session yet)",
                                translate this ID to title
                            //"id": user ID (unique only within the session),
                            "name": "user name",
                            //"ip": "IP address",
                            //"auth": true/false (is authenticated),
                            //"op": true/false (is session owner),
                            //"muted": true/false (is blocked from chat),
                            //"mod": true/false (is a moderator),
                            //"tls": true/false (is using a secure connection)
                        }
                    ]
            drawpilesendmsg session "message" #might not be needed
                Send message to drawpile chat
                PUT /session/:id/
                {
                    "message": "send a message to all participants",
                    //"alert": "send an alert to all participants"
                }
            drawpilesendalert session "alert" #might not be needed
                Send alert to drawpile chat
                PUT /session/:id/
                {
                    //"message": "send a message to all participants",
                    "alert": "send an alert to all participants"
                }
            drawpilesendspam  "alert"
                Send alert to every session (for server alerts only)
                PUT /session/:id/
                {
                    //"message": "send a message to all participants",
                    "alert": "send an alert to all participants"
                }
    """
    @commands.command()
    async def drawpiledetail(self, type):
        await self.bot.say("Getting information")
        await self.bot.say(getdata(type))
        # url = "http://localhost:8081/users/"
        # output = requests.get(url, auth=HTTPBasicAuth('clara', 'amdk6-2')).text # displays content
        # this did not work with the super complex php loader for wordpress but it can do some basic stuff
        # might not be able handle the json out wont know til tomorrow sadly
        # await self.bot.say("{0}" .format(output))
    @commands.command()
    async def drawpile(self):
        session_json = getdata("sessions")
        session_data = json.dumps(session_json, separators=(',', ':'))
        await self.bot.say(session_json)
        await self.bot.say(session_json[0]['title'])
        #for a in range(len(session_data)):
        #    await self.bot.say("Session #:\t {0}" .format(a+1))
        #    await self.bot.say("Title:\t\t {0}" .format(session_json[a]['title']))
        #    await self.bot.say("Alias:\t\t {0}" .format(session_json[a]['alias']))
        #    await self.bot.say("Users:\t\t {0}" .format(session_json[a]['userCount']))
        #    await self.bot.say("ID:\t\t {0}" .format(session_json[a]['id']))
        #    await self.bot.say("Session Size:\t {0}" .format(convert_size(session_json[a]['size'])))
        #    await self.bot.say("")
       # user_json = getdata("users")
       # users_data = json.load()
       # for b in range(len(users_data)):
       #     await self.bot.say("User:\t\t {0}" .format(users_data[b]['name']))
       #     userip = users_data[b]['ip']
       #     ip_data = getip(userip)
       #     await self.bot.say("IP:\t\t {0}" .format(ip_data))
       #     usersession = users_data[b]['session']
       #     for c in range(len(session_data)):
       #         if usersession == session_data[c]['id']:
       #             await self.bot.say("Current Session: {0}" .format(session_data[c]['title']))
       #             await self.bot.say("Session ID:\t {0}" .format(users_data[b]['session']))
       #     await self.bot.say("")

    # async def drawpilesessionsizes(self):
    #     """Get all sessions running sizes"""
    #     basedir = "/var/drawpile/sessions"
    #     with open("/var/drawpile/templates/drawpile.ini", "r") as a:
    #         file = a.readlines()
    #         a.close()
    #     for i, line in enumerate(file):
    #         if "sessionSizeLimit" in line:
    #             for l in file[i:i+1]:
    #                 sizelimit = l
    #     await self.bot.say("Drawpile Session information")
    #     await self.bot.say(sizelimit)
    #     for f in os.listdir(basedir):
    #         path = os.path.join(basedir, f)
    #         if os.path.isfile(path):
    #             if re.search('.dprec', path):
    #                 size = os.path.getsize(path)
    #                 await self.bot.say("File:\t{0}" .format(path))
    #                 await self.bot.say("Size:\t{0}" .format(convert_size(size)))

def setup(bot):
    bot.add_cog(Drawpile(bot))
