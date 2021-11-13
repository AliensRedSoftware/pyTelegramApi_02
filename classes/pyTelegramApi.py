#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib3
import certifi
import importlib
import json
import sys
import requests
import _thread
import time
import uuid
import os
from pathlib import Path

class InlineKeyBoard:

	ver=2
	Redirect=False #Редирект

	def UXBtn(data = {'txt':'нажми'}): #UXBtn
		txt=data['txt']
		try:
			url=data['url']
			vrm = '"text":"{0}", "url":"{1}"'.format(txt,url)
		except:
			try:
				func=data['func']
				vrm = '"text":"{0}", "callback_data": "{1}"'.format(txt,func)
			except:
				vrm = '"text":"{0}"'.format(txt)
		return "{"+vrm+"}"

	def UXItem(item=''): #UXItem
		vrm = '"inline_keyboard": [['+item+']]'
		return vrm

	def keyboard(desc='Описание', items='', cfg=False): #Возвращаем inline клавиаутуру
		if	cfg == False:
			cfg=pyTelegramApi.getCfgThread()
		bot=pyTelegramApi.getBot(cfg.bot.name)
		room = str(cfg.room.id)
		headers={
			'Content-Type' : 'application/json',
		}
		data = '{"chat_id":'+room+', "text":"'+desc+'", "reply_markup": {'+items+'}}"'
		data = data.encode('utf-8')
		try:
			data = json.loads(requests.post(bot.token+'sendMessage', headers=headers, data=data).text)
			if	data['ok'] == False:
				return False
			else:
				pyTelegramApi.sniffer(cfg, data)
				return data
		except:
			pass

	def UpdateRedirect(selected): #Обновить пути
		InlineKeyBoard.Redirect=selected

	def getRedirect(name):
		#Кнопки
		B=InlineKeyBoard.UXBtn({'txt': '⬅️','func':InlineKeyBoard.Redirect+'@'+name}) #Назад
		H=InlineKeyBoard.UXBtn({'txt':'🏠','func':'main@'+name}) #Домой
		K=InlineKeyBoard.UXBtn({'txt':'❌','func':'kill@'+name}) #Покончить
		#Ячейки
		return InlineKeyBoard.UXItem(B+','+H+','+K)

	def getCfgThread(name, json_response):
		try:
			user=json_response['result'][0]['message']['from']['id']
		except:
			user=json_response['result'][0]['callback_query']['message']['from']['id']
		for thread in os.scandir(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads'):
			config=os.path.splitext(os.path.basename(thread.name))[0]
			if	os.path.isfile(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + config + '.py'):
				cfg=pyTelegramApi.getModuleCfgThread(name, config)
				print(cfg.user.id)
				if	user == cfg.user.id:
					return cfg
		return False

class msg:

	def sendMessage(txt = 'Привет', cfg=False): #отправить сообщение без chatid
		if	not cfg:
			cfg=pyTelegramApi.getCfgBot()
		bot=pyTelegramApi.getBot()
		pyTelegramApi.request(bot.token, 'sendMessage', {'chat_id' : cfg.room.id, 'text' : txt})

	def sendMessageById(txt = 'Привет', room = '', cfg=False): #отправить сообщение с chatid
		if	room == '':
			if	cfg == False:
				cfg=pyTelegramApi.getCfgThread()
			room = cfg.room.id
		bot=pyTelegramApi.getBot(cfg.bot.name)
		pyTelegramApi.request(bot.token, 'sendMessage', {'chat_id' : room, 'text' : txt})

class pyTelegramApi:

	bots={}

	def InitThread(name):
		pyTelegramApi.clearCache(name)

	def setToken(name, token): #Установка токена
		token='https://api.telegram.org/bot{0}/'.format(token)
		if	pyTelegramApi.checkToken(name, token) == False:
			print('[THREAD] [CFG] [@{0}] => FAILED...'.format(name))
			sys.exit()
		else:
			bot=pyTelegramApi.getBot(name)
			bot.token=token
			print('[THREAD] [CFG] [@{0}] => OK...'.format(name))

	def getToken(name): #Получение токена
		bot=pyTelegramApi.getBot(name)
		return bot.token

	def getBot(name=False):
		if	not name:
			name=pyTelegramApi.bots[_thread.get_ident()]
		return importlib.import_module('bots.' + name + '.bot')

	def setPrefix(name, prefix='$'):
		bot=pyTelegramApi.getBot(name)
		bot.prefix=prefix

	def	checkToken(name, token): #Проверка токена
		json_response = pyTelegramApi.request(token, 'getMe')
		if	json_response['ok'] == True:
			print('[THREAD] [CONNECT] [@{0}] => OK...'.format(name))
			return True
		else:
			print('[THREAD] [CONNECT] [@{0}] => FAILED...'.format(name))
			return False

	def request(token, method, fields = {}): #Запрос к серверу и возвращение
		try:
			https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
			r = https.request('GET', token + method, fields)
			data=json.loads(r.data.decode('utf-8'))
			if	data['ok'] == False:
				return False
			else:
				return data
		except:
			return pyTelegramApi.request(token, method, fields)

	def addcommand(bot, name, module): #Добавить команду
		bot=importlib.import_module('bots.' + bot + '.bot')
		bot.listcommand.append(bot.prefix+name + '=' + module)
		print("[THREAD] [Успешно :)] [module] [Load] => {0}".format(bot.prefix+name + '=' + module))

	def sendPhotoId_ByUrl(self, PhotoUrl, chatid): #Отправка фото по url адресу
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendPhoto', {'chat_id' : chatid, 'photo' : PhotoUrl})

	def getChatId(json_response): #Возвращаем chatid от сообщение
		try:
			return json_response['result'][0]['message']['chat']['id']
		except:
			return json_response['result'][0]['callback_query']['message']['chat']['id']

	def getText(self): #Возвращаем текст
		json_response = pyTelegramApi.request(pyTelegramApi.getToken(self), 'getUpdates', {'offset' : -1})
		if	json_response['result'][0]['message']['text']:
			return json_response['result'][0]['message']['text']
		else:
			json_response['result'][0]['message']['chat']['text']

	def sendMessage_array(arr = ['Привет1', 'Привет2'], cfg=False):
		chatid = pyTelegramApi.getChatId(self)
		txt = ''
		for str in arr:
			txt += str + "\n"
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendMessage', {'chat_id' : chatid, 'text' : txt})

	def getlist(name): #Получить список команд
		bot=pyTelegramApi.getBot(name)
		return bot.listcommand

	def DeleteMessageId(name, id): # del Msg
		bot=pyTelegramApi.getBot(name)
		cfg=getCfgThread(name)
		pyTelegramApi.request(bot.token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : id})

	def sniffer(cfg, json_response):
		try:
			json_response['result'][0]['message']['message_id']
			#msg
			cfg.msg.id=json_response['result'][0]['message']['message_id']
			cfg.user.id=json_response['result'][0]['message']['from']['id']
			cfg.room.id=json_response['result'][0]['message']['chat']['id']
			try:
				cfg.sticker.id=json_response['result'][0]['message']['sticker']['file_id']
			except:
				pass
		except:
			try:
				json_response['result'][0]['callback_query']['message']['message_id']
				#msg
				cfg.msg.id=json_response['result'][0]['callback_query']['message']['message_id']
				cfg.user.id=json_response['result'][0]['callback_query']['message']['from']['id']
				cfg.room.id=json_response['result'][0]['callback_query']['message']['chat']['id']
				try:
					cfg.sticker.id=json_response['result'][0]['callback_query']['message']['sticker']['file_id']
				except:
					pass
			except:
				pass

	def newCfgThread(name):
		try:
			config='a' + uuid.uuid4().hex
			cfg=os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + config + '.py'
			Path(cfg).touch()
			cfg = open(cfg, 'r+')
			cfg.write(open(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'cfg.py', 'r').read().strip())
			cfg.close()
			return config
		except:
			pass
		return False

	def thread(name):
		try:
			thread=_thread.start_new_thread(pyTelegramApi.getUpdates, (name , ))
			pyTelegramApi.bots[thread]=name
		except:
			pass

	def getModuleCfgThread(name, config): # Return Module CFG thread...
		return importlib.import_module('bots.' + name + '.threads.' + config)

	def isUseThread(bot, json_response):
		try:
			ID=json_response['result'][0]['callback_query']['message']['from']['id']
		except:
			ID=json_response['result'][0]['message']['from']['id']
		for active in bot.active:
			if	active == ID:
				return True
		return False

	def getCfgBot(name=False):
		bot=pyTelegramApi.getBot(name)
		for user in bot.cfg:
			if	bot.cfg[user].THREAD == _thread.get_ident():
				return bot.cfg[user]
		return False

	def DestroyUseThread(bot, ID):
		list=[]
		for active in bot.active:
			if	active != ID:
				list+=active
		bot.active=list

	def deleteCfg(name, config):
		try:
			os.remove(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + config + '.py')
			os.remove(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + '__pycache__' + os.sep + config + '.cpython-38.pyc')
		except:
			pass

	def clearCache(name):
		for thread in os.scandir(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads'):
			thread=thread.name
			if	thread == '__pycache__':
				for py in os.scandir(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + thread):
					try:
						os.remove(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + '__pycache__' + os.sep + py.name)
						print("[DELETE] [__PYCACHE__] [@{0}] -> {1}".format(name, py.name))
					except:
						pass
				print("[CLEARCACHE] [__PYCACHE__] [@{0}] -> SUCCESS! :)".format(name))
			else:
				try:
					os.remove(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + thread)
					print("[DELETE] [THREAD] [@{0}] -> {1}".format(name, thread))
				except:
					pass
		print("[CLEARCACHE] [THREAD] [@{0}] -> SUCCESS! :)".format(name))

	def getNameModule(name, json_response):
		try:
			json_response['result'][0]['callback_query']['data']
			func=json_response['result'][0]['callback_query']['data']
			module=func.split('@')[0]
			func=func.split('@')[1]
			return module
		except:
			try:
				txt = json_response['result'][0]['message']['text']
				for str in pyTelegramApi.getlist(name):
					module = str.split('=')[1]
					command = str.split('=')[0]
					txt_gen = txt.split('@')
					if	command == txt_gen[0]:
						return module
					elif command == txt.split(' ')[0]:
						return module
			except:
				pass
		return False

	def isIgnoreThread(bot, json_response):
		for	id in bot.message_ids:
			try:
				json_response['result'][0]['message']['message_id']
				message_id=json_response['result'][0]['message']['message_id']
				if	id == message_id:
					return True
			except:
				try:
					json_response['result'][0]['callback_query']['message']['message_id']
					message_id=json_response['result'][0]['callback_query']['message']['message_id']
					if	id == message_id:
						return True
				except:
					pass
		return False

	def getUserId(json_response):
		try:
			json_response['result'][0]['callback_query']['message']['from']['id']
			return json_response['result'][0]['callback_query']['message']['from']['id']
		except:
			json_response['result'][0]['message']['from']['id']
			return json_response['result'][0]['message']['from']['id']
		return False

	def getMessageId(json_response):
		try:
			json_response['result'][0]['callback_query']['message']['message_id']
			return json_response['result'][0]['callback_query']['message']['message_id']
		except:
			json_response['result'][0]['message']['message_id']
			return json_response['result'][0]['message']['message_id']
		return False

	def getTypeQuery():
		try:
			json_response['result'][0]['callback_query']['message']['chat']['id']
			return 'InlineKeyBoard'
		except:
			try:
				json_response['result'][0]['message']['text']
				return 'msg'
			except:
				pass
		return 'undefined'

	def getUpdates(name):#Бесконечный цикл
		token=pyTelegramApi.getToken(name)
		try:
			json_response = pyTelegramApi.request(token, 'getUpdates', {'offset' : -1})
			pyTelegramApi.thread(name) # new start thread...
		except:
			pass
		bot=pyTelegramApi.getBot(name)
		user=pyTelegramApi.getUserId(json_response)
		try:
			#bot.cfg[user].THREAD=_thread.get_ident()
			cfg=bot.cfg[user]
			#bot.cfg[cfg.user.id]=cfg
		except:
			config=pyTelegramApi.newCfgThread(name)
			cfg=pyTelegramApi.getModuleCfgThread(name, config)
			cfg.opt.name=config
			cfg.THREAD=_thread.get_ident()
			cfg.name=name
			pyTelegramApi.sniffer(cfg, json_response)
			cfg=pyTelegramApi.getModuleCfgThread(name, config)
			bot.cfg[cfg.user.id]=cfg
			pyTelegramApi.deleteCfg(name, cfg.opt.name)
		try:
			json_response['result'][0]['callback_query']['data']
			#cfgThread=InlineKeyBoard.getCfgThread(name, json_response)
			if	cfgThread:
				print(cfgThread.InlineKeyBoard.active)
				print('SUCCESS')
				#func=json_response['result'][0]['callback_query']['data']
				#module=func.split('@')[0]
				#func=func.split('@')[1]
				#func=getattr(importlib.import_module(func), module)
				#pyTelegramApi.sniffer(cfg, json_response)
				#pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : message_id})
				#bot.message_ids.append(json_response['result'][0]['callback_query']['message']['message_id'])
				#func()
			else:
				msg.sendMessage('Ошибка использование меню пожалуйста перезапустите меню...', cfg)
		except:
			if	pyTelegramApi.isIgnoreThread(bot, json_response):
				return _thread.exit()
			if	cfg.THREAD != _thread.get_ident() and user == cfg.user.id:
				bot.message_ids.append(pyTelegramApi.getMessageId(json_response))
				if	pyTelegramApi.getNameModule(name, json_response):
					msg.sendMessage('Пожалуйста ожидайте завершение прошлого сеанса')
				return _thread.exit()
			else:
				#bot.message_ids.append(pyTelegramApi.getMessageId(json_response))
				for	txt in json_response['result'][0]['message']:
					try:
						json_response['result'][0]['message']['text']
						if	txt == 'text':
							txt = json_response['result'][0]['message']['text']
							for str in pyTelegramApi.getlist(name):
								module = str.split('=')[1]
								cmd = str.split('=')[0]
								cmdm=cmd + '=' + module
								txt_gen = txt.split('@')
								if	cmd == txt_gen[0]:
									try:
										bot.message_ids.append(pyTelegramApi.getMessageId(json_response))
										print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
										pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : cfg.room.id, 'message_id' : cfg.msg.id})
										importlib.import_module('bots.' + name + '.modules.' + module).main(cfg)
										print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
										try:
											print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
											importlib.import_module('bots.' + name + '.modules.' + module).exit(cfg)
											print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
										except:
											pass
									except:
										pass
								elif cmd == txt.split(' ')[0]:
									try:
										bot.message_ids.append(pyTelegramApi.getMessageId(json_response))
										print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
										pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : cfg.room.id, 'message_id' : cfg.msg.id})
										importlib.import_module('bots.' + name + '.modules.' + module).main(cfg)
										print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
										try:
											print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
											importlib.import_module('bots.' + name + '.modules.' + module).exit(cfg)
											print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
										except:
											pass
									except:
										pass
					except:
						pass
		
		if	cfg.InlineKeyBoard.active == False:
			bot.cfg.pop(user)
			pyTelegramApi.bots.pop(_thread.get_ident())
		print(pyTelegramApi.bots)
		return _thread.exit()

