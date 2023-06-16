from multiprocessing import Process
from threading import Thread
import os
import sys


class ThreadPool:
	def __init__(self, fn):
		self.fn = self.wrap(fn)
	
	def exec(self, args):
		self.procs = []
		self.rets = list(None for i in args)

		for n, a in enumerate(args):
			self.procs.append(self.fn(self.rets, n, args))
		
		for p in self.procs:
			p.join()
		
		return self.rets

	def wrap(self, fn):
		@thread
		def wrapper(arr, ind, arg):
			arr[ind] = fn(*arg)
		return wrapper


class SingleArgThreadPool:
	def __init__(self, fn):
		self.fn = self.wrap(fn)
	
	def exec(self, args):
		self.procs = []
		self.rets = list(None for i in args)

		# print("ARGS",args)

		for n, a in enumerate(args):
			self.procs.append(self.fn(self.rets, n, a))
		
		for p in self.procs:
			p.join()
		
		return self.rets

	def wrap(self, fn):
		@thread
		def wrapper(arr, ind, arg):
			arr[ind] = fn(arg)
		return wrapper


class InitThreadPool:
	def __init__(self, cl):
		self.cl = self.wrap(cl)
	
	def exec(self, args):
		self.procs = []
		self.rets: dict[int,object] = {}

		for n, a in enumerate(args):
			self.procs.append(self.cl(self.rets, n, a))
		
		for p in self.procs:
			p.join()
		
		return self.rets

	def wrap(self, cl):
		@thread
		def wrapper(arr, ind, arg):
			arr[ind] = cl(*arg)
		return wrapper


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
