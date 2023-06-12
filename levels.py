import os
import extui


levels_json_template = """{
	"content-type": "text/json",
	"purpose": "Config file storing levels data",
	"content": []
}
"""


def btoi(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result


def itob(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result


class LevelManager:
	def __init__(self):
		pass

	def load(self):
		if "levels.json" not in os.listdir():
			extui.popup(extui.POPUP_ERROR, "System File Error",
			"Error: System file \"levels.json\" was removed or corrupted. It will be replaced.", exit=0)
			with open("levels.json", "wt") as f:
				f.write(levels_json_template)
		with open("levels.json", "rt") as f:
			self.json = eval(f.read())

	def parse(self):
		if self.json["content-type"] != "text/json":
			extui.popup(extui.POPUP_ERROR, "Config Error", "Error: file \"levels.json\" not a json file")
		ret = []
		for i in self.json["content"]:
			ret.append(Level(self, i))
		return ret.copy()


class Level:
	def __init__(self, lvlmgr, path):
		with open(path, "rb") as f:
			self.raw = f.read()
		self.lvlmgr = lvlmgr
