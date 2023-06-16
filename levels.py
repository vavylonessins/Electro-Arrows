## Привет, Стрелочник!
## Надеюсь, ты будешь поддерживать мой формат файлов.
## По факту, твоя задача просто сделать этот же код,
## только на своём языке. Это нужно для совместимости
## между разными фанатскими версиями стрелочек.
##
## Надеюсь на содействие.


from hacks import *
from gui import *
from const import *
from funcs import *
from thread import *
import datetime
import sys	
import random
import os
import extui
import pprint
import time as pytime


# Это чтобы можно было определить, для какой версии
# предназначена карта.
versions: tuple[str] = (
	"«Стрелочки» - Онигири",
	"«Электро-стрелки» - Талисман",
	"«Стрелочки» - Kala ma",
	"«Стрелочки» - Дикий Опездал",
	"«Стрелка» - Zve1223",
	"«Cunijaji» - Mr. Ybs"

)


block___init__ = 0
layer___init__ = 0
chunk___init__ = 0


class Block:

	def __init__(self, layer, raw):

		global block___init__
		block___init__ += 1
		layer.chunk.level.blocks_amount += 1

		self.package = raw[0]
		self.package_name = layer.chunk.level.mods[raw[0]]
		self.type = raw[1]
		self.state = btoi(raw[2:])

		#print("Block.__init__(*) #"+str(block___init__))
		#print("pkg:",self.package)
		#print("type:",self.type)
		#print("state:",self.state)
		#print()
	
	def compile(self):
		return itob(self.package, 1)+itob(self.type, 1)+itob(self.state, 2)


class Layer:

	def __init__(self, chunk, data: bytes):

		global layer___init__
		layer___init__ += 1
		chunk.level.layers_amount += 1

		self.chunk = chunk
		self.blocks = []

		tpool = InitThreadPool(Block)
		tpool.exec(zip((self for i in range(64)), chunks(data, 64)))

		self.blocks = list(tpool.rets).copy()

		#print("\nLayer.__init__(*) #"+str(layer___init__))
		#print("pkg:",pprint.pformat(self.data))
		#print()
	
	def get_at(self, x: int, y: int):
		return self.blocks[y*8+x]

	def compile(self):

		ret = b''

		print("BLOCKS", self.blocks)
		for b in self.blocks:
			ret += b.compile()
		
		# print("AAA", repr(ret))
		return ret


class Chunk:

	def __init__(self, level, raw=False):

		global chunk___init__
		chunk___init__ += 1

		self.level = level
		self.raw = raw

		self.x = 0
		self.y = 0
		self.flags = 0
		self.height = 1

		#print("\n\nChunk.__init__(*) #"+str(chunk___init__))
		#print("pkg:",self.package)
		#print("type:",self.type)
		#print("state:",self.state)
		#print()
	
	def compile(self):

		ret = b''

		ret += itob(self.x, 8)
		ret += itob(self.y, 8)
		ret += itob(self.flags, 1)
		ret += itob(self.height, 1)

		#for l in self.layers:
		#	ret += l.compile()
		## Let's parallel!

		tpool = SingleArgThreadPool(lambda layer: (print(layer), layer.compile()[1]))
		tpool.exec(self.layers)

		ret += b''.join(tuple(tpool.rets))
		
		return ret

	
	def generate(self):
		# print("PANIC HERE", [b for b in chunks((b'\x00\x00\x00\x00'*64*self.height), 64*4)])
		self.layers = [Layer(self, b) for b in chunks((b'\x00\x00\x00\x00'*64*self.height), 64*4)]

	def init(self):

		if not self.raw:
			self.generate()
			return

		self.x = btoi(self.raw[:8])
		self.raw = self.raw[8:]

		self.y = btoi(self.raw[:8])
		self.raw = self.raw[8:]

		self.flags = btoi(self.raw[:1])
		self.raw = self.raw[1:]

		self.height = btoi(self.raw[:1])
		self.raw = self.raw[1:]

		self.layers = list(Layer(self, lay) for lay in chunks(self.raw, 256))
	
	def print_format(self):
		text = "Chunk at {"+str(self.x)+"; "+str(self.y)+"}:\n"
		for l in self.layers:
			lines = chunks(l.compile(), 32)
			text += "\n       "
			for block in chunks(lines, 4):
				text += " "+repr(block).upper()
		text += '\n\n'
		
		print(text)
	
	def get_at(self, x, y, z=0):
		return self.layers[z].get_at(x, y)


