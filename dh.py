import base64

class DH(object):
	""" 
	Class for handling the keys for encryption within the application.
	Just applies standard DH to get the other persons key.
	"""
	def __init__(self, public_key1, public_key2, private_key):
		self.public_key1 = public_key1
		self.public_key2 = public_key2
		self.private_key = private_key
		self.full_key = None

	def generate_partial_key(self):
		partial_key = self.public_key1**self.private_key
		partial_key = partial_key%self.public_key2
		return partial_key

	def generate_full_key(self, partial_key_r):
		full_key = int(partial_key_r)**self.private_key
		full_key = full_key%self.public_key2
		self.full_key = full_key
		return full_key

	def gen_key(self, key):
		i = 0
		key = str(key)
		var = len(key)
		while len(key) != 32:
			key += key[i]
			i += 1
			if i == var:
				i =0
		return base64.urlsafe_b64encode(bytes(key,"utf-8"))
