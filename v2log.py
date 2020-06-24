#!/usr/bin/env python3
import json
import os
import datetime

PATH = os.path.split(os.path.realpath(__file__))[0]
count_log_path = PATH + '/count_log'
access_log = '/var/log/v2ray/access.log'
error_log = '/var/log/v2ray/error.log'

def get_log(filename):
	try:
		with open(filename, 'r') as f:
			data = f.read()
	except:
		print('日志文件路径错误')
		exit(1)
	
	return data

def save_count_log(filename,data):
	with open(filename,'w') as f:
		f.write(data)

def clear_v2ray_log(filename):
	with open(filename, 'w') as f:
		f.write('')

if not os.path.exists(count_log_path):
	os.makedirs(count_log_path) 


data = get_log(access_log)
accepted_data = [item.split('accepted')[1].split()[0].split(':') for item in data.split('\n') if 'accepted' in item]
count_data = []

for item in accepted_data:
	dis = False
	for x in count_data:
		try:
			if item[0] == x['protocol'] and item[1] == x['domain'] and int(item[2]) == x['port']:
				count_data.remove(x)
				x['count'] += 1
				count_data.append(x)
				dis = True
		except:
			x = {'protocol':item[0],'domain':item[1],'port':int(item[2]),'count':1}
			count_data.append(x)
		

	if not dis:
		x = {'protocol':item[0],'domain':item[1],'port':int(item[2]),'count':1}
		count_data.append(x)

clear_v2ray_log(access_log)
clear_v2ray_log(error_log)

if count_data:
	create_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	date = datetime.datetime.now().strftime("%Y_%m_%d")
	filename = '%s/v2ray_count_%s.json'%(count_log_path,date)
	data = {'create_date':create_date,'data':count_data}
	save_count_log(filename,json.dumps(data))