class LevelManager:

	def __init__(self):
		pass

	def load(self):

		self.levels = list("./levels/"+p for p in os.listdir('./levels'))

	def add(self, path: str|os.PathLike):

		self.levels.append(path)
	
	def as_dict(self):

		self.load()
		ret = {}

		for path in self.levels:

			level = Level(self, path)
			level.read()

			ret[level.name] = level
		
		return ret
	
	def as_tuple(self):

		self.load()
		ret = ()

		for path in self.levels:

			level = Level(self, path)
			level.read()

			ret = ret + (level,)
		
		return ret


class Level:

	chunks: list[Chunk]

	def __init__(self, lvlmgr: LevelManager, path: str|os.PathLike):
		
		self.lvlmgr = lvlmgr
		self.path = path

		self.layers_amount = 0
		self.blocks_amount = 0
	
	def init(self):

		with open(self.path, "rb") as f:
			self.raw = f.read()

		self.read()
		self.parse_chunks()
	
	def get_at(self, x, y, z=0):

		cx = x // 8
		rx = x - cx

		cy = y // 8
		ry = y - cy

		return self.get_chunk(cx, cy).get_at(rx, ry, z)

	def get_chunk(self, x, y):

		tpool = ThreadPool(lambda x, y, c: c if c.x == x and c.y == y else None)
		tpool.exec(self.chunks)

		while None in tpool.rets:
			tpool.rets.remove(None)
		
		if not tpool.rets:

			self.init_chunk(x, y)
			return self.chunks[-1]

		return tpool.rets[0]

	def init_chunk(self, x, y, z=1):

		self.chunks.append(Chunk(self))

		self.chunks[-1].x = x
		self.chunks[-1].y = y
		self.chunks[-1].height = z

		self.chunks[-1].generate()
	
	def read(self):

		with open(self.path, "rb") as f:
			raw = f.read()
		
		assert btoi(raw[:8]) == 0x303153574f525241
		raw = raw[8:]

		self.name = raw.split(b'\x00')[0].decode()
		raw = raw.split(b'\x00', 1)[1]

		self.crdt = str(datetime.datetime.fromtimestamp(int.from_bytes(raw[:8], 'little')))
		raw = raw[8:]

		self.flags = raw[0]
		raw = raw[1:]

		self.ver_id = raw[0]
		raw = raw[1:]

		mods, raw = raw.split(b'\x00\x00', 1)
		mods = mods.split(b'\x00')
		self.mods = list(i.decode() for i in mods)

		self.chunks = raw
	
	def print_format(self):

		text = f"Level \"{self.name}\":\n"
		text += f"    Creation time: {self.crdt}\n"
		text += f"    3D Support: {'Yes' if self.flags & 1 else 'No'}\n"
		text += f"    Game version of creator: {versions[self.ver_id]}\n"
		text += f"    Chunks amount: {len(self.chunks)}\n"
		text += f"    Layers amount: {self.layers_amount}\n"
		text += f"    Blocks amount: {self.blocks_amount}\n"
		text += f"\n    Installed mods:\n"

		for m in self.mods:
			text += "        "+m+"\n"

		print(text)
	
	def write(self):

		raw = itob(0x303153574f525241, 8)

		raw += self.name.encode()+b'\x00'

		raw += itob(int(pytime.mktime(datetime.datetime.now().timetuple())), 8)

		raw += itob(int(self.flags), 1)
		raw += itob(self.ver_id, 1)
		
		mods: bytes = b''

		for m in self.mods:
			mods += m.encode()+b'\x00'
		
		raw += mods+b'\x00'

		raw += self.compile_chunks()

		with open(self.path, "wb") as f:
			f.write(raw)
	
	def compile_chunks(self):

		ret = b''

		for c in self.chunks:
			ret += c.compile()
		
		return ret

	def parse_chunks(self):


		if not self.chunks:

			self.chunks = []
			return

		raw = self.chunks

		self.chunks = []

		run = 1
		ptr = 0

		while run:
			try:
				if not raw[ptr:]:
					break
				chunk = Chunk(self, raw[ptr:])
				chunk.init()
				size = 10 + chunk.height*256
				chunk.content = raw[ptr+10:][:chunk.height*256]
				self.chunks.append(chunk)
				ptr += size
			except IndexError:
				break
