#!/usr/bin/env python
# autor: Ni Qingliang
# NOTE: this script can be used to sync yocto repository which is accessed through
#       http
import tkinter
from tkinter import ttk

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

#g_re_ext = r"tar\.bz2|tar\.gz|tar\.xz|tgz|zip|gz|bz2"
#g_re_ver = r"(?P<pkgver>(([0-9]+\.)+[0-9]+)|(([0-9]+_)+[0-9]+))"
#g_re_cmm = r"-" + g_re_ver + r"\." + g_re_ext
#g_re_cmm2 = r"_" + g_re_ver + r"\." + g_re_ext
#g_re_cmm3 = r"_" + g_re_ver + r"\.orig\." + g_re_ext
#g_re_cmm4 = g_re_ver + r"\." + g_re_ext
#g_re_nover = ""
#g_re_withp = r"-" + g_re_ver + "p" + r"(?P<pkgp>[0-9]+)" + r"\." + g_re_ext
#g_re_withaz = g_re_ver + r"(?P<pkgaz>[a-zA-Z])" + r"\." + g_re_ext
#
#class pkg_info:
#	def __init__(self, pn, vre = g_re_cmm, vreWithName = False):
#		self._pn = pn
#		if re.match(g_re_cmm, r"^git2_.*"):
#			self._re = g_re_cmm
#		else:
#			if vreWithName:
#				self._re = vre
#			else:
#				self._re = pn + vre
#	def pn(self):
#		return self._pn
#	def vre(self):
#		return self._re
#
#g_pkg_list = {
#	pkg_info("acl"), #-2.3.1.tar.gz"
#	pkg_info("attr"), #-2.5.1.tar.gz"
#	pkg_info("autoconf"), #-2.71.tar.gz"
#	pkg_info("autoconf-archive"), #-2022.09.03.tar.xz"
#	pkg_info("automake"), #-1.16.5.tar.gz"
#	pkg_info("base-passwd", g_re_cmm2), #_3.6.1.tar.xz"
#	pkg_info("bash"), #-5.2.9.tar.gz"
#	pkg_info("bash-completion"), #-2.11.tar.xz"
#	pkg_info("bc"), #-1.07.1.tar.gz"
#	pkg_info("bison"), #-3.8.2.tar.xz"
#	pkg_info("bluez"), #-5.65.tar.xz"
#	pkg_info("boost", g_re_cmm2), #_1_80_0.tar.bz2"
#	pkg_info("busybox"), #-1.35.0.tar.bz2"
#	pkg_info("bzip2"), #-1.0.8.tar.gz"
#	pkg_info("cairo"), #-1.16.0.tar.xz"
#	pkg_info("check"), #-0.15.2.tar.gz"
#	pkg_info("cmake"), #-3.24.2.tar.gz"
#	pkg_info("coreutils"), #-9.1.tar.xz"
#	pkg_info("cpio"), #-2.13.tar.gz"
#	pkg_info("curl"), #-7.86.0.tar.xz"
#	pkg_info("dbus"), #-1.14.4.tar.xz"
#	pkg_info("dbus-python"), #-1.3.2.tar.gz"
#	pkg_info("docbook-xml", g_re_cmm3), #_4.5.orig.tar.gz"
#	pkg_info("docbook-xsl"), #-1.79.1.tar.bz2"
#	pkg_info("dosfstools"), #-4.2.tar.gz"
#	pkg_info("dropbear"), #-2022.82.tar.bz2"
#	pkg_info("elfutils"), #-0.188.tar.bz2"
#	pkg_info("expat"), #-2.5.0.tar.bz2"
#	pkg_info("flex"), #-2.6.4.tar.gz"
#	pkg_info("flit"), #-3.8.0.tar.gz"
#	pkg_info("fmt"), #-9.1.0.zip"
#	pkg_info("fontconfig"), #-2.14.1.tar.gz"
#	pkg_info("freetype"), #-2.12.1.tar.xz"
#	pkg_info("gawk"), #-5.1.1.tar.gz"
#	pkg_info("gcc"), #-12.2.0.tar.xz"
#	pkg_info("gdbm"), #-1.23.tar.gz"
#	pkg_info("gettext"), #-0.21.1.tar.gz"
#	pkg_info("glib"), #-2.74.1.tar.xz"
#	pkg_info("gmp"), #-6.2.1.tar.bz2"
#	pkg_info("gnutls"), #-3.7.8.tar.xz"
#	pkg_info("gobject-introspection"), #-1.72.0.tar.xz"
#	pkg_info("gperf"), #-3.1.tar.gz"
#	pkg_info("gpgme"), #-1.18.0.tar.bz2"
#	pkg_info("gsl"), #-2.7.1.tar.gz"
#	pkg_info("gtk-doc"), #-1.33.2.tar.xz"
#	pkg_info("harfbuzz"), #-5.3.1.tar.xz"
#	pkg_info("i2c-tools"), #-4.3.tar.gz"
#	pkg_info("icu4c-data", "icu4c-" + g_re_ver + r"-data\." + g_re_ext, True),##########################
#	pkg_info("icu4c-src", "icu4c-" + g_re_ver + r"-src\." + g_re_ext, True),##########################
#	pkg_info("iniparse"), #-0.5.tar.gz"
#	pkg_info("installer"), #-0.5.1.tar.gz"
#	pkg_info("intltool"), #-0.51.0.tar.gz"
#	pkg_info("itstool"), #-2.0.7.tar.bz2"
#	pkg_info("Jinja2"), #-3.1.2.tar.gz"
#	pkg_info("json-c"), #-0.16.tar.gz"
#	pkg_info("kbd"), #-2.5.1.tar.xz"
#	pkg_info("libarchive"), #-3.6.1.tar.gz"
#	pkg_info("libassuan"), #-2.5.5.tar.bz2"
#	pkg_info("libcap"), #-2.66.tar.xz"
#	pkg_info("libcap-ng"), #-0.8.3.tar.gz"
#	pkg_info("libevdev"), #-1.13.0.tar.xz"
#	pkg_info("libffi"), #-3.4.4.tar.gz"
#	pkg_info("libgcrypt"), #-1.10.1.tar.bz2"
#	pkg_info("libgpg-error"), #-1.46.tar.bz2"
#	pkg_info("libical"), #-3.0.16.tar.gz"
#	pkg_info("libidn2"), #-2.3.4.tar.gz"
#	pkg_info("libjpeg-turbo"), #-2.1.4.tar.gz"
#	pkg_info("libpng"), #-1.6.38.tar.xz"
#	pkg_info("libtirpc"), #-1.3.3.tar.bz2"
#	pkg_info("libtool"), #-2.4.7.tar.gz"
#	pkg_info("libunistring"), #-1.1.tar.gz"
#	pkg_info("libwebp"), #-1.2.4.tar.gz"
#	pkg_info("libX11"), #-1.6.8.tar.bz2"
#	pkg_info("libxkbcommon"), #-1.4.1.tar.xz"
#	pkg_info("libxml2"), #-2.9.14.tar.xz"
#	pkg_info("libxslt"), #-1.1.37.tar.xz"
#	pkg_info("linux"), #-5.15.53.tar.xz"
#	pkg_info("lrzsz"), #-0.12.20.tar.gz"
#	pkg_info("lua"), #-5.4.4.tar.gz"
#	pkg_info("lzo"), #-2.10.tar.gz"
#	pkg_info("m4"), #-1.4.19.tar.gz"
#	pkg_info("make"), #-4.4.tar.gz"
#	pkg_info("MarkupSafe"), #-2.1.1.tar.gz"
#	pkg_info("meson"), #-0.64.0.tar.gz"
#	pkg_info("minicom", g_re_cmm3), #_2.8.orig.tar.bz2"
#	pkg_info("mpc"), #-1.2.1.tar.gz"
#	pkg_info("mpfr"), #-4.1.0.tar.xz"
#	pkg_info("mtdev"), #-1.1.6.tar.bz2"
#	pkg_info("netbase", g_re_cmm2), #_6.4.tar.xz
#	pkg_info("nettle"), #-3.8.1.tar.gz"
#	pkg_info("openssh", g_re_withp), #-9.1p1.tar.gz"##################################
#	pkg_info("openssl"), #-3.0.7.tar.gz"
#	pkg_info("opkg"), #-0.6.0.tar.gz"
#	pkg_info("patch"), #-2.7.6.tar.gz"
#	pkg_info("pcre2"), #-10.40.tar.bz2"
#	pkg_info("perl"), #-5.36.0.tar.gz"
#	pkg_info("perl-cross"), #-1.4.tar.gz"
#	pkg_info("pigz"), #-2.7.tar.gz"
#	pkg_info("pixman"), #-0.42.2.tar.gz"
#	pkg_info("popt"), #-1.19.tar.gz"
#	pkg_info("postgresql"), #-14.5.tar.bz2"
#	pkg_info("pseudo-prebuilt"), #-2.33.tar.xz"
#	pkg_info("pygobject"), #-3.42.2.tar.xz"
#	pkg_info("Python"), #-3.11.0.tar.xz"
#	pkg_info("qemu"), #-7.1.0.tar.xz"
#	pkg_info("quilt"), #-0.67.tar.gz"
#	pkg_info("re2c"), #-3.0.tar.xz"
#	pkg_info("readline"), #-8.2.tar.gz"
#	pkg_info("rsync"), #-3.2.7.tar.gz"
#	pkg_info("setuptools"), #-65.5.1.tar.gz"
#	pkg_info("shadow"), #-4.13.tar.gz"
#	pkg_info("six"), #-1.16.0.tar.gz"
#	pkg_info("SourceHanSansCN.zip", g_re_nover)#######################################
#	pkg_info("sqlite-autoconf"), #-3390400.tar.gz"
#	pkg_info("strace"), #-6.0.tar.xz"
#	pkg_info("sudo", g_re_withp), #-1.9.12p1.tar.gz"####################################
#	pkg_info("swig"), #-4.1.0.tar.gz"
#	pkg_info("sysfsutils"), #-2.1.0.tar.gz"
#	pkg_info("tar"), #-1.34.tar.bz2"
#	pkg_info("tzcode", g_re_withaz), #2022d.tar.gz"#################################
#	pkg_info("tzdata", g_re_withaz), #2022d.tar.gz"################################
#	pkg_info("unifdef"), #-2.12.tar.xz"
#	pkg_info("unzip", g_re_cmm4), #60.tar.gz"
#	pkg_info("util-linux"), #-2.38.1.tar.xz"
#	pkg_info("util-macros"), #-1.19.3.tar.gz"
#	pkg_info("vala"), #-0.56.3.tar.xz"
#	pkg_info("wheel"), #-0.38.4.tar.gz"
#	pkg_info("xkeyboard-config"), #-2.37.tar.xz"
#	pkg_info("xlslib", #-package-2.5.0.zip"#################################
#	pkg_info("XML-Parser"), #-2.46.tar.gz"
#	pkg_info("xmlts", g_re_cmm4), #20080827.tar.gz"
#	pkg_info("xz"), #-5.2.7.tar.gz"
#	pkg_info("yaml"), #-0.2.5.tar.gz"
#	pkg_info("zlib"), #-1.2.13.tar.gz"
#}

