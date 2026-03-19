import math
import tkinter as tk
import tkinter.font as tkFont

import constants as ct
from config import *
from api import *
from window import *
from progresssettingwindow import *



class ProgressWindow(Window):
	def __init__(self, parent, numWindow=1, completed=[], totalAch=0, game_id=0, bg_color="magenta"):
		super().__init__(parent=parent)

		self.name = "Progress window"
		self.numWindow = numWindow
		self.width = 300
		self.height = 100
		self.bg_color = bg_color
		self.bar_color = "green"
		self.text_color = 'white'
		self.section = "Progress " + str(numWindow)
		self.game_id = game_id
		self.completed = completed
		self.rateComp = 0
		self.totalAch = totalAch
		self.font_size = 24
		self.canvas = None
		self.progress_bar = None
		self.progress_text = ''
		self.window = tk.Toplevel()
		self.setConfigs()

	def setConfigs(self):
		width = None
		height = None
		posX = None
		posY = None
		bg_color = None
		bar_color = None
		text_color = None
		font_size = None

		config = getConfigSection(self.section)
		if (config != None):
			if 'posX' in config:
				posX = config['posX']
			if 'posY' in config:
				posY = config['posY']
			if 'width' in config:
				width = config['width']
			if 'height' in config:
				height = config['height']
			if 'bg_color' in config:
				bg_color = config['bg_color']
			if 'bar_color' in config:
				bar_color = config['bar_color']
			if 'text_color' in config:
				text_color = config['text_color']
			if 'font_size' in config:
				font_size = config['font_size']

		if width != None and width.isdigit():
			self.width = int(width)
		if height != None and height.isdigit():
			self.height = int(height)
		if posX != None and posX.isdigit():
			self.posX = posX
		if posY != None and posY.isdigit():
			self.posY = posY
		if bg_color != None:
			self.bg_color = bg_color
		if bar_color != None:
			self.bar_color = bar_color
		if bar_color != None:
			self.bar_color = bar_color
		if font_size != None:
			self.font_size = font_size

	def on_closing(self):
		updateConfigSection(self.section, {
			'width': self.window.winfo_width(),
			'height': self.window.winfo_height(),
			'posX': self.window.winfo_x(),
			'posY': self.window.winfo_y(),
			'bg_color': self.bg_color,
			'bar_color': self.bar_color,
			'text_color': self.text_color,
			'font_size': self.font_size,
			'game_id': self.game_id
		})

		for child in self.children:
			child.on_closing()

		self.parent.removeChild(self)
		self.window.destroy()

	def on_x_close(self):
		self.game_id = 0
		self.on_closing()

	def checkCompletedAchievements(self, cheevo):
		ach_id = int(cheevo['AchievementID'])
		if not ach_id in self.completed:
			self.completed.append(ach_id)
			self.updateRateComp()

	def updateRateComp(self):
		numComp = len(self.completed)
		self.rateComp = (numComp/self.totalAch) if self.totalAch > 0 else 0
		self.canvas.itemconfigure(self.progress_text, text=("%d/%d (%.2f%%)" % (numComp, self.totalAch, self.rateComp*100)))
		self.canvas.coords(self.progress_bar, 0, 0, self.width*self.rateComp, self.height)

	def changeFont(self, font_family=None, font_size=None):
		font_family = "TkDefaultFont"
		if font_size != None:
			self.font_size = font_size

		self.canvas.itemconfigure(self.progress_text, font=(font_family, self.font_size))

	def on_progress_rightclick(self, event):
		# only 1 child per window
		for child in self.children:
			child.on_closing()

		progressSettingWindow = ProgressSettingWindow(parent=self, posX=event.x_root, posY=event.y_root)
		progressSettingWindow.create()

	def on_window_resize(self, event):
		self.canvas.configure(width=event.width, height=event.height)
		self.canvas.coords(self.progress_bar, 0, 0, event.width*self.rateComp, event.height)
		self.canvas.coords(self.progress_text, int(event.width)/2, int(event.height)/2)

	def create(self):
		self.window.title(self.section)
		self.window.geometry("%dx%d%+d%+d" % (int(self.width), int(self.height), int(self.posX), int(self.posY)))
		self.window.configure(background=self.bg_color)
		self.window.bind("<Button-3>", self.on_progress_rightclick)
		self.window.bind("<Configure>", self.on_window_resize)

		self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, background=self.bg_color, bd=0, highlightthickness=0, relief='ridge')
		self.canvas.pack()

		self.updateRateComp()

		self.progress_bar = self.canvas.create_rectangle(0, 0, self.width*self.rateComp, self.height, fill=self.bar_color, width=0)
		self.progress_text = self.canvas.create_text(int(self.width)/2, int(self.height)/2, text=("%d/%d (%.2f%%)" % (len(self.completed), self.totalAch, self.rateComp*100)), font=("TkDefaultFont", self.font_size), fill=self.text_color)


		self.window.protocol("WM_DELETE_WINDOW", self.on_x_close)