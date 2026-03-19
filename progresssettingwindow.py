import tkinter as tk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor

import constants as ct
from config import *
from window import *



class ProgressSettingWindow(Window):
	def __init__(self, parent, posX=50, posY=50):
		super().__init__(parent=parent)

		self.name = "Progress setting window"
		self.posX = posX
		self.posY = posY
		self.window = tk.Toplevel()

	def on_closing(self):
		self.parent.removeChild(self)
		self.window.destroy()

	def create(self):
		self.window.title("Progress settings")
		self.window.geometry("300x150+%d+%d" % (self.posX-100, self.posY-70))
		self.window.resizable(False, False)

		self.window.columnconfigure(0, weight=1)
		self.window.columnconfigure(1, weight=1)

		font = tkFont.Font(size=ct.font_size_default)
		padx = 5
		pady = 5
		curRow = 0



		fontsize_entry = tk.IntVar(self.window, self.parent.font_size)

		def on_fontsize_change():
			self.parent.changeFont(font_size=fontsize_entry.get())

		tk.Label(self.window, text="Font size:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		tk.Spinbox(self.window, from_=6, to=200, width=5, font=font, textvariable=fontsize_entry, state='readonly', readonlybackground="white", command=on_fontsize_change).grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1

		def on_text_color_change_btn():
			colors = askcolor(title="Text color", parent=self.window)
			if colors[1]:
				self.parent.text_color = colors[1]
				self.parent.canvas.itemconfigure(self.parent.progress_text, fill=colors[1])
				text_color_btn.configure(background=colors[1])

		tk.Label(self.window, text="Text color:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		text_color_btn = tk.Button(self.window, text="     ", background=self.parent.text_color, command=on_text_color_change_btn)
		text_color_btn.grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1

		def on_bar_color_change_btn():
			colors = askcolor(title="Progress bar color", parent=self.window)
			if colors[1]:
				self.parent.bar_color = colors[1]
				self.parent.canvas.itemconfigure(self.parent.progress_bar, fill=colors[1])
				bar_color_btn.configure(background=colors[1])

		tk.Label(self.window, text="Progress bar color:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		bar_color_btn = tk.Button(self.window, text="     ", background=self.parent.bar_color, command=on_bar_color_change_btn)
		bar_color_btn.grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
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