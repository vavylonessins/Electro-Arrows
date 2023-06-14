from gui import *
from const import *
import gui
import random


class ArrowsEffect:
	def __init__(self, sc, color, amount, speed=15):
		self.amount = amount
		self.sc = sc
		self.arrows = []
		self.x = 0
		self.base_h = self.sc.get_height()
		self.speed = speed
		for n in range(amount):# color  length                   d  t
			self.arrows.append(([color, random.randint(175, 225), 1, 1]))

	def draw(self):
		for i in range(self.amount):
			x = (self.sc.get_width()/self.amount*i+self.x) % self.sc.get_width()
			y1 = self.sc.get_height()
			y2 = self.sc.get_height()-(self.arrows[i][1]/self.base_h*self.sc.get_height())
			c = self.arrows[i][0]
			draw.arrow(self.sc, c, Vec2(x, y1), Vec2(x, y2))

	def update(self, delta):
		self.x += delta*self.speed
		for i in range(self.amount):
			l, d, t = self.arrows[i][-3:]
			l += d*delta*self.speed
			t -= delta
			if t <= 0:
				t = random.randint(1, 2)
				d = -d
			self.arrows[i] = [self.arrows[i][0], l, d, t]


class LevelCard:
	def __init__(self, sc, level, pos, size):
		self.sc = sc
		self.level = level
		self.pos = Vector2(pos)
		self.size = Vector2(size)
		self.title_font = gui.Font(gui.SYSTEM, 42, ("Console", "Droid Sans Mono", "Consolas", "Courier", "Monospace"))
		self.main_font = gui.Font(gui.SYSTEM,32, ("Console", "Droid Sans Mono", "Consolas", "Courier", "Monospace"))
	
	def draw(self):
		surf = Surface((int(self.size.x), int(self.size.y)), SRCALPHA)
		gui.draw.rect(surf, TOP, (0, 0, *self.size), 0, MARGIN)
		gui.draw.rect(surf, MAIN, (0, 0, *self.size), 1, MARGIN)

