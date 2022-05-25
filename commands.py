import curses

import sys

from dh import DH

class Commands():
	def __init__(self):
		pass


	# working and updated
	async def pwd(self):
		if self.current[2] == None:
			self.messagelist.insert(0, "Client -> Listening to: #"+ self.channels[self.current[0]][self.current[1]].name + " @ "+  self.servers[self.current[0]].name )
		else:
			self.messagelist.insert(0, "Client -> Currently in "+self.current[2] + "'s dms")
		self.redraw()

	# working and updated
	async def use(self, n):
		self.current[0] = int(n)-1
		self.current[2] = None
		self.encrypt = False
		await self.switch(1)
		await self.channellist(self.current[0])

	# working and updated
	async def switch(self, n):
		if self.current[2] == None:
			if int(n)-1 <= len(self.servers):
				self.current[1] = int(n)-1
				self.redraw()
				messages = []
				print(self.channels[self.current[0]][self.current[1]])
				async for message in self.channels[self.current[0]][self.current[1]].history(limit=self.cli.main_height-3):
					messages.append(message)
				for message in reversed(messages):
					if message.content[:len(self.prefix1)] != self.prefix1 or message.content[:len(self.prefix2)] != self.prefix2:
						await self.parse_message(message)
				await self.pwd()

	# working and updated
	async def quit(self):
		curses.endwin()
		await self.bot.logout()
		sys.exit()

	# working and updated
	async def serverlist(self):
		index = 3
		self.cli.screen.addstr(index-1,5,"Server list")
		for server in self.servers:
			self.cli.screen.addstr(index,5," "+str(index-2) + ": "+ server.name[:self.cli.side_width-7-len(str(index-2))])
			index += 1
			self.cli.sidebar_window()
		self.cli.sidebar.refresh()
		self.redraw()

	# working and updated
	async def channellist(self, server):
		server = self.servers[int(server)-1]

		index = 3
		self.cli.screen.addstr(index-1, 5, server.name)
		for channel in server.channels:
			if channel.name in self.listened_channels:
				self.cli.sidebar_window()
				self.cli.sidebar.refresh()

				self.cli.screen.addstr(index,5," "+str(index-2) + " #"+channel.name[:self.cli.side_width-1])
				index += 1
		self.redraw()

	# not working ; måste fixas
	async def init(self):
		if self.current[2] != None:
			user = self.dmstuff[self.current[2]]
			dm = user.dm_channel

			for server in self.servers:
				member = server.get_member(user.id)

			self.dh = DH(int(member.activity.name), self.pub_key, self.pri_key)
			my_partial_key = self.dh.generate_partial_key()
			#self.crypto.public_key_peer = int(member.activity.name)
			#partial_key = self.crypto.get_partial()
			await dm.send(self.prefix1+str(my_partial_key))



	async def accept(self):
		if self.current[2] != None and self.stored_key != "":
			user = self.dmstuff[self.current[2]]
			dm = user.dm_channel

			# this looks weird
			for server in self.servers:
				member = server.get_member(user.id)
				if member != None:
					break

			self.dh = DH(self.pub_key, int(member.activity.name), self.pri_key)
			#self.crypto.public_key_peer = int(member.activity.name)
			partial_key_peer = self.stored_key
			self.stored_key = ""

			#partial_key = self.crypto.get_partial()
			my_partial_key = self.dh.generate_partial_key()
			await dm.send(self.prefix2+str(my_partial_key))
			print("partial key peer in accept() is:", partial_key_peer)
			#self.crypto.full_key = self.crypto.get_final(partial_key_peer)
			self.full_key = self.dh.generate_full_key(partial_key_peer)
			print("full key =", self.full_key)
			token = self.dh.gen_key(self.full_key)
			await self.start_encryption(token)



	async def tcrypt(self):
		self.encrypt = False
		self.dh = None


	# working and updated
	async def dmlist(self):
		index = 3
		self.cli.screen.addstr(index-1, 5, "DMs")
		for user in self.dm_objects:
			self.cli.sidebar_window()
			self.cli.sidebar.refresh()

			self.cli.screen.addstr(index,5, " "+str(index-2) + " @" + user.name[:self.cli.side_width-1])


	# working
	async def dm(self, inp):
		try:

			user = self.dmstuff[inp.lower()]
			if user.dm_channel == None:
				await user.create_dm()

			dm = user.dm_channel
			self.current[2] = user.name.lower()

		except Exception as e:
			self.messagelist.insert(0,"Client -> Error: User not found")
		try:
			messages = []
			async for message in dm.history(limit=self.cli.main_height-3):
				messages.append(message)
			for message in reversed(messages):
				if message.content[:len(self.prefix1)] != self.prefix1:
					await self.parse_message(message)
		except:
			pass
