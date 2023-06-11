import os


os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


from pygame import *
from pygame.transform import *


OPTIMIZE = HWACCEL|HWPALETTE|HWSURFACE
SYSTEM = 0b100000000000000000000
FILE = 0b010000000000000000000


class Vec2(Vector2):
	...


class Vec3(Vector3):
	...


def init():
	display.init()
	font.init()
	mixer.init()


def _calc_pos(ts, ss, ofs, alg):
	if alg[0] == "c":
		x = ts.get_width()/2-ss.get_width()/2+ofs[0]
	elif alg[0] == "r":
		x = ts.get_width()-ss.get_width()-ofs[0]
	else:
		x = ofs[0]

	if alg[1] == "c":
		y = ts.get_height()/2-ss.get_height()/2+ofs[1]
	elif alg[1] == "b":
		y = ts.get_height()-ss.get_height()-ofs[1]
	else:
		y = ofs[1]

	return Vec2(x, y)


class Window:
	def __init__(self, size, flags):
		self.size = size,
		self.flags = flags
		self.running = False

	def set_title(self, title):
		display.set_caption(title)

	def set_icon(self, icon):
		display.set_icon(icon)

	def show(self, *a, **k):
		if not a and not k:
			self.sc = display.set_mode(self.size, self.flags)
			self.clock = time.Clock()
			self.running = True
			for i in range(30): self.tick()
		else:
			self.blit(*a, **k)

	def blit(self, texture, offset=Vec2(0,0), align="lt", rect=None, mix_mode=0, flush=False):
		self.sc.blit(texture, _calc_pos(self.sc, texture, offset, align), rect, mix_mode)
		if flush:
			display.flip()

	def is_running(self):
		return True and self.running

	def get_new_events(self):
		return event.get()

	def close(self):
		self.running = False

	def fill(self, color):
		self.sc.fill(color)

	def apply(self):
		display.flip()

	def hide(self):
		display.quit()

	def tick(self, target_fps=60):
		self.clock.tick(target_fps)

	def width(self):
		return self.sc.get_width()

	def height(self):
		return self.sc.get_height()

	def size(self):
		return Vec2(self.sc.get_size())

	def fps(self):
		return max(min(self.clock.get_fps(), 1000), 0.1)

	def delta(self):
		return self.fps()**(-1)


class Font:
	def __init__(self, typ, size, fam):
		if typ == FILE:
			self.sdl_font = font.Font(fam, size)
		if typ == SYSTEM:
			f = None
			for fx in fam:
				if fx in font.get_fonts():
					f = fx
					break
			self.sdl_font = font.SysFont(f, size)

	def render(self, text, color):
		return self.sdl_font.render(text,1,color)

	def get_em(self):
		return self.sdl_font.get_height()

	def width(self):
		return self.get_width()

	def height(self):
		return self.get_height()

	def size(self):
		return Vec2(self.get_size())


class Texture(Surface):
	...
