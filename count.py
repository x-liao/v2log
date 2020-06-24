#!/usr/bin/env python3
import os
import sys
import json
import datetime
from collections import defaultdict

path = os.path.split(os.path.realpath(__file__))[0]
log_path = os.path.split(os.path.realpath(__file__))[0] + '/logs'

def exte(a,*endstring):
	array = map(a.endswith,endstring)
	if True in array:
		return True
	else:
		return False

def save_count_log(filename,data):
	with open(filename,'w') as f:
		f.write(data)

def get_files():
	type = '.json'
	files = []
	for dirpath,dirnames,filenames in os.walk(log_path):
		for name in filenames:
			if exte(name,type):
				json_file = os.path.join(dirpath, name)
				files.append(json_file)
	return files


files = get_files()
print('一共%d个文件'%len(files))

count_data = defaultdict(int)

i = 1
for name in files:
	print('正在处理第%d个文件'%i)
	i += 1
	with open(name, 'r') as f:
		data = f.read()

	data = json.loads(data)
	for item in data['data']:
		count_data[item['domain']] += item['count']


if count_data:
	create_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	date = datetime.datetime.now().strftime("%Y_%m_%d")
	filename = 'v2ray_count_%s.json'%(date)
	data = {'create_date':create_date,'data':count_data}
	save_count_log(filename,json.dumps(data))

data_str = ''
for key in data['data'].keys():
	data_str = data_str + key + ',' +  str(data['data'][key]) + '\n'

with open('data.txt', 'w') as f:
	f.write(data_str)