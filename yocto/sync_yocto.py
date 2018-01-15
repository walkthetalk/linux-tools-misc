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

from bs4 import BeautifulSoup
from subprocess import call
import fileinput

# the `-N' option can make wget overwrite the old file
def g_download(rem_file, loc_dir):
	call("wget -e robots=off -N --timeout=10 --wait=10 --tries=0 --progress=bar -P " + loc_dir + " " + rem_file, shell=True)

g_STYLE = 1
g_timefmtlist = [ "%Y-%b-%d %H:%M", "%Y-%b-%d"]
g_timefmt = g_timefmtlist[g_STYLE]

class creg_file:
	def __init__(self, parent, fname, fsize, ftime, isregular):
		self._parent = parent
		self._name = fname
		self._size = fsize
		self._time = ftime
		self._isregular = isregular

	def need_dl(self):
		file_path = self._parent.loc_dir() + self._name
		if os.path.exists(file_path):
			ltime = time.gmtime(os.path.getmtime(file_path))
			print(self._name + " local time: " + time.strftime(g_timefmt, ltime) + ", remote time: " + time.strftime(g_timefmt, self._time))
			if time.strftime(g_timefmt, ltime) != time.strftime(g_timefmt, self._time):
				return True
			else:
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
	def __genlist(self):
		# get index
		#call("wget --progress=bar -O " + "index.html" + " " + base_url, shell=True)
		soup = BeautifulSoup(open("index.html"), "html.parser")
		#print(soup.prettify())
		prev_file = None
		prev_pkg_name = ""
		prev_pkg_ver = ""
		for link in soup.html.body.table.tbody.find_all("tr", recursive=False):
			#print(link["href"])
			NNN = link.contents[0]
			print("NNN: " + NNN.string)
			#continue
			file_name = NNN.a["href"].strip()
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

			SSS = link.contents[1]
			TTT = link.contents[2]
			print("SSS: " + SSS.string)
			print("TTT: " + TTT.string.strip())
			file_size = SSS.string.strip()
			file_time = time.strptime(TTT.string.strip(), g_timefmtlist[0])
			# parse
			self._fl_ordered.append(file_name)
			if re.match(r"^.*"
				"(_\.svn|\.trunk|svn\.)"
				".*$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, False)
				continue
			if re.match(r"^git[2]?_.*$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, False)
				continue
			if re.match(r"^.*\.patch$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, True)
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
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, True)
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
				prev_file = creg_file(self, file_name, file_size, file_time, True)

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
							prev_file = creg_file(self, file_name, file_size, file_time, True)
						break
		# the final one
		if prev_file:
			self._fl_regular[prev_file.name()] = prev_file
	def __genlist1(self):
		# get index
		#call("wget --progress=bar -O " + "index.html" + " " + base_url, shell=True)  
		fp = open("index.html")

		prev_file = None
		prev_pkg_name = ""
		prev_pkg_ver = ""
		for cnt, line in enumerate(fp):
			link = re.split(' +', line)
			
			if len(link) < 9:
				continue

			file_name = link[8].rstrip()
			file_size = link[4]
			#directory
			if re.match("\..*", file_name):
				continue
			if re.match(".*/$", file_name):
				continue
			#done file
			if re.match(".*\.done$", file_name):
				continue
			if re.match(".*\.lock$", file_name):
				continue
			if re.match(".*bad-checksum.*", file_name):
				continue
			if file_size == 0:
				continue

			#print(link)
			if re.match(".*\:.*", link[7]):
				file_time = time.strptime(time.strftime("%Y", time.gmtime()) + '-' + link[5] + '-' + link[6] + ' ' + link[7], g_timefmtlist[0])
			else:
				file_time = time.strptime(link[7] + '-' + link[5] + '-' + link[6], g_timefmtlist[1])

			# parse
			self._fl_ordered.append(file_name)
			if re.match(r"^.*"
				"(_\.svn|\.trunk|svn\.)"
				".*$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, False)
				continue
			if re.match(r"^git[2]?_.*$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, False)
				continue
			if re.match(r"^.*\.patch$", file_name):
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, True)
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
				self._fl_non_regular[file_name] = creg_file(self, file_name, file_size, file_time, True)
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
				prev_file = creg_file(self, file_name, file_size, file_time, True)

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
							prev_file = creg_file(self, file_name, file_size, file_time, True)
						break
		# the final one
		if prev_file:
			self._fl_regular[prev_file.name()] = prev_file
	def __init__(self, base_url, loc_dir):
		self._main_page = base_url
		self._fl_non_regular = {}
		self._fl_regular = {}
		self._fl_dl = {}
		self._fl_ordered = []
		self._loc_dir = loc_dir

		if g_STYLE == 0:
			self.__genlist()
		else:
			self.__genlist1()
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
