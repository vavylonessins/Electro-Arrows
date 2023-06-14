"""
Привет, Стрелочник!
Надеюсь, ты будешь поддерживать мой формат файлов.
По факту, твоя задача просто сделать этот же код,
только на своём языке. Это нужно для совместимости
между разными фанатскими версиями стрелочек.

Надеюсь на содействие.
"""


from hacks import *
from gui import *
from datetime import datetime
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

# это мне было лень вспоминать библиотеку uuid
hex_letters: str = "0123456789ABCDEF"

# Это чтобы можно было определить, для какой версии
# предназначена карта.
versions: tuple[str] = (
	"«Стрелочки» - Онигири",
	"«Электро-стрелки» - Талисман",
	"«Стрелочки» - Кала Ма",
	"«Стрелочки» - Дикий Опездал",
	"«Стрелка» - Zve1223",
	"«Cunijaji» - Mr. Ybs"

)


# из байт в число
def btoi(bytes: bytes, signed: bool = False) -> int:
    result = int.from_bytes(bytes, 'little', signed=signed)
    return result


# из числа в байты
def itob(value: int, length: int, signed: bool = False) -> bytes:
    result = value.to_bytes(length, 'little', signed=signed)
    return result


"""
Эта ф-ия позволяет создать файл для карты. Тут все просто
"""
def create_level(name: str, path: str|os.PathLike,
				 firstrun: bool = True, is_3d: bool = True,
				 chunk_amount: int = 0, arrows_version: int = 1,
				 chunks_binary: bytes = b'') -> None:
	# name - str, any length
	name: bytes = (name.strip()[:32]+(" "*(32-len(name[:32])))).encode('utf-8')+b'\x00'

	# firstrun - bool, 1 byte
	firstrun: bytes = itob(b'\x00\x01'[int(firstrun)], 1)

	is_3d: bytes = b'\x00\x01'[int(is_3d)]

	# creation date and time - str, any length
	creation_datetime: bytes = str(datetime.now()).encode('utf-8')+b'\x00'

	# convert integer to binary
	chunk_amount: bytes = itob(chunk_amount, 8)

	# version ID
	print(arrows_version)
	verid: bytes = itob(arrows_version, 1)
	print(verid)

	# chunks data - complex, dynamic sizeable
	chunks: bytes = chunks_binary

	# compiling all into binaryb'\x00\x01'[int(firstrun)]
	#print(name,firstrun,creation_datetime,chunk_amount,verid,chunks)
	raw: bytes = name+firstrun+creation_datetime+chunk_amount+verid+chunks

	with open(path, "wb") as f:
		f.write(raw)


"""
Эта ф-ия позволяет читать файл карты
"""
def read_level(path: str|os.PathLike) -> tuple:
	with open(path, "rb") as f:
		raw: bytes = f.read()

	name: str = raw.split(b'\x00', 1)[0].decode('utf-8')
	raw = raw.split(b'\x00', 1)[1]

	firstrun: bool = bool(raw[0])
	raw = raw[1:]

	is_3d: bool = bool(raw[0])
	raw = raw[1:]

	creation_datetime: str = raw.split(b'\x00', 1)[0].decode('utf-8')
	raw = raw.split(b'\x00',1)[1] # ERROR

	chunk_amount: int = btoi(raw[:8])
	raw = raw[8:]

	print("VERID:",raw[0])
	verid: str = versions[raw[0]]
	raw = raw[1:]

	chunks: bytes = raw
	return name, firstrun, is_3d, creation_datetime, chunk_amount, verid, chunks


class Layer:
	def __init__(self, data: bytes):
		self.rows: tuple[bytes] = tuple(data[::8])
	
	def get_at(self, x: int, y: int):
		return self.data[y][x]


class Chunk:
	def __init__(self, x, y, flags: int, layers: int, content: bytes):
		self.x: int = x
		self.y: int = y
		self.flags: int = flags
		self.height: int = layers
		self.layers: tuple[Layer] = (Layer(c) for c in content[::64])
	
	def get_at(self, x: int, y: int, z: int = 0):
		return self.layers[z].get_at(x, y)


class LevelManager:
	def __init__(self):
		pass

	def load(self):
		self.levels = os.listdir('./levels')

	def add(self, path: str|os.PathLike):
		self.levels.append(path)


class Level:
	def __init__(self, lvlmgr: LevelManager, path: str|os.PathLike):
		with open(path, "rb") as f:
			self.raw = f.read()
		self.lvlmgr: LevelManager = lvlmgr
		self.path: str|os.PathLike = path
		self.chunks: list[Chunk] = []

	def parse(self):
		self.name, self.new, self.is_3d, self.datetime, chunk_amount, self.version, self.raw = read_level(self.path)

	def parse_bins(self):
		raw = self.raw
		run = 1
		ptr = 0
		while run:
			try:
				chunk = self.parse_chunk(raw[ptr:])
				size = 10 + chunk.heigh*64
				chunk.content = raw[ptr+10:][:chunk.height*64]
				self.chunks.append(chunk)
				ptr += size
			except IndexError:
				run = 0

	def parse_chunk(self, raw):
		""" формат чанков для электро стрелок '''

		struct chunk_base {
			int32 x;
			int32 y;
			uint8 flags;
			uint8 height;
			char** layers[];
		}
		"""
		chunk = Chunk(
			x = btoi(raw[:4]),
			y = btoi(raw[4:][:4]),
			flags = raw[8],
			layers = raw[9],
			content = b''
		)

		return chunk

	def prepare_chunk(self, x, y, h):
		chunk = Chunk(
			x = x,
			y = y,
			flags = 0,
			layers = h,
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
		levels = lvlmgr.levels
		for level in levels:
			level = Level(lvlmgr, './levels/'+level)
			level.parse()
			print(f"* {level.name}")
		name = input('name?> ')
		path = "ERROR"
		for level in levels:
			level = Level(lvlmgr, './levels/'+level)
			level.parse()
			if level.name.strip() == name:
				path = level.path
				break
		if path == "ERROR":
			print("Not found.")
			return
		name, firstrun, is_3d, creation_datetime, chunk_amount, verid, chunks = read_level(path)
		print(f"Name: {name}")
		print(f"Firstrun: {firstrun}")
		print(f"3D: {is_3d}")
		print(f"Creation date and time: {creation_datetime}")
		print(f"Arrows verrsion: {verid}")
		print(f"Chunks amount: {chunk_amount}")
		backslash_x = '\\x'
		print(f"Chunks binary data: {repr(chunks).replace(backslash_x,'').upper()}")

	def edi_resp():
		lvlmgr.load()
		levels = lvlmgr.levels
		print("\n".join(("* "+level.name for level in levels)))
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
		for i in range(16):
			random_name += random.choice(hex_letters)
		name = input('name?> ')
		firstrun = True
		is_3d = input("3D?> ").strip().lower()[0] == "y"
		verid = max(min(int(input("Version ID?> ")), 5), 0)
		path = './levels/%s.arrows' % random_name
		print()
		print('Path:',path)
		print('\nName:',name)
		ok = input('Ok[Y/n/c]?> ')
		if ok == 'c':
			return
		if ok == 'n':
			print('Let\'s try again.')
			new_resp()
			return
		create_level(name, path, firstrun, is_3d, 0, verid, b'')
		lvlmgr.add(path)


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