#g_splitReg = re.compile(
#	"^<tr>"
#	+ "<td class=\"link\"><a href=\"([^\"]+)\" title=\"[^\"]+\">[^</]+</a></td>"
#	+ "<td class=\"size\">([^<]+)</td>"
#	+ "<td class=\"date\">([^<]+)</td>"
#	+ "</tr>$")
g_splitReg = re.compile(
	"^<tr>"
	+ "<td class=\"[^\"]+\"><a href=\"([^\"]+)\" title=\"[^\"]+\">[^</]+</a></td>"
	+ "<td class=\"size\">([^<]+)</td>"
	+ "<td class=\"date\">([^ ]+) ([^ <]+)</td>"
	+ "</tr>$")
g_list_file = "files.lst"
g_html_file = "index.html"
g_loc_dir = './sources.yoctoproject/'
g_new_dir = './sources.new/'
g_deprecated_dir = "./sources.deprecated/"
g_updated_dir = "./sources.updated/"
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

def cmp_ver(s0, s1):
	if s0 == s1:
		return 0
	print("cmp ver: " + s0 + ", " + s1)
	ver0 = re.split('[\._]', s0)
	ver1 = re.split('[\._]', s1)
	for i,j in zip(ver0, ver1):
		print("i: " + i + ", j: " + j)
		if i == "":
			if j == "":
				continue
			else:
				return -1
		else:
			if j == "":
				return 1
			#else: compare it
		v0 = int(i)
		v1 = int(j)
		if v0 == v1:
			continue
		if v0 < v1:
			return -1
		if v0 > v1:
			return 1
	if len(ver0) > len(ver1):
		return 1
	if len(ver0) < len(ver1):
		return -1
	return 0
