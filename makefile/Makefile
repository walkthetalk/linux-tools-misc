override CFLAGS += -std=c11
override CXXFLAGS += -std=c++11

# NOTE: you can select one of the following styles to minimal binary size

# minimal final size option 1
#override LDFLAGS += -Wl,--gc-sections
#override CFLAGS += -fdata-sections -ffunction-sections
#override CXXFLAGS += -fdata-sections -ffunction-sections

# minimal final size option 2
#override CFLAGS += -fwhole-program
#override CXXFLAGS += -fwhole-program

# minimal final size option 3
#override LDFLAGS += -flto
#override CFLAGS += -flto
#override CXXFLAGS += -flto

# you can add your own libs need to link.
#override LDLIBS += -lpthread

# the aux variable, used to identify the directory this Makefile in.
dir_self := $(shell dirname $(shell readlink -fe $(lastword ${MAKEFILE_LIST})))
dir_main := $(dir_self)

############ compile control
# output directory, all the output files will be put in it.
output_dir := ${dir_main}/output
# the main name of this program
main_name := TEST
# include directories, use `:' as seperator
inc_dir_set := ${dir_main}/include
# recursive directory, will compile files in it, and in it's subdirectories.
src_recdir_set:=${dir_main}/src
# solo directory, will only compile the files under it directly, no recursive.
#src_solodir_set:=${dir_self}/src

# the default value of `output_types' is `bin'
# you can assign multi value to it.
# the selective values:
# 	bin:		*	exe program.
# 	sharedlib:	*.so	if you selected it, you must define `lib_version'
# 			simultaneously.
#	staticlib:	*.a	used to link with other module to final .so or bin.
#output_types := bin,sharedlib,staticlib
#lib_version :=
output_types := bin

############ install control
# if your output_types contain *lib, then you need it.
header_dir := ${dir_main}/include

include ${dir_main}/Makefile.base
