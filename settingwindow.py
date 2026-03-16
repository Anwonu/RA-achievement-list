import math
import tkinter as tk
import tkinter.font as tkFont
from tkinter.colorchooser import askcolor

import constants as ct
from config import *
from window import *



class SettingWindow(Window):
	def __init__(self, parent, posX=50, posY=50):
		super().__init__(parent=parent)

		self.name = "Setting window"
		self.posX = posX
		self.posY = posY
		self.window = tk.Toplevel()

	def on_closing(self):
		self.parent.removeChild(self)
		self.window.destroy()

	def create(self):
		self.window.title("List settings")
		self.window.geometry("300x120+%d+%d" % (self.posX-100, self.posY-70))
		self.window.resizable(False, False)

		self.window.columnconfigure(0, weight=1)
		self.window.columnconfigure(1, weight=1)

		font = tkFont.Font(size=ct.font_size_default)
		padx = 5
		pady = 5
		curRow = 0


		# 4 is the border * 2
		badgeWidth = math.floor(ct.achiev_width * self.parent.size) + 4
		badgeHeight = math.floor(ct.achiev_height * self.parent.size) + 4


		numCols = tk.IntVar(self.window)
		numCols.set(int(math.floor(self.parent.window.winfo_width() / badgeWidth)))

		def on_cols_change():
			newWidth = numCols.get() * badgeWidth
			height = self.parent.window.winfo_height()

			self.parent.window.geometry("%dx%d" % (newWidth, height))

		tk.Label(self.window, text="Achievements per row:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		tk.Spinbox(self.window, from_=1, to=100, width=5, font=font, textvariable=numCols, state='readonly', readonlybackground="white", command=on_cols_change).grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1



		numRows = tk.IntVar(self.window)
		numRows.set(int(math.floor(self.parent.window.winfo_height() / badgeHeight)))

		def on_rows_change():
			width = self.parent.window.winfo_width()
			newHeight = numRows.get() * badgeHeight

			self.parent.window.geometry("%dx%d" % (width, newHeight))

		tk.Label(self.window, text="Number of rows:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		tk.Spinbox(self.window, from_=1, to=100, width=5, font=font, textvariable=numRows, state='readonly', readonlybackground="white", command=on_rows_change).grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1



		def on_cheevo_color_change_btn():
			colors = askcolor(title="Background color", parent=self.window)
			if colors[1]:
				self.parent.bg_color = colors[1]
				self.parent.window.configure(background=colors[1])
				self.parent.container.configure(background=colors[1])
				bg_color_btn.configure(background=colors[1])

		tk.Label(self.window, text="Background color:", font=font).grid(row=curRow, column=0, padx=padx, pady=pady, sticky="E")
		bg_color_btn = tk.Button(self.window, text="     ", background=self.parent.bg_color, command=on_cheevo_color_change_btn)
		bg_color_btn.grid(row=curRow, column=1, padx=padx, pady=pady, sticky="W")
		curRow += 1


		self.window.protocol("WM_DELETE_WINDOW", self.on_closing)