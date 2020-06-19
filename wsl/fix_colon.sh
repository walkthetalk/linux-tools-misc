#!/usr/bin/env sh

for i in `find $1 -type f | grep ""`; do
	mv $i `echo $i | sed 's//:/'`
done
