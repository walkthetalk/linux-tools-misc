#!/usr/bin/env python
# autor: Ni Qingliang
# NOTE: this script can be used to sync arch repository which is accessed through
#       http

import time
import datetime
import re
import os
import tempfile
import urllib.parse

from bs4 import BeautifulSoup
from subprocess import call
import fileinput

#g_host = "mirrors.163.com"
g_host = "mirrors.ustc.edu.cn"
g_loc_base_dir = "/srv/http/archlinux/"

class csub_rep:
	def __init__(self, repo_name, main_page, loc_dir):
		self._repo_name = repo_name
		self._main_page = main_page
		self._loc_dir = loc_dir

		self._fl_new = []
		self._fl_old = []
		# get index
		tmp_dir = tempfile.mkdtemp(prefix="syncarch_") + "/"
		call("wget --progress=bar"
			+ " -O index.html"
			+ " -P " + tmp_dir
			+ " " + self._main_page, shell=True)
		soup = BeautifulSoup(open("index.html"))
		os.rmdir(tmp_dir)

		for a in soup.pre.find_all("a", recursive=False):
			# string的内容如果太长，html显示的是省略号
			#self._fl_new.add(a.string);
			file_name = a["href"]
			# 去除上一级目录
			if file_name == "../":
				continue
			# 处理 %
			file_name = urllib.parse.unquote(string=file_name, errors="strict")
			# 移除开头的./，163的有问题
			self._fl_new.append(re.sub("^\./", "", file_name));

		#for f in self._fl_new:
		#	print(f)
		#print(len(self._fl_new))

		# create locale directory
		if not os.path.exists(self._loc_dir):
			os.makedirs(self._loc_dir)
		else:
			self._fl_old = os.listdir(self._loc_dir)
			#for f in self._fl_old:
			#	print(f)
			#print(len(self._fl_old))

		# abs list
		self.__abs_list = []
		for i in (
			".abs.tar.gz",
			".db",
			".db.tar.gz",
			".db.tar.gz.old",
			".files",
			".files.tar.gz",
			".files.tar.gz.old"):
			self.__abs_list.append(self._repo_name + i)

	def download(self):
		dl_list = list(set(self._fl_new) - set(self._fl_old) - set(self.__abs_list))
		dl_list.sort()
		for i in dl_list:
			print("dling " + i)
			call("wget -N --progress=bar -P " + self._loc_dir + " " + self._main_page + i, shell=True)

		if len(dl_list) != 0:
			abs_names = list(set(self.__abs_list) & set(self._fl_new))
			abs_names.sort()

			bkup_dir = tempfile.mkdtemp(prefix="syncarch_") + "/"
			for i in abs_names:
				print("dling " + i)
				call("wget -N --progress=bar -P " + bkup_dir + " " + self._main_page + i, shell=True)

			for i in abs_names:
				call("mv " + bkup_dir + i + " " + self._loc_dir + i, shell=True)
			os.rmdir(bkup_dir)

	def rm_old_files(self):
		for i in (set(self._fl_old) - set(self._fl_new)):
			print("rming " + i)
			os.remove(self._loc_dir + i)

if __name__ == '__main__':
	repos = ["core",
		"extra",
		"community",
		"multilib",
#		"testing",
#		"multilib-testing",
#		"community-testing"
	]

	for repo in repos:
		print("dling repo %s:" % (repo))
		test = csub_rep(repo, "http://" + g_host + '/archlinux/' + repo + '/os/x86_64/', g_loc_base_dir + repo + "/os/x86_64/")
		test.download()
		test.rm_old_files()
