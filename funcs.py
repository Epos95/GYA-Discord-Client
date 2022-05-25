from cryptography.fernet import Fernet

class Funcs():
	def __init__(self):
		pass

	def redraw(self):
		var = 1
		for thing in self.messagelist:
			self.cli.main_window()
			self.cli.main.refresh()

			self.cli.screen.addstr(self.cli.main_height-var, self.cli.side_width+5, str(thing))
			var += 1

	async def start_encryption(self, token):
		self.f = Fernet(token)
		self.encrypt = True

	async def parse_message(self, message):
		if self.encrypt:
			msg = message.content.encode("utf-8")
			msg = self.f.decrypt(msg)
			message.content = msg.decode("utf-8")
		message.content = message.content.replace("\n", " ")
		if message.content[:len(self.prefix1)] == self.prefix1 and message.author != self.bot.user:
			self.stored_key = message.content[len(self.prefix1):]
			self.messagelist.insert(0,"Client -> " + message.author.name + " wants to use crypto, /accept to accept")

		elif message.content[:len(self.prefix2)] == self.prefix2 and message.author != self.bot.user:
			partial_key_peer = message.content[len(self.prefix2):]
			self.full_key = self.dh.generate_full_key(partial_key_peer)
			print("final key is:", self.full_key)
			token = self.dh.gen_key(self.full_key)
			await self.start_encryption(token)
		else:
			final = message.author.name + " -> "
			for char in message.content:
				if len(final) == self.cli.main_width-4:
					if len(self.messagelist) > self.cli.main_height-2:
						del self.messagelist[self.cli.main_height-2:]
					self.messagelist.insert(0,final)
					final = " " + char
				else:
					final += char

			if final != "":
				if len(self.messagelist) > self.cli.main_height-3:
					del self.messagelist[self.cli.main_height-3:]
				self.messagelist.insert(0,final)
