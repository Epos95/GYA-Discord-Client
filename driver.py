import curses
import sys
import asyncio
import json

from bot import Bot
from loop import Loop
from frontend import Frontend
from commands import Commands
from funcs import Funcs

class Driver(Bot, Loop, Commands, Funcs):
	def __init__(self):
		with open("config.json","r") as file:
			d = json.load(file)
			counter = 1
			for v in d["accounts"]:
				print(counter,"\t",v["user"])
				counter+=1

			self.index = int(input())-1

		asyncio.run(self.main())

	async def main(self):
		await self.log_in()


client = Driver()
