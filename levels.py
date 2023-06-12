"""
Привет, Стрелочник!
Надеюсь, ты будешь поддерживать мой формат файлов.
По факту, твоя задача просто сделать этот же код,
только на своём языке. Это нужно для совместимости
между разными фанатскими версиями стрелочек.

Надеюсь на содействие.
"""


from hacks import *
from datetime import datetime
from base64 import b64encode, b64decode
import sys	
import random
import os
import extui
import pprint


levels_json_template = """{
	"content-type": "text/json",
	"purpose": "Config file storing levels data",
	"content": []
}
"""

LAYERS_MASK = 0b0000111111111111
FLAGS_MASK  = 0b1111000000000000

# это мне было лень вспоминать библиотеку uuid
hex_letters = "0123456789ABCDEF"

# Это чтобы можно было определить, для какой версии
# предназначена карта.
versions = (
	"Original Arrows by Onigiri",
	"Electro Arrows by Talisman",
	"Fan Arrows by Kala Ma"
)


# из байт в число
def btoi(bytes, signed=False):
    result = int.from_bytes(bytes, 'little', signed=signed)
    return result


# из числа в байты
def itob(value, length, signed=False):
    result = value.to_bytes(length, 'little', signed=signed)
    return result


"""
Эта ф-ия позволяет создать файл для карты. Тут все просто
"""
def create_level(name, path, firstrun=True, chunk_amount=0, arrows_version=b'\x01', chunks_binary=b''):
	# name - str, 96 bytes
	name = b64encode((name[:32]+(" "*(32-len(name[:32])))).encode('utf-8'))+b'\x00'

	# firstrun - bool, 1 byte
	firstrun = b'\x01'

	# creation date and time - str, 78 bytes
	creation_datetime = b64encode(str(datetime.now()).encode('utf-8'))+b'\x00'

	# convert integer to binary
	chunk_amount = itob(chunk_amount, 8)

	# version ID
	verid = arrows_version

	# reserved - int576, 72 bytes
	reserved = b'\x00'*72

	# chunks data - complex, dynamic sizeable
	chunks = chunks_binary

	# compiling all into binary
	raw = name+firstrun+creation_datetime+chunk_amount+verid+reserved+chunks

	with open(path, "wb") as f:
		f.write(raw)


"""
Эта ф-ия позволяет читать файл карты
"""
def read_level(path):
	with open(path, "rb") as f:
		raw = f.read()

	name = b64decode(raw.split(b'\x00', 1)[0]).decode('utf-8')
	raw = raw.split(b'\x00', 1)[1]
	firstrun = bool(raw[0])
	raw = raw[1:]
	creation_datetime = b64decode(raw.split(b'\x00', 1)[0]).decode('utf-8')
	raw = raw.split(b'\x00',1)[1]
	chunk_amount = btoi(raw[:8])
	raw = raw[8:]
	verid = raw[0]
	raw = raw[1:]
	chunks = raw[72:]
	return name, firstrun, creation_datetime, chunk_amount, verid, chunks


class LevelManager:
	def __init__(self):
		pass

	def load(self):
		if "levels.spy" not in os.listdir():
			extui.popup(extui.POPUP_ERROR, "System File Error",
			"Error: System file \"levels.spy\" was removed or corrupted. It will be replaced.", exit=0)
			with open("levels.spy", "wt") as f:
				f.write(levels_json_template)
		with open("levels.spy", "rt") as f:
			self.json = eval(f.read())

	def add(self, path):
		self.json["content"].append(path)

	def save(self):
		with open("levels.spy", "wt") as f:
			f.write(pprint.pformat(self.json))

	def parse(self):
		if self.json["content-type"] != "text/json":
			extui.popup(extui.POPUP_ERROR, "Config Error", "Error: file \"levels.spy\" not a json file")
		ret = []
		for i in self.json["content"]:
			ret.append(Level(self, i))
			ret[-1].parse()
		return ret.copy()


