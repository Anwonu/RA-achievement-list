import tkinter as tk

import constants as ct
from config import *
from window import *
from timersettingwindow import *



class TimerWindow(Window):
	def __init__(self, parent, bg_color):
		super().__init__(parent=parent)

		self.name = "Timer window"
		self.opened = True
		self.window = tk.Toplevel()
		self.bg_color = bg_color
		self.timer_color = "green"
		self.canvas = None
		self.arc = None

		self.parent.timerWindow = self

		updateConfig('Timer', 'opened', True)
		self.setConfigs()

	def setConfigs(self):
		width = None
		height = None
		posX = None
		posY = None
		bg_color = None
		timer_color = None

		config = getConfigSection('Timer')
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
			if 'timer_color' in config:
				timer_color = config['timer_color']

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
		if timer_color != None:
			self.timer_color = timer_color

	def on_closing(self):
		updateConfigSection('Timer', {
			'width': self.window.winfo_width(),
			'height': self.window.winfo_height(),
			'posX': self.window.winfo_x(),
			'posY': self.window.winfo_y(),
			'bg_color': self.bg_color,
			'timer_color': self.timer_color,
			'opened': self.opened
		})

		for child in self.children:
			child.on_closing()

		self.parent.removeChild(self)
		self.parent.timerWindow = None
		self.window.destroy()

	def on_x_close(self):
		self.opened = False
		self.on_closing()

	def on_timer_rightclick(self, event):
		# only 1 child per window
		for child in self.children:
			child.on_closing()

		settingWindow = TimerSettingWindow(parent=self, posX=event.x_root, posY=event.y_root)
		settingWindow.create()

	def on_window_resize(self, event):
		self.canvas.configure(width=event.width, height=event.height)
		minSide = min(event.width, event.height)
		self.canvas.coords(self.arc, 10, 10, minSide-10, minSide-10)

	def create(self):
		self.window.title("Timer")
		self.window.geometry("%dx%d%+d%+d" % (int(self.width), int(self.height), int(self.posX), int(self.posY)))
		self.window.configure(background=self.bg_color)
		#self.window.resizable(False, False)
		self.window.bind("<Button-3>", self.on_timer_rightclick)
		self.window.bind("<Configure>", self.on_window_resize)

		self.canvas = tk.Canvas(self.window, width=self.width, height=self.height, background=self.bg_color, bd=0, highlightthickness=0, relief='ridge')
		self.canvas.pack()
		self.arc = self.canvas.create_arc(10, 10, self.width-10, self.height-10, fill=self.timer_color, outline=self.timer_color, start=90, extent=0)


		self.window.protocol("WM_DELETE_WINDOW", self.on_x_close)

	def updateTimer(self):
		extent = (ct.refresh_time - self.parent.currentTimer) / ct.refresh_time * 360
		if extent == 360:
			extent = 359.9

		self.canvas.itemconfigure(self.arc, extent=extent)
		self.window.update()