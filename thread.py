from multiprocessing import Process
from threading import Thread


def thread(fn):
	def proc(*a, **k):
		p = Process(target=fn, args=a, kwargs=k)
		# p.daemon = True
		p.start()
		return p
	return proc


def daemon_thread(fn):
	def proc(*a, **k):
		p = Process(target=fn, args=a, kwargs=k)
		p.daemon = True
		p.start()
		return p
	return proc

def thread_t(fn):
	def proc(*a, **k):
		p = Thread(target=fn, args=a, kwargs=k)
		# p.daemon = True
		p.start()
		return p
	return proc


def daemon_thread_t(fn):
	def proc(*a, **k):
		p = Thread(target=fn, args=a, kwargs=k)
		p.daemon = True
		p.start()
		return p
	return proc
