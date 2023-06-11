## importing 'gui' library

from gui import *
import gui


## constants
# colors
BACK = Color(43, 43, 43)
MIDDLE = Color(53, 53, 53)
ACCENT = Color(106, 214, 218)
MAIN = Color(255, 255, 255)
SKETCH = Color(0, 0, 0)

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


# important textures setup
author_logo = onigiri_logo = gui.smoothscale(gui.image.load("images/slowman.png"), (128, 128))
talisman_logo = gui.smoothscale(gui.image.load("images/fastman.png"), (128, 128))
title_texture = title_font.render("Электро-стрелки",ACCENT).convert_alpha()
menu_texture = gui.Texture((window.width()/3,MARGIN*10+main_em*4)).convert()
menu_texture.fill(BACK)
gui.draw.rect(menu_texture,MIDDLE,(0,0,*menu_texture.get_size()),0,EDGE_RADIUS)
gui.draw.rect(menu_texture,SKETCH,(0,0,*menu_texture.get_size()),1,EDGE_RADIUS)
menu_texture.blit(main_font.render("Играть",MAIN), gui._calc_pos(menu_texture,main_font.render("Играть",MAIN),Vec2(0,MARGIN*2),"ct"))
menu_texture.blit(main_font.render("Настройки",MAIN), gui._calc_pos(menu_texture,main_font.render("Настройки",MAIN),Vec2(0,MARGIN*4+main_em),"ct"))
menu_texture.blit(main_font.render("О авторе",MAIN), gui._calc_pos(menu_texture,main_font.render("О авторе",MAIN),Vec2(0,MARGIN*6+main_em*2),"ct"))
menu_texture.blit(main_font.render("Выход",MAIN), gui._calc_pos(menu_texture,main_font.render("Выход",MAIN),Vec2(0,MARGIN*8+main_em*3),"ct"))


## mainloop
while window.is_running():
	## events
	for event in window.get_new_events():
		# QUIT
		if event.type == gui.QUIT:
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
			if timer < 255:
				author_logo.set_alpha(int(timer))
				timer += window.delta()*255
			else:
				subscreen = "logo-on"
				timer = 0

		# just delay
		if subscreen == "logo-on":
			if timer < 1:
				timer += window.delta()
			else:
				subscreen = "logo-out"
				timer = 255

		# hiding logo
		if subscreen == "logo-out":
			# distortion out
			if timer > 0:
				author_logo.set_alpha(int(timer))
				timer -= window.delta()*255
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
	if screen == "main-menu":
		window.show(title_texture, align="ct", offset=Vec2(0,MARGIN))
		window.show(menu_texture, align="ct", offset=Vec2(0,MARGIN*4+title_em))
	window.apply()
	window.tick(60)

window.hide()
