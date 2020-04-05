import discord
from discord.ext import commands
from discord import DiscordException

import asyncio
import curses
import sys
import json

from dh import DH
from test import DH_Endpoint

class Bot():
	def __init__(self):
		pass

	async def log_in(self):
		self.bot = commands.Bot(command_prefix="!",
		description="lmao",
		self_bot=True)

		with open("config.json","r") as file:
			self.config = json.load(file)

		print("Using: " + self.config["accounts"][self.index]["user"])

		self.token = self.config["accounts"][self.index]["token"]

		self.pri_key = self.config["accounts"][self.index]["private"]
		self.pub_key = self.config["accounts"][self.index]["public"]

		self.game = discord.Game(str(self.pub_key))
		self.encrypt = False
		self.prefix1 = "p@5KRE{ITx"
		self.prefix2 = "F038[^*4H3"

		self.stored_key = ""


		@self.bot.event
		async def on_connect():
			await self.bot.change_presence(status=discord.Status.online, activity=self.game)

			self.servers = []
			self.channels = []
			self.dmstuff = {}
			self.messagelist = []
			self.current = [0,0,None]

			listened_servers = [server for server in self.config["servers"]]
			self.server_objects = [server for server in self.bot.guilds if server.name in listened_servers]

			self.friends = [user for user in self.bot.user.friends]
			self.dm_objects = [user for user in self.bot.user.friends if user.name in self.config["dm users"]]

			self.listened_channels = []

			for server in self.config["servers"]:
				for channel in self.config["servers"][server]["channels"]:
					self.listened_channels.append(channel)

			self.channel_objects = []
			for server in self.server_objects:
				for channel in server.channels:
					if channel.name in self.listened_channels:
						self.channel_objects.append(channel)

			for server in self.bot.guilds:
				if server.name in listened_servers:
					self.servers.append(server)

					channels = []
					for channel in server.channels:
						if channel.name in self.listened_channels:
							channels.append(channel)

					if channels != []:
						self.channels.append(channels)

			for dm_obj in self.dm_objects:
				self.dmstuff[dm_obj.name.lower()] = dm_obj

			future = asyncio.ensure_future(self.start_frontend())

			print("in on_connect, self.channels is", self.channels)
			await asyncio.sleep(1)
			await self.use(1)


		@self.bot.event
		async def on_ready():
			pass



		@self.bot.event
		async def on_message(message):

			s = self.servers[self.current[0]]
			c = self.channels[self.current[0]][self.current[1]]
			d = self.current[2]

			if s == message.guild and c == message.channel and d == None:
				pass
			elif d != None and message.channel == self.dmstuff[self.current[2]].dm_channel:
				pass
			else:
				return


			await self.parse_message(message)

			var = 1
			for thing in self.messagelist:
				self.cli.main_window()
				self.cli.main.refresh()

				self.cli.screen.addstr(self.cli.main_height-var, self.cli.side_width+5, thing)
				var += 1

		try:
			await self.bot.login(self.token, bot=False)
			await self.bot.connect()
		except:
			print("Error")
			sys.exit()
			quit()