def stage_to_n(s):
	if len(s) == 1:
		return ord(s)
	switch={
		"alpha": 100,
		"beta": 101,
		"rc": 102,
		"pre": 103,
		"p": 104,
		"P": 105,
		}
	return switch.get(s, -1)
def cmp_stage(s0, s1):
	if s0 == s1:
		return 0
	v0 = stage_to_n(s0)
	v1 = stage_to_n(s1)
	if v0 < v1:
		return -1
	if v0 > v1:
		return 1
	return 0

class creg_file:
	def __init__(self, parent, fname, fsize, ftime):
		self._parent = parent
		self._name = fname
		self._size = fsize
		self._time = ftime
		self._need = False
		self._need_dl = False

		self._pkgname = ""
		self._pkgver = ""
		self._pkgstage = ""
		self._pkgstagever = ""
		self._pkgrevision = ""
		m = re.match(r"^(?P<pkgname>.*)"
				"(-|_|-s|\.v)"
				"(?P<pkgver>(([0-9]+\.)+[0-9]+)|(([0-9]+_)+[0-9]+))"
				"(?P<pkgstage>-P[0-9]+|p[0-9]+|[a-z]|alpha|-?beta[0-9]*|-?rc[0-9]+|-pre[0-9]+)?"
				"(-(?P<pkgrevision>[0-9]+))?"
				"\."
				"(?P<ext>tar\.bz2|tar\.gz|tar\.xz|tgz|zip|gz|bz2|crate)"
				"$", fname)
		if m:
			self._pkgname = m.group("pkgname")
			self._pkgver = m.group("pkgver")

			if m.group("pkgstage"):
				#print("pkgstage: " + m.group("pkgstage"))
				mm = re.match(r"^-?"
					"(?P<prefix>[a-zA-Z]*)"
					"(?P<version>[0-9]*)", m.group("pkgstage"))
				if mm:
					if mm.group("prefix"):
						self._pkgstage = mm.group("prefix")
					if mm.group("version"):
						self._pkgstagever = mm.group("version")
				else:
					assert(0)
			if m.group("pkgrevision"):
				self._pkgrevision = m.group("pkgrevision")
		if m:
			self._cant_parse = False
		else:
			self._cant_parse = True

	def set_need(self, isNeed):
		self._need = isNeed
		self._need_dl = self.__need_dl()
	def get_need(self):
		return self._need
	def get_need_dl(self):
		return self._need_dl
	def is_cant_parse(self):
		return self._cant_parse

	def __need_dl(self):
		if not self.get_need():
			return False
		file_path = self._parent.loc_dir() + self._name
		
		if os.path.exists(file_path + ".st"):
			os.remove(file_path)
			os.remove(file_path + ".st")
		if os.path.exists(file_path):
			statinfo = os.stat(file_path)
			#if (statinfo.st_size == self._size):
			#	and (time.gmtime(statinfo.st_mtime) >= self._time):
			#	return False
			#if not re.match("^git2_.*", self._name):
			#	return False
			if (time.gmtime(statinfo.st_mtime) >= self._time):
				return False
			#print("local time: ")
			#print(time.gmtime(statinfo.st_mtime))
			#print("remote time: ")
			#print(self._time)
			#print(time.gmtime(statinfo.st_mtime) >= self._time)
			call("mv " + file_path + " " + g_updated_dir, shell=True)
		return True

	def name(self):
		return self._name
	def pkgname(self):
		if (self._pkgname == ""):
			return self._name
		return self._pkgname
	def cmpWith(self, other):
		assert(self.pkgname() == other.pkgname())
		assert(self._pkgver != "")
		#print("cmp: " + self._name)
		#print("cmp pkg ver")
		cmpr = cmp_ver(self._pkgver, other._pkgver)
		if cmpr != 0:
			return cmpr
		#print("cmp pkg stage")
		cmpr = cmp_stage(self._pkgstage, other._pkgstage)
		if cmpr != 0:
			return cmpr
		#print("cmp pkg stagever")
		cmpr = cmp_ver(self._pkgstagever, other._pkgstagever)
		if cmpr != 0:
			return cmpr
		#print("cmp pkg rev")
		cmpr = cmp_ver(self._pkgrevision, other._pkgrevision)
		if cmpr != 0:
			return cmpr
		#print(self.name() + ", " + self._pkgver + "," + self._pkgstage)
		#print(other.name() + ", " + other._pkgver + "," + other._pkgstage)
		#print("can't parse:")
		#print("\t" + self.name())
		#print("\t" + other.name())
		other.set_cant_parse()
		self.set_cant_parse()
		return 0
	def set_cant_parse(self):
		self._cant_parse = True
