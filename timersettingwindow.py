import tkinter as tk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor

import constants as ct
from config import *
from window import *



class TimerSettingWindow(Window):
	def __init__(self, parent, posX=50, posY=50):
		super().__init__(parent=parent)

		self.name = "Timer setting window"
		self.posX = posX
		self.posY = posY
		self.window = tk.Toplevel()
		self.size_entry = tk.IntVar(self.window, min(self.parent.window.winfo_width(), self.parent.window.winfo_height()))

	def on_closing(self):
		self.parent.removeChild(self)
		self.window.destroy()

	def create(self):
		self.window.title("Timer settings")
		self.window.geometry("300x120+%d+%d" % (self.posX-100, self.posY-70))
		self.window.resizable(False, False)

		self.window.columnconfigure(0, weight=1)
		self.window.columnconfigure(1, weight=1)

		font = tkFont.Font(size=ct.font_size_default)
		padx = 5
		pady = 5
		curRow = 0



		def on_size_change():
			self.parent.window.geometry("%dx%d" % (self.size_entry.get(), self.size_entry.get()))

		tk.Label(self.window, text="Window size (px):", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		tk.Spinbox(self.window, from_=50, to=1000, increment=10, width=5, font=font, textvariable=self.size_entry, state='readonly', readonlybackground="white", command=on_size_change).grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1

		def on_timer_color_change_btn():
			colors = askcolor(title="Timer color", parent=self.window)
			if colors[1]:
				self.parent.timer_color = colors[1]
				self.parent.canvas.itemconfigure(self.parent.arc, fill=colors[1], outline=colors[1])
				timer_color_btn.configure(background=colors[1])

		tk.Label(self.window, text="Timer color:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		timer_color_btn = tk.Button(self.window, text="     ", background=self.parent.timer_color, command=on_timer_color_change_btn)
		timer_color_btn.grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1

		def on_bg_color_change_btn():
			colors = askcolor(title="Background color", parent=self.window)
			if colors[1]:
				self.parent.bg_color = colors[1]
				self.parent.canvas.config(background=colors[1])
				bg_color_btn.configure(background=colors[1])

		tk.Label(self.window, text="Background color:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		bg_color_btn = tk.Button(self.window, text="     ", background=self.parent.bg_color, command=on_bg_color_change_btn)
		bg_color_btn.grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1