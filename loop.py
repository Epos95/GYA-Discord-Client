import curses
import asyncio

from frontend import Frontend
from contextlib import redirect_stderr

class Loop():
	def __init__(self):
		pass

	async def start_frontend(self):
		self.cli = Frontend()

		commands = [
		"/quit",
		"/serverlist",
		"/channellist",
		"/use",
		"/pwd",
		"/listen",
		"/tcrypt",
		"/dmlist",
		"/dm",
		"/switch",
		"/init",
		"/accept"
		]

		keys = {
		113 : "q",
		119 : "w",
		101 : "e",
		114 : "r",
		116 : "t",
		121 : "y",
		117 : "u",
		105 : "i",
		111 : "o",
		112 : "p",
		97 : "a",
		115 : "s",
		100 : "d",
		102 : "f",
		103 : "g",
		104 : "h",
		106 : "j",
		107 : "k",
		108 : "l",
		122 : "z",
		120 : "x",
		99 : "c",
		118 : "v",
		98 : "b",
		110 : "n",
		109 : "m",
		32 : " ",
		47 : "/",
		48 : "0",
		49 : "1",
		50 : "2",
		51 : "3",
		52 : "4",
		53 : "5",
		54 : "6",
		55 : "7",
		56 : "8",
		57 : "9",
		}
		string = ""

		while 1:
			try:
				k = self.cli.screen.getch()
				if k == "\n":
					k = None
				#cli.screen.addstr(10,0,k)
			except:
				k = None

			# backspace was pressed, remove last character from the string
			if (k == 127 or k == 8) and k != "":
				string = string[:-1]
				self.cli.input_window()
				self.cli.input.refresh()
				self.cli.screen.addstr(self.cli.height-self.cli.input_height,self.cli.side_width+5, string)

			# key was pressed, add it to the string
			if k in keys:
				string += keys[k]
				self.cli.screen.addstr(self.cli.height-self.cli.input_height,self.cli.side_width+5, string)

			# enter was pressed, handle the input
			if not string.isspace() and k == 10 and string != "":

				# handle commands
				if string.split()[0] in commands:
					string = string.split()

					if string[0] == "/use" and len(string) > 1:
						await self.use(string[1])

					elif string[0] == "/listen" and len(string) > 1:
						await self.listen(string[1])

					elif string[0] == "/switch" and len(string) > 1:
						await self.switch(string[1])

					elif string[0] == "/dm" and len(string) > 1:
						await self.dm(string[1])


					elif string[0] == "/channellist":
						if len(string) > 1:
							await self.channellist(string[1])
						else:
							await self.channellist(self.current[1])

					elif string[0] == "/serverlist":
						await self.serverlist()
					elif string[0] == "/dmlist":
						await self.dmlist()


					elif string[0] == "/pwd":
						await self.pwd()
					elif string[0] == "/quit":
						await self.quit()
					elif string[0] == "/tcrypt":
						await self.tcrypt()
					elif string[0] == "/init":
						await self.init()
					elif string[0] == "/accept":
						await self.accept()

				else:
					if self.encrypt:
						string = self.f.encrypt(string.encode("utf-8")).decode("utf-8")
					if self.current[2] != None:
						await self.dmstuff[self.current[2].lower()].send(string)
					else:
						await self.channels[self.current[0]][self.current[1]].send(string)

				#clear string
				string = ""

				# purge messagelist
				if len(self.messagelist) > self.cli.main_height-2:
					del self.messagelist[self.cli.main_height-2:]

				# print out the messagelist
				var = 1
				for thing in self.messagelist:
					self.cli.main_window()
					self.cli.main.refresh()

					#self.cli.screen.addstr(self.cli.main_height-1, self.cli.side_width+5, " "*(self.cli.main_width-1))
					self.cli.screen.addstr(self.cli.main_height-var, self.cli.side_width+5, str(thing))
					var += 1

				# updatera input_window
				self.cli.input_window()
				self.cli.input.refresh()

			# resize event
			if k == curses.KEY_RESIZE:
				self.cli.screen.erase()
				self.cli = Frontend()

			# flytta cursor efter input
			self.cli.screen.move(self.cli.height-self.cli.input_height, self.cli.side_width+5+len(string))

			await asyncio.sleep(0.00000001)
