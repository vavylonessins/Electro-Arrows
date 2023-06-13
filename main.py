## importing 'gui' library

from gui import *
from effects import *
from const import *
from levels import *
import gui


## constants
# colors
BACK = Color(43, 43, 43)
MIDDLE = Color(53, 53, 53)
ACCENT = Color(106, 214, 218)
MAIN = Color(255, 255, 255)
SKETCH = Color(0, 0, 0)
SYSIND = Color(255, 100, 100)

# integers
MARGIN = 8
EDGE_RADIUS = 8

## initialization
gui.init()
window = gui.Window((1280, 720), gui.OPTIMIZE|gui.DOUBLEBUF|gui.RESIZABLE)
title_font = gui.Font(gui.SYSTEM, 64, ("Console", "Droid Sans Mono", "Consolas", "Courier", "Monospace"))
main_font = gui.Font(gui.SYSTEM,32, ("Console", "Droid Sans Mono", "Consolas", "Courier", "Monospace"))
title_em = title_font.get_em()
main_em = main_font.get_em()

## level manager
lvlmgr = LevelManager()


## script. has no code effect.
script = {
	"splash": {
		"main-menu": {
			"levels": {
				"create-level": {
					"game": {
						"pause": {
							"main-menu": {}
						}
					},
				"import": {},
				"export": {}
				}
			}
		}
	}
}

## variables for frame changing
screen = "splash"
subscreen = "startup"
moment = 0
timer = 0
counter = 0

## window setup
window.set_title("")
window.set_icon(gui.image.load("images/icon.png"))
window.show()

