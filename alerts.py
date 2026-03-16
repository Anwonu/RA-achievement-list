from tkinter import messagebox

def showError(title, msg):
	messagebox.showerror(title, msg)

def showWarning(title, msg):
	messagebox.showwarning(title, msg)