import curses
import sys
import asyncio
import json

from bot import Bot
from loop import Loop
from commands import Commands
from funcs import Funcs

class Driver(Bot, Loop, Commands, Funcs):
	"""
	This could be considered the main class!
	Since I had no idea how to propperly do OOP when writing this I just opted to let everything 
	inherit into one single class and keep a global state through self, this, in combination with 
	me not knowing how to propperly utilize data structures results in a mess of different lists 
	of duplicate information and all around confusing data handling.
	"""
	def __init__(self):
		# Let the user choose a account from the accounts listed in the config file.
		with open("config.json","r") as file:
			d = json.load(file)
			
			# Could be done better with enumerate :D 
			counter = 1
			for v in d["accounts"]:
				print(counter,"\t",v["user"])
				counter+=1

			# This is a bad variable name
			self.index = int(input())-1

		asyncio.run(self.main())

	async def main(self):
		await self.log_in()


client = Driver()
