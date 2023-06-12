## Utf-8 escape-Safe Encoding ##


def encode(text, coding='utf-8'):
	text = text.encode(coding)
	ret = ""
	for c in text:
		ret += "%"+hex(c).removeprefix('0x').upper()
	return ret


def decode(text, coding='utf-8'):
	ret = b""

	for h in text.split("%"):
		if not h:
			continue
		ret += int('0x'+h,16).to_bytes(1,'little')

	return ret.decode(coding)


if __name__ == "__main__":
	try:
		while 1:
			inp = input("man> ")
			cmd = inp[0]
			dat = inp[1:]
			if cmd == "e":
				print("use> "+encode(dat))
			elif cmd == "d":
				print("use> "+decode(dat))
			else:
				print("ERR> please write: [ed].+\n")
	except: pass
