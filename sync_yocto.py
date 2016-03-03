#!/usr/bin/env python
# autor: Ni Qingliang
# NOTE: this script can be used to sync yocto repository which is accessed through
#       http
import time
import datetime
import re
import os
import tempfile
import subprocess

from bs4 import BeautifulSoup
from subprocess import call
import fileinput

# the `-N' option can make wget overwrite the old file
def g_download(rem_file, loc_dir):
	call("wget -N --timeout=10 --wait=10 --tries=0 --progress=bar -P " + loc_dir + " " + rem_file, shell=True)

class creg_file:
	def __init__(self, parent, name, isregular):
		self._parent = parent
		self._name = name
		self._isregular = isregular

	def need_dl(self):
		file_path = self._parent.loc_dir() + self._name
		if os.path.exists(file_path):
			if self._isregular:
				return False
			else:
				file_header_info = subprocess.check_output(["wget","--spider", self._parent.main_page() + self._name], stderr=subprocess.STDOUT, universal_newlines=True)
				obj_size = re.sub(r'.*\nLength: ([0-9]+) \(.*', r'\1', file_header_info, flags=re.DOTALL)
				# TODO: maybe we should use strict comparision, here just compare the size
				if os.path.getsize(file_path) == (int)(obj_size):
					return False
		return True
	def download(self):
		if self.need_dl():
			g_download(self._parent.main_page() + self._name, self._parent.loc_dir())
		else:
			print("{:<50} skip".format(self._name))
		return

	def name(self):
		return self._name

class csub_rep:
	def __init__(self, base_url, loc_dir):
		self._main_page = base_url
		self._fl_non_regular = {}
		self._fl_regular = {}
		self._fl_dl = {}
		self._fl_ordered = []
		self._loc_dir = loc_dir
		# get index
		call("wget --progress=bar -O " + "index.html" + " " + base_url, shell=True)
		soup = BeautifulSoup(open("index.html"), "html.parser")
		#print(soup.prettify())
		prev_file = None
		prev_pkg_name = ""
		prev_pkg_ver = ""
		for link in soup.find_all("a"):
			#print(link["href"])
			file_name = link["href"].strip()
			#directory
			if re.match(".*/$", file_name):
				continue
			#done file
			if re.match(".*\.done$", file_name):
				continue
			if re.match(".*\.lock$", file_name):
				continue
			if re.match(".*bad-checksum.*", file_name):
				continue

			# parse
			self._fl_ordered.append(file_name)
			if re.match(r"^.*"
				"(_\.svn|\.trunk|svn\.)"
				".*$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, False)
				continue
			if re.match(r"^git[2]?_.*$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, False)
				continue
			if re.match(r"^.*\.patch$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, True)
				continue
			m = re.match(r"^(?P<pkgname>.*)"
				"(-|_|-s|\.v)"
				"(?P<pkgver>(([0-9]+\.)+[0-9]+)|(([0-9]+_)+[0-9]+))"
				"(?P<stage>-P[0-9]+|p[0-9]+|[a-z]|alpha|-?beta[0-9]*|-?rc[0-9]+|-pre[0-9]+)?"
				"(?P<revision>-[0-9]+)?"
				"\."
				"(?P<ext>tar\.bz2|tar\.gz|tar\.xz|tgz|zip|gz|bz2)"
				"$", file_name)
			if not m:
				self._fl_non_regular[file_name] = creg_file(self, file_name, True)
				continue

			# regular file
			self._fl_regular[file_name] = None
			pkgname = m.group("pkgname")
			pkgver = m.group("pkgver")
			if pkgname != prev_pkg_name: # different pkg
				if prev_file:
					#print(prev_pkg_name, prev_pkg_ver)
					self._fl_regular[prev_file.name()] = prev_file
				# update prev
				prev_pkg_name = pkgname
				prev_pkg_ver = pkgver
				prev_file = creg_file(self, file_name, True)

			else: # same pkg
				if prev_pkg_ver == pkgver:
					None
				else:
					prev_ver_array = re.split('[\._]', prev_pkg_ver)
					ver_array = re.split('[\._]', pkgver)
					for i,j in zip(prev_ver_array, ver_array):
						pn = int(i)
						cn = int(j)
						if pn == cn:
							continue
						if pn < cn:
							prev_pkg_ver = pkgver
							prev_file = creg_file(self, file_name, True)
						break
		# the final one
		if prev_file:
			self._fl_regular[prev_file.name()] = prev_file
		# remove files non't need dl in non-regular list
		with fileinput.input(files=("yocto-nrfl-with-flag.lst")) as f:
			for line in f:
				m = re.match(r"^#(?P<file_name>.*)$", line)
				if m:
					self._fl_non_regular[m.group("file_name")] = None
		# generate download list
		for (k, v) in self._fl_non_regular.items():
			if v:
				self._fl_dl[k] = v
		for (k, v) in self._fl_regular.items():
			if v:
				self._fl_dl[k] = v
		# generate new non-regular-with-flag.lst
		with open("yocto-nrfl-with-flag.lst.new", 'w') as f:
			for k in self._fl_ordered:
				if k not in self._fl_non_regular:
					continue
				f.write("{}{}".format("" if self._fl_non_regular[k] else "#", k))
				f.write("\n")

		# create locale directory
		if not os.path.exists(self._loc_dir):
			os.makedirs(self._loc_dir)
	def main_page(self):
		return self._main_page

	def loc_dir(self):
		return self._loc_dir

	def download(self):
		#for k in self._fl_ordered:
		#	print("{}{}".format("" if k in self._fl_dl else "#", k))
		for (k, v) in sorted(self._fl_dl.items()):
			v.download()

		return

	def rm_old_files(self):
		cur_files = os.listdir(self._loc_dir)
		set_cur = set()
		for i in cur_files:
			set_cur.add(i)
		set_repo = set()
		for (k, v) in self._fl_dl.items():
			set_repo.add(v.name())

		set_del = set_cur - set_repo
		for i in set_del:
			print("rming {}".format(i))
			os.remove(self._loc_dir + i)

		return

if __name__ == '__main__':
	base_url = 'http://downloads.yoctoproject.org/mirror/sources/'
	loc_dir = './sources.yoctoproject/'
	test = csub_rep(base_url, loc_dir)
	test.download()
	#test.rm_old_files()
	call("rm ./sources/*; find sources.yoctoproject/ sources.custom/ -type f -exec ln -sf ../{} ./sources/ \\;", shell=True)
