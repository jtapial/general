#!/usr/bin/env bash

if [ "$1" == "-h" ] ; then
	echo -e "UNTAR_ALL.SH , by Javier Tapial"
	echo -e "-----------------------------------"
	echo -e "This script takes an input path and a destination path."
	echo -e "Then all .tar files in the input path are unpacked into specific folders at the destination path"
	echo -e "Include the '-zipped' flag if the .tar files are zipped, followed by the extension of the zipped files ('.tgz', '.tar.gz', '.bz2'...)\n"
	echo -e "Usage: $(basename "$0") [-h] [-zipped EXTENSION] INPUT_PATH DESTINATION_PATH"
	exit 0

elif [ "$1" == "-zipped" ] ; then
	for f in $3/*$2; do
		d=`basename $f $2`
		mkdir $3/$d
		tar -xzf $f -C $4/$d
	done

else
	for f in $1/*.tar; do
		d=`basename $f .tar`
		mkdir $2/$d
		tar -xf $f -C $2/$d
	done
fi
