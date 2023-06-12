"""
Привет, Стрелочник!
Надеюсь, ты будешь поддерживать мой формат файлов.
По факту, твоя задача просто сделать этот же код,
только на своём языке. Это нужно для совместимости
между разными фанатскими версиями стрелочек.

Надеюсь на содействие.
"""


# Из нестандартных модулей python 3 только use8,
# моя разработка В)
from datetime import datetime
import os, sys, use8, random


# это мне было лень вспоминать библиотеку uuid
hex_letters = "0123456789ABCDEF"

# Это чтобы можно было определить, для какой версии
# предназначена карта.
versions = (
	"Original Arrows by Onigiri",
	"Electro Arrows by Talisman",
	"Fan Arrows by Kala Ma"
)

"""
Эта ф-ия позволяет создать файл для карты. Тут все просто
"""
def create_level(name, path, firstrun=True, chunk_amount=0, arrows_version=b'\x01', chunks_binary=b''):
	# name - str, 96 bytes
	name = use8.encode(name[:32]+(" "*(32-len(name[:32])))).encode('utf-8')

	# firstrun - bool, 1 byte
	firstrun = b'\x01'

	# creation date and time - str, 78 bytes
	creation_datetime = use8.encode(str(datetime.now())).encode('utf-8')

	# convert integer to binary
	chunk_amount = chunk_amount.to_bytes(8,'little',signed=False)

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

	name = use8.decode(raw[:96].decode('utf-8'))
	raw = raw[96:]
	firstrun = bool(raw[0])
	raw = raw[1:]
	creation_datetime = use8.decode(raw[:78].decode('utf-8'))
	raw = raw[78:]
	chunk_amount = int.from_bytes(raw[:8], 'little', signed=False)
	raw = raw[8:]
	verid = raw[0]
	raw = raw[1:]
	chunks = raw[72:]
	return name, firstrun, creation_datetime, chunk_amount, verid, chunks


###    ДАЛЬШЕ ТОЛЬКО ПРИМИТИВНЫЙ CLI РЕДАКТОР КАРТ, ТЕБЕ ОН НЕ ОЧЕНЬ ИНТЕРЕСЕН    ###


def red_response():
	path = input('path?> ')
	name, firstrun, creation_datetime, chunk_amount, verid, chunks = read_level(path)
	print(f"Name: {name}")
	print(f"Firstrun: {firstrun}")
	print(f"Creation date and time: {creation_datetime}")
	print(f"Arrows verrsion: {versions[verid]}")
	print(f"Chunks amount: {chunk_amount}")
	print(f"Chunks binary data: {use8.encode(chunks.decode('utf-8')).replace('%','')}")


def new_response():
	random_name = ""
	for i in range(32):
		random_name += random.choice(hex_letters)
	name = input('name?> ')
	path = './levels/%s.arrows' % random_name
	print('Path:',path)
	print('Name:',name)
	ok = input('Ok[Y/n/exit]?> ')
	if ok == 'exit':
		return
	if ok == 'n':
		print('Let\'s try again.')
		new_response()
		return
	create_level(name, path)


if __name__ == "__main__":
	run = 1
	while run:
		cmd = input('> ')
		if cmd == 'exit':
			run = 0
			continue
		if cmd == 'new':
			new_response()
		if cmd == 'red':
			red_response()
