from abc import ABC, abstractmethod

class Window(ABC):
	def __init__(self, width=680, height=680, posX=50, posY=50, parent=None):
		self.width = width
		self.height = height
		self.posX = posX
		self.posY = posY

		self.name = "Window"
		self.parent = parent
		self.children = []

		if parent:
			parent.addChild(self)

	def addChild(self, child):
		self.children.append(child)

	def removeChild(self, child):
		self.children.remove(child)

	@abstractmethod
	def create(self):
		pass