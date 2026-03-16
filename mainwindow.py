import os
import requests
import re
import tkinter as tk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
from io import BytesIO

import constants as ct
from config import *
from api import *
from alerts import *
from window import *
from achievementwindow import *
from timerwindow import *
import tooltip



class MainWindow(Window):
	def __init__(self):
		self.name = "Main window"
		self.window = tk.Tk()
		self.apikey_entry = tk.StringVar(self.window)
		self.apikey_readonly = tk.BooleanVar(self.window, value=False)
		self.username_entry = tk.StringVar(self.window)
		self.username_readonly = tk.BooleanVar(self.window, value=False)
		self.gameid_entry = tk.StringVar(self.window)
		self.size_entry = tk.DoubleVar(self.window, 1)
		self.show_unlocked = tk.BooleanVar(self.window, True)
		self.show_locked = tk.BooleanVar(self.window, True)
		self.bg_color = "magenta"

		self.timerWindow = None
		self.timerRunning = False
		self.currentTimer = 0

		config = getConfigSection('Initial config')
		super().__init__(width=600, height=420, posX=config['posX'], posY=config['posY'])
		self.setConfigs()

	def setConfigs(self):
		config = getConfig()
		apikey = config['API']['key']
		apikey_readonly = config['API']['readonly']
		username = config['User']['username']
		username_readonly = config['User']['readonly']
		gameid_entry = config['Initial config']['game_id']
		size_entry = config['Initial config']['size']
		bg_color = config['Initial config']['bg_color']

		if apikey != None:
			self.apikey_entry.set(apikey)
		if apikey_readonly != None:
			self.apikey_readonly.set(apikey_readonly)
		if username != None:
			self.username_entry.set(username)
		if username_readonly != None:
			self.username_readonly.set(username_readonly)
		if gameid_entry != None:
			self.gameid_entry.set(gameid_entry)
		if size_entry != None:
			self.size_entry.set(size_entry)
		if bg_color != None:
			self.bg_color = bg_color

	def on_closing(self):
		updateConfigSection('Initial config', {
			'posX': self.window.winfo_x(),
			'posY': self.window.winfo_y()
		})

		# if I do the usual loop, children will delete themselves and might skip some here
		for i in range(len(self.children)-1, -1, -1):
			self.children[i].on_closing()

		self.window.destroy()

	def removeChild(self, child):
		super().removeChild(child)

		cheevoOpened = False
		for child in self.children:
			if child.name == "Achievement window":
				cheevoOpened = True

		if not cheevoOpened:
			self.stopTimer()

	def runTimer(self):
		if self.timerRunning == False:
			self.timerRunning = True
			self.currentTimer = ct.refresh_time
			self.window.after(ct.refresh_step, self.lowerTimer)

	def stopTimer(self):
		if self.timerRunning == True:
			self.timerRunning = False
			self.currentTimer = ct.refresh_time

	def lowerTimer(self):
		if self.timerRunning == True:
			self.currentTimer -= ct.refresh_step

			if self.timerWindow:
				self.timerWindow.updateTimer()

			if self.currentTimer <= 0:
				self.checkLatestAchievements()
				self.stopTimer()
				self.runTimer()
			else:
				self.window.after(ct.refresh_step, self.lowerTimer)

	def checkLatestAchievements(self):
		if self.timerRunning == True:
			api = getRecent(1)
			
			if (api):
				for item in api:
					for child in self.children:
						if (str(child.game_id) == str(item['GameID'])):
							child.checkCompletedAchievements(item)

		#self.window.after(ct.refresh_time, self.checkLatestAchievements)


	def create(self):
		self.window.title("Initial config")
		self.window.geometry("%dx%d%+d%+d" % (int(self.width), int(self.height), int(self.posX), int(self.posY)))
		self.window.resizable(False, False)

		self.window.columnconfigure(0, weight=1)
		self.window.columnconfigure(1, weight=1)
		self.window.columnconfigure(2, weight=1)

		font = tkFont.Font(size=ct.font_size_default)
		font_big = tkFont.Font(size=ct.font_size_big)
		padx = 5
		pady = 5
		curRow = 0





		def on_apikey_change(*args):
			updateConfig('API', 'key', self.apikey_entry.get())

		self.apikey_entry.trace_add("write", on_apikey_change)

		tk.Label(self.window, text="API key:", font=font).grid(row=curRow, column=0, padx=padx, pady=(pady+5, 0), sticky="E")
		apikeyentrywidget = tk.Entry(self.window, font=font, textvariable=self.apikey_entry, show="*", state=("readonly" if self.apikey_readonly.get() else "normal"))
		apikeyentrywidget.grid(row=curRow, column=1, padx=padx, pady=(pady, 0), sticky="W")
		info_apikey = tk.Label(self.window, text=" ? ", font=font_big, borderwidth=1, relief="solid")
		info_apikey.grid(row=curRow, column=2, padx=padx, pady=pady+5, sticky="W")
		tooltip.CreateToolTip(info_apikey, text="Settings → Authentication → copy/paste \"Web API Key\" here.")
		curRow += 1

		def on_apikey_check_change():
			if self.apikey_readonly.get():
				apikeyentrywidget.config(state="readonly")
			else:
				apikeyentrywidget.config(state="normal")

			updateConfig('API', 'readonly', self.apikey_readonly.get())

		tk.Checkbutton(self.window, text="Make field readonly", variable=self.apikey_readonly, command=on_apikey_check_change).grid(row=curRow, column=1, padx=padx, pady=(0, pady), sticky="W")
		curRow += 1






		def on_username_change(*args):
			updateConfig('User', 'username', self.username_entry.get())

		self.username_entry.trace_add("write", on_username_change)

		tk.Label(self.window, text="Username/ULID:", font=font).grid(row=curRow, column=0, padx=padx, pady=(pady, 0), sticky="E")
		usernameentrywidget = tk.Entry(self.window, font=font, textvariable=self.username_entry, state=("readonly" if self.username_readonly.get() else "normal"))
		usernameentrywidget.grid(row=curRow, column=1, padx=padx, pady=(pady, 0), sticky="W")

		def on_ulid_btn_clicked():
			username = self.username_entry.get().strip()

			if username == '':
				showWarning('Warning', 'Put a username')
				return

			api = getProfile(username)
			if (api):
				self.username_entry.set(api['ULID'])

		usernamebutton = tk.Button(self.window, text="Get ULID from username", command=on_ulid_btn_clicked, state=("disabled" if self.username_readonly.get() else "normal"))
		usernamebutton.grid(row=curRow, column=2, padx=padx, pady=(pady, 0), sticky="W")
		curRow += 1

		def on_username_check_change():
			if self.username_readonly.get():
				usernameentrywidget.config(state="readonly")
				usernamebutton.config(state="disabled")
			else:
				usernameentrywidget.config(state="normal")
				usernamebutton.config(state="normal")
			
			updateConfig('User', 'readonly', self.username_readonly.get())

		tk.Checkbutton(self.window, text="Make field readonly", variable=self.username_readonly, command=on_username_check_change).grid(row=curRow, column=1, padx=padx, pady=(0, pady), sticky="W")
		info_username = tk.Label(self.window, text=" ? ", font=font_big, borderwidth=1, relief="solid")
		info_username.grid(row=curRow, column=2, padx=padx, pady=pady, sticky="W")
		tooltip.CreateToolTip(info_username, text="You can keep just the username here, but ULID makes sure\nit's still you even after a username change.")
		curRow += 1




		def on_game_id_change(*args):
			updateConfig('Initial config', 'game_id', self.gameid_entry.get())

		self.gameid_entry.trace_add("write", on_game_id_change)

		def on_lastgame_btn_clicked():
			api = getProfile(self.username_entry.get())
			if (api):
				try:
					self.gameid_entry.set(api['LastGameID'])
				except:
					showWarning('Error', 'No last game found.')

		tk.Label(self.window, text="Game ID:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		tk.Entry(self.window, font=font, textvariable=self.gameid_entry).grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		tk.Button(self.window, text="Get last game played", command=on_lastgame_btn_clicked).grid(row=curRow, column=2, padx=padx, pady=pady, sticky="W")
		curRow += 1




		def on_size_change():
			updateConfig('Initial config', 'size', self.size_entry.get())

		tk.Label(self.window, text="Badge size (multiplier):", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		tk.Spinbox(self.window, from_=0.5, to=1, increment=0.05, width=5, font=font, textvariable=self.size_entry, state='readonly', readonlybackground="white", command=on_size_change).grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1




		def on_show_change():
			if self.show_locked.get() == False and self.show_unlocked.get() == False:
				open_btn.config(state="disabled")
			else:
				open_btn.config(state="normal")

		tk.Label(self.window, text="Show achievements:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		tk.Checkbutton(self.window, text="Show unlocked achievements", variable=self.show_unlocked, command=on_show_change).grid(row=curRow, column=1, padx=padx, pady=(pady, 0), sticky="W")
		curRow += 1
		tk.Checkbutton(self.window, text="Show locked achievements", variable=self.show_locked, command=on_show_change).grid(row=curRow, column=1, padx=padx, pady=(0, pady), sticky="W")
		curRow += 1




		def on_bg_color_change_btn():
			colors = askcolor(title="Background color", parent=self.window)
			if colors[1]:
				self.bg_color = colors[1]
				bg_color_btn.configure(background=colors[1])
				updateConfig('Initial config', 'bg_color', colors[1])

		tk.Label(self.window, text="Default background color:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		bg_color_btn = tk.Button(self.window, text="     ", background=self.bg_color, command=on_bg_color_change_btn)
		bg_color_btn.grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		info_bg_color = tk.Label(self.window, text=" ? ", font=font_big, borderwidth=1, relief="solid")
		info_bg_color.grid(row=curRow, column=2, padx=padx, pady=pady, sticky="W")
		tooltip.CreateToolTip(info_bg_color, text="This will be the default background when creating a new achievement list;\nafter the first time, you'll have to use the individual setting to change.")
		curRow += 1





		def on_timer_btn_clicked():
			for child in self.children:
				if child.name == "Timer window":
					child.on_closing()

			timer = TimerWindow(parent=self, bg_color=self.bg_color)
			timer.create()

		timer_btn = tk.Button(self.window, text="Timer window", font=font, command=on_timer_btn_clicked)
		timer_btn.grid(row=curRow, column=2, padx=padx, pady=(pady+20, pady))




		# this next part is kind of a mess, but it works ig

		def on_openlist_btn_clicked(game_id=None, size=None, show_unlocked=None, show_locked=None, bg_color=None, numWindow=1):
			if game_id == None:
				game_id = self.gameid_entry.get().strip()
			if size == None:
				size = self.size_entry.get()
			if show_unlocked == None:
				show_unlocked = self.show_unlocked.get()
			if show_locked == None:
				show_locked = self.show_locked.get()
			if bg_color == None:
				bg_color = self.bg_color

			if game_id == '':
				showWarning('Error', "Put a game ID.")
				return

			if not game_id.isdigit():
				showWarning('Error', "Put a valid ID.")
				return

			game = getGameWithUser(game_id)
			if game:
				# download badges, show progress on that if it is downloading, and separate completed from not completed achievements
				showProgression = False
				counter = 0
				total = game['NumAchievements'] * 2

				game_folder = ct.badges_folder + game_id + '/'
				if not os.path.exists(game_folder):
					os.mkdir(game_folder)
					showProgression = True
					open_btn.config(state="disabled")
					dl_msg_widget.config(text="Downloading badges... 0/%d" % total)

				cheevos = game['Achievements']

				completed = []
				notcompleted = []
				session = requests.Session()

				for item in cheevos.values():
					# download images
					id = item['BadgeName']
					path = game_folder + id + '.png'
					pathL = game_folder + id + '_lock.png'

					if (not os.path.isfile(path)):
						u = session.get("https://media.retroachievements.org/Badge/" + id + ".png")
						image = Image.open(BytesIO(u.content))
						image.save(path, "png")
						counter += 1
						dl_msg_widget.config(text="Downloading badges... %d/%d" % (counter, total))
						self.window.update()

					if (not os.path.isfile(pathL)):
						u = session.get("https://media.retroachievements.org/Badge/" + id + "_lock.png")
						image = Image.open(BytesIO(u.content))
						image.save(pathL, "png")
						counter += 1
						dl_msg_widget.config(text="Downloading badges... %d/%d" % (counter, total))
						self.window.update()

					# check if completed
					if 'DateEarnedHardcore' in item:
						if show_unlocked:
							completed.append(item)
					else:
						if show_locked:
							notcompleted.append(item)

				open_btn.config(state="normal")
				dl_msg_widget.config(text="")
				completed = sorted(completed, key = lambda x: x['DateEarnedHardcore'], reverse = True)
				notcompleted = sorted(notcompleted, key = lambda x: (x['DisplayOrder'], x['ID']))

				self.createAchievementWindow(completed, notcompleted, game_id, size, show_unlocked, show_locked, bg_color, numWindow)
			else:
				showWarning('Error', "ID doesn't exist.")

		open_btn = tk.Button(self.window, text="Open achievement list", font=font, command=on_openlist_btn_clicked)
		open_btn.grid(row=curRow, column=1, padx=padx, pady=(pady+20, pady))
		curRow += 1

		dl_msg_widget = tk.Label(self.window, text='')
		dl_msg_widget.grid(row=curRow, column=0, columnspan=3, padx=padx, pady=0)
		curRow += 1


		

		# check if we need to start with opened windows
		def checkOpenedWindows():
			config = getConfig()
			for s in config:
				m = re.search(r"Achievement list (\d+)", s)
				if m:
					if 'game_id' in config[s] and config[s]['game_id'].isdigit() and int(config[s]['game_id']) > 0:
						size = 1
						show_unlocked = True
						show_locked = True
						bg_color = "magenta"

						if 'size' in config[s] and config[s]['size'] != '':
							size = float(config[s]['size'])
						if 'show_unlocked' in config[s] and config[s]['show_unlocked'] != '':
							show_unlocked = (config[s]['show_unlocked'] == 'True')
						if 'show_locked' in config[s] and config[s]['show_locked'] != '':
							show_locked = (config[s]['show_locked'] == 'True')
						if 'bg_color' in config[s] and config[s]['bg_color'] != '':
							bg_color = config[s]['bg_color']

						on_openlist_btn_clicked(config[s]['game_id'], size, show_unlocked, show_locked, bg_color, int(m.group(1)))

				elif s == "Timer":
					if 'opened' in config[s] and str(config[s]['opened']) == 'True':
						on_timer_btn_clicked()


		self.window.after(10, checkOpenedWindows)

		self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
		self.window.mainloop()



	def createAchievementWindow(self, completed, notcompleted, game_id, size, show_unlocked, show_locked, bg_color, numWindow=1):
		for child in self.children:
			if child.name == "Achievement window" and numWindow < child.numWindow + 1:
				numWindow = child.numWindow + 1

		cheevoWindow = AchievementWindow(parent=self, numWindow=numWindow, game_id=game_id, size=size, show_unlocked=show_unlocked, show_locked=show_locked, bg_color=bg_color)
		cheevoWindow.prepareLists(completed, notcompleted)
		cheevoWindow.create()
		self.window.update()

		self.runTimer()