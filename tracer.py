import time


_trace_time = 0
_trace_delta = 0

def traceon():
	global _trace_time
	_trace_time = time.time()


def traceoff():
	global _trace_delta
	_trace_delta = time.time() - _trace_time


def get_trace():
	return _trace_delta
