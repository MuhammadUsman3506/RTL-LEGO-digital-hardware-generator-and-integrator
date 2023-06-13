#!/bin/bash
#set -x
LEGO_DIR=$(pwd);
FILE1=false;
FILE2=false;
FILE3=false;

RED=$'\e[1;31m'
YELLOW=$'\e[1;33m'
WHITE=$'\e[1;37m'
GREEN=$'\e[1;32m'

CREATE_LINK()
{
	cd /usr/bin/
	sudo ln -s  ${LEGO_DIR}/files/create.py create;
	echo "+++++++++++++++++++++++++++++";
	echo "======create  installed======";
	sudo ln -s  ${LEGO_DIR}/files/plug.py plug;
	echo "======plug    installed======";
	sudo ln -s  ${LEGO_DIR}/files/connect.py connect;
	echo "======connect installed======";
	sudo ln -s ${LEGO_DIR}/list_lego.sh list_lego;
	echo "======list_lago installed===";
	sudo ln -s ${LEGO_DIR}/files/add.py add;
	echo "======add installed=======";
	sudo ln -s ${LEGO_DIR}/files/rename.py rename;
	echo "======rename installed=======";
	sudo ln -s ${LEGO_DIR}/files/delete.py delete;
	echo "======delete installed=======";
	echo "+++++++++++++++++++++++++++++";
	cd $LEGO_DIR
	if [[ -f ~/.LAGO_USR_INFO ]]
	then
		/bin/rm -r ~/.LEGO_USR_INFO
		echo -n "LEGO_DIR=${LEGO_DIR}">~/.LEGO_USR_INFO;

	elif [[ -n ~/.LAGO_USR_INFO ]]
	then
		echo -n "LEGO_DIR=${LEGO_DIR}">~/.LEGO_USR_INFO;
	else
		echo "error: LEGO_USR_INFO is not written!";
		exit 1
	fi

		/bin/chmod u+x *.sh
		/bin/chmod u+x ${LEGO_DIR}/examples/*
		/bin/chmod u+x ${LEGO_DIR}/files/*.py

		${LEGO_DIR}/list_lego.sh

	# adding tab_completion to /etc/bash_completion.d/
	if [[ -f /etc/bash_completion.d/tab_completion.sh ]]
	then
		echo ${YELLOW} "tab_completion is already installed";
	else
		sudo cp ${LEGO_DIR}/tab_completion.sh /etc/bash_completion.d/tab_completion.sh
		echo "tab_completion installed";
		echo -e ${GREEN}  "\nplease restart your terminal to apply changes"
	fi
}


if [ -e ./files/create.py ];then
	FILE1=true;
else
	echo "create.sh not exists";
	echo "create.sh is not installed";
	exit 1;
fi
if [ -e ./files/plug.py ];then
	FILE2=true;
else
	echo "plug.sh not exists";
	echo "plug.sh is not installed ";
	exit 1;
fi

if [ -e ./files/connect.py ];then
	FILE3=true;
else
	echo "connect.sh not exists"
	echo "connect.sh is not installed"
	exit 1
fi

#if [ -e ./files/config.py ];then
#	FILE4=true;
#else
#	echo "config.sh not exists"
#$	echo "config.sh is not installed"
#	exit 1
#fi

CREATE_LINK

#echo -e -n ${WHITE} "USAGE:\nUse 'create' command to generate toplevel file\n eg:";./create.sh '-h';
#echo -e -n ${WHITE}  "\nAfter creating toplevel file use 'plug' command to plug the instance of file\n eg:"; ./plug.sh '-h';
#echo -e -n ${WHITE} "\nAfter pluging instances use 'connect' command to connect instances \n eg:";./connect.sh '-h';
#echo -e -n ${WHITE} "\nUse config command to configure your Top_level_file"
#echo -e -n ${WHITE} "\nUse 'list_lago' command to find avalible modules";./list_lago.sh '-h';
#echo -e -n ${WHITE} "\nHERE is a list of files you can plug to:";
