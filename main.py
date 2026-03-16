import os

import constants as ct
from mainwindow import *



def main():
	validateConfig()

	if not os.path.exists(ct.badges_folder):
		os.mkdir(ct.badges_folder)

	mainWindow = MainWindow()
	mainWindow.create()


main()