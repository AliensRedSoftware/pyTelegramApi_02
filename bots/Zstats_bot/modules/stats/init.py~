#!/usr/bin/env python3
import classes.pyTelegramApi as api
import classes.extensions as ext
import os
from pathlib import Path

max=10

def add(cfg):
	chat=os.path.dirname(__file__) + os.sep + 'supergroups' + os.sep + str(cfg.room.id)
	user=os.path.dirname(__file__) + os.sep + 'supergroups' + os.sep + str(cfg.room.id) + os.sep + str(cfg.user.id)
	count=os.path.dirname(__file__) + os.sep + 'supergroups' + os.sep + str(cfg.room.id) + os.sep + str(cfg.user.id) + os.sep + 'count'
	if	os.path.isdir(chat) == False:
		os.mkdir(chat)
	if	os.path.isdir(user) == False:
		os.mkdir(user)
	if	os.path.isfile(count) == False:
		Path(count).touch()
	count=Path(count)
	#add
	count.write_text(str(eval("{0} + 1".format(count.read_text()))))

def	pool(cfg):
	if	cfg.room.type == 'supergroup':
		add(cfg)

def getStatsByArray(cfg):
	chat=os.path.dirname(__file__) + os.sep + 'supergroups' + os.sep + str(cfg.room.id)
	if	os.path.isdir(chat) == False:
		api.msg.sendMessage('Не удается найти супергруппу :(')
	else:
		arr=[]
		list={}
		i=-1
		for user in os.scandir(chat):
			count=os.path.dirname(__file__) + os.sep + 'supergroups' + os.sep + str(cfg.room.id) + os.sep + str(user.name) + os.sep + 'count'
			list[user.name]=int(open(count).read())
		list=ext.orderDict(list, True)
		arr.append('Топ {0} пользователей нашего чата :)'.format(max))
		arr.append('---')
		for u in list:
			i+=1
			if	i < max:
				info=api.user.getById(u)
				name=''
				try:
					info['result']['first_name']
					name+=info['result']['first_name']
				except:
					pass
				try:
					info['result']['last_name']
					name+=' '
					name+=info['result']['last_name']
				except:
					pass
				try:
					info['result']['username']
					arr.append("{0} -> [{1}] [@{2}] = [{3} кол-во]".format(i, name, info['result']['username'], list[u]))
				except:
					arr.append("{0} -> [{1}] = [{2} кол-во]".format(i, name, list[u]))
		return arr

def init(cfg):
	if	cfg.room.type == 'supergroup':
		api.msg.sendMessage_array(getStatsByArray(cfg))
	else:
		api.msg.sendMessage('Пожалуйста используйте команду в супергруппе!')

def main(cfg):
	init(cfg)