class csub_rep:
	def __genlist(self):
		fp = open(g_html_file)

		for cnt, line in enumerate(fp):
			splitR = g_splitReg.match(line)
			if not splitR:
				continue
			#for i in [1, 2, 3]:
			#	print("{}: {}".format(i, splitR.group(i)))

			file_name = urllib.parse.unquote(splitR.group(1))
			if re.match(".*bad-checksum.*", file_name):
				continue
			if re.match("^git2_tmp.*", file_name):
				continue
			# use git repo
			if re.match("^git2_.*", file_name):
				continue
			file_size = splitR.group(2)
			file_time = time.strptime(splitR.group(3) + " " + splitR.group(4), "%Y-%b-%d %H:%M")

			self._full_fl[file_name] = creg_file(self, file_name, file_size, file_time)
	def __init__(self, base_url, loc_dir):
		self._main_page = base_url
		self._loc_dir = loc_dir

		self._full_fl = {}
		self.__genlist()

	def loc_dir(self):
		return self._loc_dir
	def main_page(self):
		return self._main_page

	def prepare_for_run(self):
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

		return
	def gen_cb_list(self, par):
		last_settings = {}
		with fileinput.input(files=(g_list_file)) as f:
			for line in f:
				m = re.match("([+-])(.*)", line)
				if m:
					if m.group(1) == "+":
						last_settings[m.group(2)] = True
					elif m.group(1) == "-":
						last_settings[m.group(2)] = False
		# generate package list (newest list need)
		_tmp = {}
		for i in self._full_fl:
			vv = self._full_fl[i]
			pn = vv.pkgname()
			# old delete files
			if (i in last_settings) and (not last_settings[i]):
				continue
			# old download or new
			if pn in _tmp:
				if vv.cmpWith(_tmp[pn]) > 0:
					#print("\tnew version: " + vv.name())
					_tmp[pn] = vv
			else:
				#print("new package: " + vv.pkgname())
				_tmp[pn] = vv
		# add in gui list
		for (k, v) in natural_sorted(self._full_fl.items()):
			# old delete files
			if (k in last_settings) and (not last_settings[k]):
				continue

			# need dlownload?
			_dl = False
			if v.pkgname() in _tmp:
				if _tmp[v.pkgname()] == v:
					_dl = True

			# insert and set select
			par.insert(tkinter.END, k)
			if _dl:
					par.selection_set(tkinter.END)

			# set decoration
			if (k in last_settings):
				par.itemconfig(tkinter.END, fg="black", selectforeground="black")
				par.itemconfig(tkinter.END, selectbackground="grey75")
				#if last_settings[k]:# old download
					#if _dl:# keep
					#else:# drop
				#else:
				#	assert(0)
			else:# new files
				par.itemconfig(tkinter.END, fg="purple4", selectforeground="purple4")
				par.itemconfig(tkinter.END, selectbackground="SlateBlue1")
				#if _dl:# new download
				#else:# new drop

			if v.is_cant_parse():
				par.itemconfig(tkinter.END, fg="red", selectforeground="red")

			#if (k in last_settings):# old file
			#	if last_settings[k]:# old selected
			#		par.insert(tkinter.END, k)
			#		if v.pkgname() in _tmp:
			#			if _tmp[v.pkgname()] == v:
			#				par.selection_set(tkinter.END)
			#else:#new file
			#	par.insert(tkinter.END, k)
			#	par.itemconfig(tkinter.END, selectbackground="blue")
			#	if v.is_cant_parse():
			#		par.itemconfig(tkinter.END,{'fg': "red"})
			#	else:
			#		if v.pkgname() in _tmp:
			#			if _tmp[v.pkgname()] == v:
			#				par.selection_set(tkinter.END)
	def process_need_list(self, par):
		for i in par.curselection():
			self._full_fl[par.get(i)].set_need(True)

		# generate download list
		self._dl_fl = {}
		for (k,v) in natural_sorted(self._full_fl.items()):
			if v.get_need_dl():
				print("need dl: " + k)
				self._dl_fl[k] = v

		# create locale directory
		if not os.path.exists(self._loc_dir):
			os.makedirs(self._loc_dir)

