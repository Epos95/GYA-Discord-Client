import discord
from discord.ext import commands
from discord import DiscordException

import asyncio
import curses
import sys
import json

from dh import DH

class Bot():
	def __init__(self):
		pass

	async def log_in(self):
		"""
		Logs in the user and initializes the application by declaring the 
		wrapper functions which discord needs to make the bot work.
		"""

		# The discord.bot object which acts as our connection to discord.
		self.bot = commands.Bot(command_prefix="!",
			description="lmao",
			self_bot=True)

		# Load the config file containing which users and servers to pay attention to among other things.
		with open("config.json","r") as file:
			self.config = json.load(file)

		print(f'Using: {self.config["accounts"][self.index]["user"]}')

		# The desired accounts discord token.
		self.token = self.config["accounts"][self.index]["token"]

		# The clients public and private keys for encryption shenanigans.
		self.pri_key = self.config["accounts"][self.index]["private"]
		self.pub_key = self.config["accounts"][self.index]["public"]

		# The "currently playing" functionality in discord gives us a way to 
		# broadcast the public key without engaging in any actual transfer of 
		# information through the direct messages.
		self.game = discord.Game(str(self.pub_key))
		
		# Flag for if the client should treat the messages as encrypted
		# bad design since it might enable encryption globally(?)
		self.encrypt = False

		# prefix for when sending the keys between clients.
		self.prefix1 = "p@5KRE{ITx"
		self.prefix2 = "F038[^*4H3"

		# The targets public key.
		self.stored_key = ""

		# Built in discord function that gets called on the on_connect event from discord
		# in our case it acts as a init function, setting up the client with all the 
		# servers and users from the config file.
		@self.bot.event
		async def on_connect():
			
			# Set the accounts "currently playing" status to advertise the public key
			# If this was rewritten today discord now has functionality for writing 
			# your own description of your account which could be used instead of the 
			# "currently playing" status.
			await self.bot.change_presence(status=discord.Status.online, activity=self.game)

			# The server and channel objects to pay attention to
			self.servers = []
			self.channels = []

			# hashmap of the dm name to the dm channel object
			self.dmstuff = {}

			# The messages to show in the message view
			self.messagelist = []

			# List containing information about the current state of the client:
			# [0] = int representing the index of the current server into self.servers
			# [1] = int representing the index of the current channel into self.channels
			#		kind of since self.channels is actually a 2 dimensional list of the 
			#		servers' channels. 
			# [2] = None if not in a dm, else its the name of the current user
			#       This name can then be used with self.dmstuff to get the dm obj.
			self.current = [0,0,None]

			# The servers we are currently listening to per the config
			# in retrospect this is kind of a unnecesary list comprehension
			listened_servers = [server for server in self.config["servers"]]
			self.server_objects = [server for server in self.bot.guilds if server.name in listened_servers]

			# Gets all the potential dms and filters them through the config
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

			# Run the frontend as a future.
			future = asyncio.ensure_future(self.start_frontend())

			await asyncio.sleep(1)

			# Set the client to use the first server availible to us on startup.
			await self.use(1)

		@self.bot.event
		async def on_message(message):
			"""
			Discord function which reacts to the on_message event.
			Runs this code each time the bot notices a message in 
			ANY server it is currently apart of.
			"""

			# Some shorthand variables for easiness
			server = self.servers[self.current[0]]
			channel = self.channels[self.current[0]][self.current[1]]
			dm = self.current[2]

			# Early return pattern is VERY clumsy to use here hah
			if server == message.guild and channel == message.channel and dm == None:
				# the message server is our server and the message channel is 
				# our channel and were not in a dm, go to handle the message event!
				pass
			elif dm != None and message.channel == self.dmstuff[self.current[2]].dm_channel:
				# we are in a dm and the message channel is the current channel.
				pass
			else:
				return

			# Parse AND react to the message, this is misusing a function since we 
			# say that this function shoudld PARSE a MESSAGE but instead it does 
			# so much more than that.
			await self.parse_message(message)

		# Starts the bot in the main "thread" (future)
		try:
			await self.bot.login(self.token, bot=False)
			await self.bot.connect()
		except:
			print("Error")
			sys.exit()
			quit()
