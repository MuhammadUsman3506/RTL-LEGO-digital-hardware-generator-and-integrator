#!/bin/bash
GREEN=$'\e[1;32m'
YELLOW=$'\e[1;33m'
cd /usr/bin
# remove links
set -e
# remove links
if [[ -L "/usr/bin/create" ]]
then
	echo "------------------------------";
	sudo /bin/rm /usr/bin/create
	echo "-----create uninstalled-------";
else
	echo "---create is not installed----";
fi

if [[ -L "/usr/bin/plug" ]]
then
	echo "------------------------------";
	sudo /bin/rm /usr/bin/plug
	echo "------plug uninstalled--------";
else
	echo "----plug is not installed----";
fi
if [[ -L "/usr/bin/connect" ]]
then
	echo "------------------------------";
	sudo /bin/rm /usr/bin/connect
	echo "-----connect uninstalled------";
else
	echo "--connect is not installed----";
fi
if [[ -L "/usr/bin/list_lago" ]]
then
	echo "------------------------------";
	sudo /bin/rm /usr/bin/list_lago
	echo "----list_lago uninstalled-----";
else
	echo "--list_lago is not installed-";
fi
if [[ -L "/usr/bin/add" ]]
then
	echo "------------------------------";
	sudo /bin/rm /usr/bin/add
	echo "-------add uninstalled--------";
else
	echo "---add is not installed-----";
fi
if [[ -L "/usr/bin/rename" ]]
then
	echo "------------------------------";
	sudo /bin/rm /usr/bin/rename
	echo "------rename uninstalled-------";
else
	echo "-----rename is not installed-";
fi
if [[ -L "/usr/bin/delete" ]]
then
	echo "------------------------------";
	sudo /bin/rm /usr/bin/delete
	echo "------delete uninstalled------";
else
	echo "---delete is not installed---";
fi
cd ~
# removing LAGO_USR_INFO
if [[ -f ~/.LAGO_USR_INFO ]]
then
	/bin/rm ~/.LAGO_USR_INFO
	echo "-------------------------------"
	echo "---LAGO_USR_INFO uninstalled---";
	echo "-------------------------------";
else
	echo "-LAGO_USR_INFO is not installed-";
fi

# removing tab_completion from /etc/bash_completion.d/
if [[ -f /etc/bash_completion.d/tab_completion.sh ]]
then
	sudo /bin/rm /etc/bash_completion.d/tab_completion.sh
	complete -r create connect plug add rename delete
	echo "---tab_completion uninstalled---";
	echo "--------------------------------";
	echo ${YELLOW} "restart your terminal to apply changes";
else
	echo "--tab_completion is not installed--";
fi