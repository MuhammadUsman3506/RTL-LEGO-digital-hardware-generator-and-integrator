#!/bin/bash
. ~/.LEGO_USR_INFO
RED=$'\e[1;31m';
YELLOW=$'\e[1;33m';
WHITE=$'\e[1;37m';
GREEN=$'\e[1;32m';

PATH="${LEGO_DIR}/files/library"
USAGE(){
echo -e ${YELLOW} "USAGE:\n 1) To see library files\n\t list_lagos \n 2) To view each file \n\t list_lagos -f [filename] \n 3) To edit file \n\t list_lago -fe [filename] ";
}
if [ -d $PATH ]
then
	cd $PATH
	if [ $# -eq 0 ]
	then
	      /bin/tree
		exit
	elif [[ $# -eq 2 && $1 == '-f' || $1 == '--file' ]]
	then
		if [[ -f $2 ]]
		then
			/bin/cat $2
			exit
		else
			echo "$1: not exists ";
			exit
		fi
	elif [[ $# -eq 2 && $1 == '-e' || $1 == '--edit' ]]
	then
		if [[ -f $2 ]]
		then
			/bin/nano $2
			exit
		else
			echo "$1: not exists ";
			exit
		fi
	elif [[ $# -eq 1 && $1 == '-h' || $1 == '--help' ]]
	then
		USAGE
	else
		echo "Unkown argument";
		USAGE
	fi
else
	echo "library files not exists";
	exit
fi
