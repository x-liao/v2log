#!/usr/bin/env bash

BASE_PATH=$(cd `dirname $0`; pwd)
logs_path="${BASE_PATH}/logs"
rm -rf $v2log/*

get_log(){
	# 使用scp拷贝文件夹
	name=$1
	host=$2
	port=$3
	passwd=$4
	echo sshpass -p $passwd scp -r $host:/usr/local/v2log_count/count_log/ $logs_path/${name}
	sshpass -p $passwd scp -r $host:/usr/local/v2log_count/count_log/ $logs_path/${name}
}

err='''
HongKong ssh root@10.0.0.1 -p 22 passwd
'''

hosts='''
HongKong ssh root@10.0.0.1 -p 22 passwd
'''

IFS=$'\n'
for i in $hosts; do
	name=$(echo $i | awk '{print $1}')
	host=$(echo $i | awk '{print $3}')
	port=$(echo $i | awk '{print $5}')
	passwd=$(echo $i | awk '{print $6}')
	get_log  $name $host $port $passwd
done

