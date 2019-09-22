#!/usr/bin/env python
# autor: Ni Qingliang
# NOTE: this script can be used to sync yocto repository which is accessed through
#       http
import operator
import time
import datetime
import re
import os
import tempfile
import subprocess
from multiprocessing import Queue
import threading
#from threading import Thread

#from bs4 import BeautifulSoup
from subprocess import call
import fileinput
import urllib.parse

g_splitReg = re.compile("^<a href=\"([^>\"]+)\">[^</]+</a> +([^ ]+) ([^ ]+) +([1-9][0-9]*)$")
g_list_file = "files.lst"
g_html_file = "index.html"
g_loc_dir = './sources.yoctoproject/'
g_new_dir = './sources.new/'
g_deprecated_dir = "./sources.deprecated/"
g_thread_number = 10

# the `-N' option can make wget overwrite the old file
def g_download(rem_file, loc_dir):
	#call("wget -e robots=off -N --timeout=10 --wait=10 --tries=0 --progress=bar -P " + loc_dir + " " + rem_file, shell=True)
	cmd = "axel " \
		+ "-n " + "32" + " " \
		+ "-a -v " \
		+ "-U " + "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15'" + " " \
		+ "-o '" + loc_dir + "' " \
		+ rem_file
	#print(cmd)
	call(cmd, shell=True)

# https://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
def natural_sorted(iterable, key=None, reverse=False):
    """Return a new naturally sorted list from the items in *iterable*.

    The returned list is in natural sort order. The string is ordered
    lexicographically (using the Unicode code point number to order individual
    characters), except that multi-digit numbers are ordered as a single
    character.

    Has two optional arguments which must be specified as keyword arguments.

    *key* specifies a function of one argument that is used to extract a
    comparison key from each list element: ``key=str.lower``.  The default value
    is ``None`` (compare the elements directly).

    *reverse* is a boolean value.  If set to ``True``, then the list elements are
    sorted as if each comparison were reversed.

    The :func:`natural_sorted` function is guaranteed to be stable. A sort is
    stable if it guarantees not to change the relative order of elements that
    compare equal --- this is helpful for sorting in multiple passes (for
    example, sort by department, then by salary grade).
    """
    prog = re.compile(r"(\d+)")

    def alphanum_key(element):
        """Split given key in list of strings and digits"""
        return [int(c) if c.isdigit() else c for c in prog.split(element[0])]

    return sorted(iterable, key=alphanum_key, reverse=reverse)

class creg_file:
	def __init__(self, parent, fname, fsize, ftime):
		self._parent = parent
		self._name = fname
		self._size = fsize
		self._time = ftime
		self._need = False
	def set_need(self, isNeed):
		self._need = isNeed
	def get_need(self):
		return self._need

	def need_dl(self):
		if not self.get_need():
			return False
		file_path = self._parent.loc_dir() + self._name
		
		if os.path.exists(file_path + ".st"):
			os.remove(file_path)
			os.remove(file_path + ".st")
		if os.path.exists(file_path):
			statinfo = os.stat(file_path)
			if (statinfo.st_size == self._size) and (time.gmtime(statinfo.st_mtime) >= self._time):
				return False
			#print("need dl " + self._name)
			#print("local size: ")
			#print(statinfo.st_size)
			#print("remote size: ")
			#print(self._size)
			#print(statinfo.st_size == self._size)
			#print("local time: ")
			#print(time.gmtime(statinfo.st_mtime))
			#print("remote time: ")
			#print(self._time)
			#print(time.gmtime(statinfo.st_mtime) >= self._time)
		return True
	def download(self):
		if self.need_dl():
			#print("downloading {}".format(self._name))
			g_download(self._parent.main_page() + self._name, self._parent.loc_dir())
		#else:
		#	print("{:<50} skip".format(self._name))
		return

	def name(self):
		return self._name

class csub_rep:
	def __genlist(self):
		fp = open(g_html_file)

		for cnt, line in enumerate(fp):
			splitR = g_splitReg.match(line)
			if not splitR:
				continue
			#for i in [1, 2, 3, 4]:
			#	print("{}: {}".format(i, splitR.group(i)))

			file_name = urllib.parse.unquote(splitR.group(1))
			if re.match(".*bad-checksum.*", file_name):
				continue
			if re.match("^git2_tmp.*", file_name):
				continue
			file_size = int(splitR.group(4))
			file_time = time.strptime(splitR.group(2) + " " + splitR.group(3), "%d-%b-%Y %H:%M")

			self._full_fl[file_name] = creg_file(self, file_name, file_size, file_time)
	def __init__(self, base_url, loc_dir):
		self._main_page = base_url
		self._loc_dir = loc_dir

		self._full_fl = {}
		self.__genlist()

		# remove files non't need dl in non-regular list
		with fileinput.input(files=(g_list_file)) as f:
			for line in f:
				m = re.match("([+-])(.*)", line)
				if m:
					if m.group(1) == "+" and m.group(2) in self._full_fl:
						self._full_fl[m.group(2)].set_need(True)

		self._dl_fl = {}
		for (k,v) in natural_sorted(self._full_fl.items()):
			if v.need_dl():
				self._dl_fl[k] = v

		# create locale directory
		if not os.path.exists(self._loc_dir):
			os.makedirs(self._loc_dir)

	def loc_dir(self):
		return self._loc_dir
	def main_page(self):
		return self._main_page

	def download(self):
		self._queue = Queue(len(self._dl_fl))
		for (k, v) in natural_sorted(self._dl_fl.items()):
			self._queue.put(self.main_page() + k)
			#g_download(fl, self.loc_dir())
		self._locker = threading.Lock()

		return
	def run(self, threadName):
		while True:
			self._locker.acquire()
			if not self._queue.empty():
				data = self._queue.get()
				self._locker.release()
				print("thread {} processing {}".format(threadName, data))
				g_download(data, self.loc_dir())
			else:
				self._locker.release()
				break
			time.sleep(1)
	def save(self):
		with open(g_list_file + ".new", 'w') as f:
			for (k, v) in natural_sorted(self._full_fl.items()):
				f.write("{}{}\n".format(("+" if v.get_need() else "-"), k))

	def rm_old_files(self):
		cur_files = os.listdir(self._loc_dir)
		for i in cur_files:
			if (not (i in self._full_fl)) or (not self._full_fl[i].get_need()):
				#print("mving " + i)
				print("mv " + self._loc_dir + i + " " + g_deprecated_dir)
				call("mv " + self._loc_dir + i + " " + g_deprecated_dir, shell=True)
				#os.remove(self._loc_dir + i)

		return

if __name__ == '__main__':
	base_url = 'http://downloads.yoctoproject.org/mirror/sources/'
	#call("wget --progress=bar -O " + g_html_file + " " + base_url, shell=True)
	test = csub_rep(base_url, g_loc_dir)
	test.download()

	threadList = []
	for i in range(0, g_thread_number):
		tmp = threading.Thread(target = test.run, args = [i])
		tmp.start()
		threadList.append(tmp)
	for i in range(0, g_thread_number):
		threadList[i].join()
	test.save()
	test.rm_old_files()
	call("rm ./sources/*; find sources.yoctoproject/ sources.custom/ -type f -exec ln -sf ../{} ./sources/ \\;", shell=True)
