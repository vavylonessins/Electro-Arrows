import time


_trace_time = 0
_trace_delta = 0

def on():
	global _trace_time
	_trace_time = time.time()


def off():
	global _trace_delta
	_trace_delta = time.time() - _trace_time


def get():
	return _trace_delta
