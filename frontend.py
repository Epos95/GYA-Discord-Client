import curses
from curses.textpad import Textbox, rectangle
import os



class Frontend:
	if os.name == "nt":
		os.system("title Damned-Discord-Client")

	def __init__(self):
		self.screen = curses.initscr()
		self.height, self.width = self.screen.getmaxyx()
		rectangle(self.screen,0,1,self.height-1, self.width-2)
		curses.noecho()
		curses.halfdelay(1)
		#curses.cbreak()
		#self.screen.keypad(1)

		try:
			self.update()


		except Exception as e:
			print(e)
			self.screen.addstr(1,2, "Screen size too small")

	def update(self):
		self.sidebar_window()
		self.input_window()
		self.main_window()

		self.screen.refresh()
		self.sidebar.refresh()
		self.main.refresh()
		self.input.refresh()

	def sidebar_window(self):
		side_height = int(self.height-2)
		side_width = int(self.width/4)

		self.sidebar = curses.newwin(side_height, side_width,  1,3)
		self.side_height, self.side_width = self.sidebar.getmaxyx()

		rectangle(self.sidebar,0,0,self.side_height-1,self.side_width-2)

	def main_window(self):
		main_height = self.height-2-self.input_height
		main_width = self.width-5-self.side_width

		self.main = curses.newwin(main_height,main_width,  1,int(self.side_width+3))
		self.main_height, self.main_width = self.main.getmaxyx()

		rectangle(self.main, 0,0,self.main_height-1, self.main_width-2)

	def input_window(self):
		input_height = int(self.height/5)
		input_width = self.width-5-self.side_width

		self.input = curses.newwin(input_height,input_width,    self.height-1-input_height,self.side_width+3)
		self.input_height, self.input_width = self.input.getmaxyx()

		rectangle(self.input, 0,0, self.input_height-1, self.input_width-2)