## init sth needs window already initialized
main_menu_arrows = ArrowsEffect(window.sc, Color(list(i//2 for i in MAIN[:3])), MAIN_MENU_ARROWS_AMOUNT)

# important textures setup
author_logo = onigiri_logo = gui.smoothscale(gui.image.load("images/slowman.png"), (128, 128))
talisman_logo = gui.smoothscale(gui.image.load("images/fastman.png"), (128, 128))
title_texture = title_font.render("Electro-arrows",ACCENT).convert_alpha()
menu_texture = gui.Texture((window.width()/3,MARGIN*10+main_em*4)).convert()
menu_texture.fill(BACK)
gui.draw.rect(menu_texture,MIDDLE,(0,0,*menu_texture.get_size()),0,EDGE_RADIUS)
gui.draw.rect(menu_texture,SKETCH,(0,0,*menu_texture.get_size()),1,EDGE_RADIUS)
menu_texture.blit(main_font.render("Play",MAIN), gui._calc_pos(menu_texture,main_font.render("Play",MAIN),Vec2(0,MARGIN*2),"ct"))
menu_texture.blit(main_font.render("Settings",MAIN), gui._calc_pos(menu_texture,main_font.render("Settings",MAIN),Vec2(0,MARGIN*4+main_em),"ct"))
menu_texture.blit(main_font.render("About author",MAIN), gui._calc_pos(menu_texture,main_font.render("About the author",MAIN),Vec2(0,MARGIN*6+main_em*2),"ct"))
menu_texture.blit(main_font.render("Quit",MAIN), gui._calc_pos(menu_texture,main_font.render("Quit",MAIN),Vec2(0,MARGIN*8+main_em*3),"ct"))

# hitboxes
main_menu_rect_pos = Vec2(*gui._calc_pos(window.sc, menu_texture, Vec2(0,MARGIN*4+title_em), "ct"))

main_menu_play_pos = gui._calc_pos(menu_texture,main_font.render("Play",MAIN),Vec2(0,MARGIN*2),"ct")
main_menu_play_pos += main_menu_rect_pos
main_menu_play_rect = Rect(*main_menu_play_pos, *main_font.render("Play",MAIN).get_size())

main_menu_settings_pos = gui._calc_pos(menu_texture,main_font.render("Settings",MAIN),Vec2(0,MARGIN*4+main_em),"ct")
main_menu_settings_pos += main_menu_rect_pos
main_menu_settings_rect = Rect(*main_menu_settings_pos, *main_font.render("Settings",MAIN).get_size())

main_menu_about_pos = gui._calc_pos(menu_texture,main_font.render("About the author",MAIN),Vec2(0,MARGIN*6+main_em*2),"ct")
main_menu_about_pos += main_menu_rect_pos
main_menu_about_rect = Rect(*main_menu_about_pos, *main_font.render("About the author",MAIN).get_size())

main_menu_exit_pos = gui._calc_pos(menu_texture,main_font.render("Quit",MAIN),Vec2(0,MARGIN*8+main_em*3),"ct")
main_menu_exit_pos += main_menu_rect_pos
main_menu_exit_rect = Rect(*main_menu_exit_pos, *main_font.render("Quit",MAIN).get_size())


## mainloop
while window.is_running():
	## events
	for event in window.get_new_events():
		# QUIT
		if event.type == gui.QUIT:
			window.close()

		# mouse button release
		if event.type == gui.MOUSEBUTTONUP:
			if main_menu_play_rect.collidepoint(event.pos):
				screen = "levels"
				subscreen = "list"
				timer = 0
				counter = 0
				moment = 0
				lvlmgr.load()
			if main_menu_settings_rect.collidepoint(event.pos):
				screen = "settings"
				subscreen = "list"
				timer = 0
				counter = 0
				moment = 0
			if main_menu_about_rect.collidepoint(event.pos):
				screen = "about"
				subscreen = "list"
				timer = 0
				counter = 0
				moment = 0
			if main_menu_exit_rect.collidepoint(event.pos):
				window.close()

	## draw process
	# background
	window.fill(BACK)

	## screens
	if screen == "splash":
		## splash
		# startup -> instantly into 'onigiri-in'
		if subscreen == "startup":
			subscreen = "logo-in"

		# onigiri-in -> show slowman with distortion 1.0
		if subscreen == "logo-in":
			# distortion in
			if timer < 255*SPLASH_EFFECT_DURATION:
				author_logo.set_alpha(int(timer))
				timer += window.delta()*255/SPLASH_EFFECT_DURATION
			else:
				subscreen = "logo-on"
				timer = 0

		# just delay
		if subscreen == "logo-on":
			if timer < 1*SPLASH_EFFECT_DURATION:
				timer += window.delta()
			else:
				subscreen = "logo-out"
				timer = 255*SPLASH_EFFECT_DURATION

		# hiding logo
		if subscreen == "logo-out":
			# distortion out
			if timer > 0:
				author_logo.set_alpha(int(timer))
				timer -= window.delta()*255/SPLASH_EFFECT_DURATION
			else:
				# next logo?
				if counter == 0:
					subscreen = "logo-in"
					author_logo = talisman_logo
					author_logo.set_alpha(0)
					timer = 0
					counter = 1
				# or next screen?)
				else:
					screen = "main-menu"
					subscreen = "startup"
					counter = 0
					timer = 0
		if subscreen.startswith("logo"):
			window.show(author_logo, align="cc")

	if screen == "levels":
		if subscreen == "list":
			...

	if screen == "main-menu":
		## update part
		main_menu_arrows.update(window.delta())
		## draw part
		main_menu_arrows.draw()
		window.show(title_texture, align="ct", offset=Vec2(0,MARGIN))
		window.show(menu_texture, align="ct", offset=Vec2(0,MARGIN*4+title_em))
		# gui.draw.rect(window.sc, SYSIND, main_menu_play_rect, 1)
		# gui.draw.rect(window.sc, SYSIND, main_menu_settings_rect, 1)
		# gui.draw.rect(window.sc, SYSIND, main_menu_about_rect, 1)
		# gui.draw.rect(window.sc, SYSIND, main_menu_exit_rect, 1)

	window.apply()
	window.tick(60)

window.hide()
