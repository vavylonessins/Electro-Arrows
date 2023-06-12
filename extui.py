import os, sys
from base64 import b16encode
import use8


def popup(typ, title, text, extra="None", exit=1):
	os.system(sys.executable+" popup.py "+use8.encode(typ)+" "+
		use8.encode(title)+" "+use8.encode(text)+" "+use8.encode(extra))
	if typ==POPUP_ERROR and exit:
		sys.exit()


POPUP_ERROR = "1"
POPUP_INFO = "2"
POPUP_WARNING = "3"
POPUP_IMAGE = "4"
