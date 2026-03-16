import math
import tkinter as tk
import tkinter.font as tkFont
from PIL import ImageTk, Image

import constants as ct
from config import *
from api import *
from window import *
from settingwindow import *



class AchievementWindow(Window):
	def __init__(self, parent, numWindow=1, game_id=0, size=1, show_unlocked=True, show_locked=True, bg_color="magenta"):
		super().__init__(parent=parent)

		self.name = "Achievement window"
		self.numWindow = numWindow
		self.bg_color = bg_color
		self.size = size
		self.section = "Achievement list " + str(numWindow)
		self.completed = []
		self.notcompleted = []
		self.game_id = game_id
		self.container = None
		self.list_completed = []
		self.list_notcompleted = []
		self.show_unlocked = show_unlocked
		self.show_locked = show_locked
		self.window = tk.Toplevel()
		self.setConfigs()

	def setConfigs(self):
		width = None
		height = None
		posX = None
		posY = None
		bg_color = None

		config = getConfigSection(self.section)
		if (config != None):
			if 'width' in config:
				width = config['width']
			if 'height' in config:
				height = config['height']
			if 'posX' in config:
				posX = config['posX']
			if 'posY' in config:
				posY = config['posY']
			if 'bg_color' in config:
				bg_color = config['bg_color']

		if width != None and width.isdigit():
			self.width = width
		if height != None and height.isdigit():
			self.height = height
		if posX != None and posX.isdigit():
			self.posX = posX
		if posY != None and posY.isdigit():
			self.posY = posY
		if bg_color != None:
			self.bg_color = bg_color

	def on_closing(self):
		updateConfigSection(self.section, {
			'width': self.window.winfo_width(),
			'height': self.window.winfo_height(),
			'posX': self.window.winfo_x(),
			'posY': self.window.winfo_y(),
			'bg_color': self.bg_color,
			'game_id': self.game_id,
			'size': self.size,
			'show_unlocked': self.show_unlocked,
			'show_locked': self.show_locked
		})

		for child in self.children:
			child.on_closing()

		self.parent.removeChild(self)
		self.window.destroy()

	# closed by clicking the close button, or alt f4, or something similar
	# NOT when closing the main window
	# this is for knowing which windows to open or not at the start
	def on_x_close(self):
		# if I put a valid value here, it'll be used when opening a new window of this numWindow
		self.game_id = 0
		self.size = ''
		self.show_unlocked = ''
		self.show_locked = ''
		self.on_closing()

	def prepareLists(self, completed=[], notcompleted=[]):
		self.completed = completed
		self.notcompleted = notcompleted

	# possible to just use window_create again on the frame and it'll move, but I'd have to redo the image
	def checkCompletedAchievements(self, cheevo):
		if self.show_unlocked:
			found = False
			for item in self.list_completed:
				if str(item.ach_id) == str(cheevo['AchievementID']):
					found = True

			if not found:
				frame = self.getBadgeFrame(cheevo['BadgeName'], cheevo['AchievementID'])
				self.container.window_create("1.0", window=frame)
				self.list_completed.append(frame)

		if self.show_locked:
			for item in self.list_notcompleted:
				if str(item.ach_id) == str(cheevo['AchievementID']):
					self.list_notcompleted.remove(item)
					item.destroy()
					break

	def getBadgeFrame(self, badge_id, ach_id, locked=False):
		game_folder = ct.badges_folder + str(self.game_id) + '/'
		frame = tk.Frame(self.container, bg=("black" if locked else "gold"), bd=0)
		frame.badge_id = badge_id
		frame.ach_id = ach_id
		imgaux = Image.open(game_folder + str(badge_id) + ("_lock" if locked else "") + '.png')
		if self.size != 1:
			imgaux = imgaux.resize((math.floor(ct.achiev_width * self.size), math.floor(ct.achiev_height * self.size)))
		image = ImageTk.PhotoImage(imgaux)
		label = tk.Label(frame, image=image, bd=0)
		label.img = image # just to save somewhere and not get apparently garbage collected
		label.pack(padx=2, pady=2)

		return frame

	def on_cheevo_rightclick(self, event):
		# only 1 child per window
		for child in self.children:
			child.on_closing()

		settingWindow = SettingWindow(parent=self, posX=event.x_root, posY=event.y_root)
		settingWindow.create()

	def create(self):
		#def on_cheevo_scroll(event):
		#	self.container.yview_scroll(int(-1*(event.delta/120)), "units")

		self.window.title(self.section)
		self.window.geometry("%dx%d%+d%+d" % (int(self.width), int(self.height), int(self.posX), int(self.posY)))
		self.window.configure(background=self.bg_color)
		self.window.minsize(72, 72)
		self.window.bind("<Button-3>", self.on_cheevo_rightclick)
		#self.window.bind("<MouseWheel>", on_cheevo_scroll)

		game_folder = ct.badges_folder + str(self.game_id) + '/'

		# https://stackoverflow.com/questions/76263866/using-tkinter-how-could-i-wrap-images-so-they-would-not-be-out-of-window
		self.container = tk.Text(self.window, wrap="word", background=self.bg_color, cursor="arrow", padx=0, pady=0, bd=0)
		self.container.config(state=tk.DISABLED)
		self.container.pack(fill=tk.BOTH, expand=True)

		for item in self.completed:
			frame = self.getBadgeFrame(item['BadgeName'], item['ID'])
			self.container.window_create("end", window=frame)
			self.list_completed.append(frame)

		for item in self.notcompleted:
			frame = self.getBadgeFrame(item['BadgeName'], item['ID'], True)
			self.container.window_create("end", window=frame)
			self.list_notcompleted.append(frame)

		self.window.protocol("WM_DELETE_WINDOW", self.on_x_close)