class Level:
	def __init__(self, lvlmgr, path):
		with open(path, "rb") as f:
			self.raw = f.read()
		self.lvlmgr = lvlmgr
		self.path = path
		self.chunks: dict[int,dict[int,object]] = VectorDict()

	def parse(self):
		name, firstrun, creation_datetime, chunk_amount, verid, chunks = read_level(self.path)
		self.name = name
		self.new = firstrun
		self.datetime = creation_datetime
		self.version = versions[verid]

	def parse_bins(self):
		raw = self.raw[256:]
		run = 1
		ptr = 0
		while run:
			try:
				size = raw[ptr:][:8]
				self.parse_chunk(raw[ptr:][:size])
				ptr += size
			except IndexError:
				run = 0

	def parse_chunk(self, raw):
		""" формат чанков для электро стрелок '''

		struct chunk_base {
			char my_size;
			bool is_3d;
			int x;
			int y;
			unsigned short int flags_and_layers_num;
			char** layers[];
		}
		"""
		chunk = dataclass(
			my_size = btoi(raw[:8]),
			is_3d = raw[8],
			x = btoi(raw[9:][:4]),
			y = btoi(raw[13:][:4]),
			flags = (raw[17] & FLAGS_MASK) >> 12,
			layers = raw[16:][:2] & LAYERS_MASK,
			content = raw[18:]
		)

		self.chunks.append(chunk)

	def prepare_chunk(self, x, y, h):
		chunk = dataclass(
			my_size = 64*h+145,
			is_3d = 1,
			x = x,
			y = y,
			flags = 0,
			layers = h & LAYERS_MASK,
			content = b'\x00'*64*h
		)

		self.chunks.append(chunk)

	def delete_chunk(self, x, y):
		n = -1
		for c in self.chunks:
			if c.x == x and c.y == y:
				n = self.chunks.index(c)
				break
		if n == -1:
			extui.popup(extui.POPUP_ERROR, "NOT FOUND", f"chunk at ({x}, {y})")
		del self.chunks[n]

	def save(self):
		...


###    ДАЛЬШЕ ТОЛЬКО ПРИМИТИВНЫЙ CLI РЕДАКТОР КАРТ, ТЕБЕ ОН НЕ ОЧЕНЬ ИНТЕРЕСЕН    ###

if __name__ == "__main__":
	lvlmgr = LevelManager()
	lvlmgr.load()

	def red_resp():
		lvlmgr.load()
		levels = lvlmgr.parse()
		for level in levels:
			print(f"* {level.name}")
		name = input('name?> ')
		path = "ERROR"
		for level in levels:
			if level.name.strip() == name:
				path = level.path
				break
		if path == "ERROR":
			print("Not found.")
			return
		name, firstrun, creation_datetime, chunk_amount, verid, chunks = read_level(path)
		print(f"Name: {name}")
		print(f"Firstrun: {firstrun}")
		print(f"Creation date and time: {creation_datetime}")
		print(f"Arrows verrsion: {versions[verid]}")
		print(f"Chunks amount: {chunk_amount}")
		backslash_x = '\\x'
		print(f"Chunks binary data: {repr(chunks).replace(backslash_x,'').upper()}")

	def edi_resp():
		lvlmgr.load()
		levels = lvlmgr.parse()
		print("\n".join(("* "+level.name for level in levels)))
		name = input('name?> ')
		name, firstrun, creation_datetime, chunk_amount, verid, chunks = read_level(path)
		print("""
MENU:
* exit - quit
* prepare-chunk - prepares new chunk
* delete-chunk - deletes chunk
* apply-changes - applies changes
""".strip)
		
		run = 1

		while run:
			if cmd == "exit":
				break
			if cmd == "prepare-chunk":
				if level.new:
					print("This is first chunk? so it automatically will be at (0;0)")
					x = y = 0
				else:
					x = int(input("x?> "))
					y = int(input("y?> "))
				h = max(min(int(input("height?> ")), 4095), 1)
				level.prepare_chunk(x, y, h)
			if cmd == "delete-chunk":
				x = int(input("x?> "))
				y = int(input("y?> "))
				level.delete_chunk(x, y)
			if cmd == "apply-changes":
				level.save()


	def new_resp():
		random_name = ""
		for i in range(32):
			random_name += random.choice(hex_letters)
		name = input('name?> ')
		path = './levels/%s.arrows' % random_name
		print('Path:',path)
		print('Name:',name)
		ok = input('Ok[Y/n/c]?> ')
		if ok == 'c':
			return
		if ok == 'n':
			print('Let\'s try again.')
			new_resp()
			return
		create_level(name, path)
		lvlmgr.add(path)
		lvlmgr.save()


	run = 1
	while run:
		try:
			cmd = input('> ')
			if cmd == 'exit':
				run = 0
				continue
			if cmd == 'new':
				new_resp()
			if cmd == 'red':
				red_resp()
			if cmd == 'edi':
				edi_resp()
		except EOFError:
			print()
			run = 0
		except KeyboardInterrupt:
			print()
			run = 0