if __name__ == '__main__':
	base_url = 'http://downloads.yoctoproject.org/mirror/sources/'
	#call("wget --progress=bar -O " + g_html_file + " " + base_url, shell=True)
	test = csub_rep(base_url, g_loc_dir)

	# edit
	win = tkinter.Tk()
	listbox = tkinter.Listbox(win, selectmode="multiple", height=40,width=100)
	test.gen_cb_list(listbox)
	listbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
	#listbox.configure(font=('Aerial 13'))
	#scrollbar = ttk.Scrollbar(win, orient='vertical', command=listbox.yview)
	#scrollbar.grid(row=0, column=1, sticky=tkinter.NS)
	scrollbar = tkinter.Scrollbar(win)
	scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
	listbox.config(yscrollcommand=scrollbar.set)
	scrollbar.config(command=listbox.yview)
	win.protocol("WM_DELETE_WINDOW", lambda : (
		      test.process_need_list(listbox),
		      win.destroy()
		      ))
	win.mainloop()

	# download
	test.prepare_for_run()
	threadList = []
	for i in range(0, g_thread_number):
		tmp = threading.Thread(target = test.run, args = [i])
		tmp.start()
		threadList.append(tmp)
	for i in range(0, g_thread_number):
		threadList[i].join()

	# save
	test.save()
	# remove old
	test.rm_old_files()
	call("rm ./sources/*; find sources.yoctoproject/ sources.custom/ -type f -exec ln -sf ../{} ./sources/ \\;", shell=True)
