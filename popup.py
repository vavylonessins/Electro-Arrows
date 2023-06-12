from pygame import *
import sys
import os
import use8


HEIGHT = 128
MARGIN = 32

_fp, typ, title, desc, extra = sys.argv
typ, title, desc, extra = use8.decode(typ), use8.decode(title), \
	use8.decode(desc), use8.decode(extra)

if typ == "1":
	display.set_mode((1,1))
	font.init()
	fnt = font.SysFont(None, 28)
	icon = transform.smoothscale(image.load("images/error_icon.png"), (HEIGHT/2, HEIGHT/2))
	icon_pos = Vector2(HEIGHT/4, HEIGHT/4)
	text = fnt.render(desc,1,(0,0,0))
	display.quit()
	display.set_caption(title)
	display.set_icon(icon)
	size = Vector2(HEIGHT+text.get_width()+MARGIN, HEIGHT)
	text_pos = Vector2(HEIGHT,HEIGHT/2-text.get_height()/2)
	sc = display.set_mode((int(size.x), int(size.y)))
	run = 1
	clock = time.Clock()
	while run:
		clock.tick(30)
		for e in event.get():
			if e.type == QUIT:
				run = 0
		sc.fill((255,255,255))
		sc.blit(icon, icon_pos)
		sc.blit(text, text_pos)
		display.flip()
	sys.exit()

if typ == "2":
	display.set_mode((1,1))
	font.init()
	fnt = font.SysFont(None, 28)
	icon = transform.smoothscale(image.load("images/error_icon.png"), (HEIGHT/2, HEIGHT/2))
	icon_pos = Vector2(HEIGHT/4, HEIGHT/4)
	text = fnt.render(desc,1,(0,0,0))
	display.quit()
	display.set_caption(title)
	display.set_icon(icon)
	size = Vector2(HEIGHT+text.get_width()+MARGIN, HEIGHT)
	text_pos = Vector2(HEIGHT,HEIGHT/2-text.get_height()/2)
	sc = display.set_mode((int(size.x), int(size.y)))
	run = 1
	clock = time.Clock()
	while run:
		clock.tick(30)
		for e in event.get():
			if e.type == QUIT:
				run = 0
		sc.fill((255,255,255))
		sc.blit(icon, icon_pos)
		sc.blit(text, text_pos)
		display.flip()
	sys.exit()
