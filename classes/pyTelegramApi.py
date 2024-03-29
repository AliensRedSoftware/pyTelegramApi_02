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
		bot=pyTelegramApi.getBot()
		pyTelegramApi.request(bot.token, 'sendMessage', {'chat_id' : room, 'text' : txt})

	def sendMessage_array(arr = ['Привет1', 'Привет2'], cfg=False):
		if	not cfg:
			cfg=pyTelegramApi.getCfgBot()
		bot=pyTelegramApi.getBot()
		txt = ''
		for str in arr:
			txt += str + "\n"
		pyTelegramApi.request(bot.token, 'sendMessage', {'chat_id' : cfg.room.id, 'text' : txt})

class user:

	def getById(id):
		bot=pyTelegramApi.getBot()
		return pyTelegramApi.request(bot.token, 'getChat', {'chat_id' : id})

class env:
	pass

class pyTelegramApi:

	bots={}

	def InitThread(name):
		if	os.path.isdir(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads') == False:
			os.mkdir(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads')
		pyTelegramApi.clearCache(name)

	def setToken(name): #Установка токена
		token='https://api.telegram.org/bot{0}/'.format(open(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'token', 'r').read().strip())
		if	pyTelegramApi.checkToken(name, token) == False:
			print('[THREAD] [CONNECT] [@{0}] => FAILED...'.format(name))
			_thread.exit()
		else:
			bot=pyTelegramApi.getBot(name)
			bot.token=token
			print('[THREAD] [CONNECT] [@{0}] => OK...'.format(name))

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
		if	pyTelegramApi.request(token, 'getMe'):
			return True
		else:
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

	def getlist(): #Получить список команд
		bot=pyTelegramApi.getBot()
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
			#txt
			try:
				json_response['result'][0]['message']['text']
				cfg.msg.txt=json_response['result'][0]['message']['text']
			except:
				cfg.msg.txt=json_response['result'][0]['message']['chat']['text']
			cfg.user.id=json_response['result'][0]['message']['from']['id']
			#room
			cfg.room.id=json_response['result'][0]['message']['chat']['id']
			cfg.room.type=json_response['result'][0]['message']['chat']['type']
			try:
				cfg.sticker.id=json_response['result'][0]['message']['sticker']['file_id']
			except:
				pass
		except:
			try:
				json_response['result'][0]['callback_query']['message']['message_id']
				#msg
				cfg.msg.id=json_response['result'][0]['callback_query']['message']['message_id']
				#txt
				try:
					json_response['result'][0]['callback_query']['message']['text']
					cfg.msg.txt=json_response['result'][0]['callback_query']['message']['text']
				except:
					cfg.msg.txt=json_response['result'][0]['callback_query']['message']['chat']['text']
				cfg.user.id=json_response['result'][0]['callback_query']['message']['from']['id']
				#room
				cfg.room.id=json_response['result'][0]['callback_query']['message']['chat']['id']
				cfg.room.type=json_response['result'][0]['callback_query']['message']['chat']['type']
				try:
					cfg.sticker.id=json_response['result'][0]['callback_query']['message']['sticker']['file_id']
				except:
					pass
			except:
				pass
		return cfg

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

	def getCfgBot(name=False):
		bot=pyTelegramApi.getBot(name)
		for user in bot.cfg:
			if	bot.cfg[user].THREAD == _thread.get_ident():
				return bot.cfg[user]
		return False

	def isUsesUser(json_response):
		user=pyTelegramApi.getUserId(json_response)
		try:
			bot=pyTelegramApi.getBot()
			bot.cfg[user]
			return True
		except:
			return False

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

	def isModule(json_response):
		try:
			json_response['result'][0]['callback_query']['data']
			func=json_response['result'][0]['callback_query']['data']
			module=func.split('@')[0]
			func=func.split('@')[1]
			return module
		except:
			try:
				txt = json_response['result'][0]['message']['text']
				for str in pyTelegramApi.getlist():
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

	def isIgnoreMsg(json_response):
		bot=pyTelegramApi.getBot()
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

	def getRoomId(json_response):
		try:
			json_response['result'][0]['callback_query']['message']['chat']['id']
			return json_response['result'][0]['callback_query']['message']['chat']['id']
		except:
			json_response['result'][0]['message']['chat']['id']
			return json_response['result'][0]['message']['chat']['id']
		return False


	def pool(bot, cfg):
		name=cfg.name
		try:
			print("[THREAD] [{0}] [@{1}] [POOL] [PROCCESS] => CLONE...".format(cfg.THREAD, name))
			importlib.import_module('bots.' + name + '.behavior').pool(cfg)
			bot.message_ids.append(cfg.msg.id)
			print("[THREAD] [{0}] [@{1}] [POOL] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name))
		except:
			pass

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
			#данные сообщение
			#cfg=pyTelegramApi.sniffer(cfg, json_response)
			#cfg.THREAD=_thread.get_ident()
			#bot
			#cfg.name=name
			#bot cfg
			#cfg.opt.name=config
			#bot.cfg[user]=cfg
			#pyTelegramApi.pool(bot, cfg)
		except:
			pass
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
				msg.sendMessageById('Ошибка использование меню пожалуйста перезапустите меню...', pyTelegramApi.getRoomId(json_response))
		except:
			if	pyTelegramApi.isIgnoreMsg(json_response):
				pyTelegramApi.bots.pop(_thread.get_ident())
				return _thread.exit()
			if	pyTelegramApi.isUsesUser(json_response):
				#pyTelegramApi.bots.pop(_thread.get_ident())
				if	pyTelegramApi.isModule(json_response):
					bot.message_ids.append(pyTelegramApi.getMessageId(json_response))
					msg.sendMessageById('Пожалуйста ожидайте завершение прошлого сеанса', pyTelegramApi.getRoomId(json_response))
				return _thread.exit()
			else:
				#cfg
				config=pyTelegramApi.newCfgThread(name)
				cfg=importlib.import_module('bots.' + name + '.threads.' + config)
				#данные сообщение
				cfg=pyTelegramApi.sniffer(cfg, json_response)
				cfg.THREAD=_thread.get_ident()
				#bot
				cfg.name=name
				#bot cfg
				cfg.env.name=config
				bot.cfg[cfg.user.id]=cfg
				pyTelegramApi.deleteCfg(name, config)
				#Наш общий
				pyTelegramApi.pool(bot, cfg)
				#pool модульный
				for str in pyTelegramApi.getlist():
					module = str.split('=')[1]
					try:
						bot.message_ids.append(pyTelegramApi.getMessageId(json_response))
						print("[THREAD] [{0}] [@{1}] [{2}] [POOL] [PROCCESS] => CLONE...".format(cfg.THREAD, name, module))
						importlib.import_module('bots.' + name + '.modules.' + module).pool(cfg)
						print("[THREAD] [{0}] [@{1}] [{2}] [POOL] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, module))
					except:
						pass
				for	txt in json_response['result'][0]['message']:
					try:
						json_response['result'][0]['message']['text']
						if	txt == 'text':
							txt = json_response['result'][0]['message']['text']
							for str in pyTelegramApi.getlist():
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
									except:
										pass
								elif cmd == txt.split(' ')[0]:
									try:
										bot.message_ids.append(pyTelegramApi.getMessageId(json_response))
										print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
										pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : cfg.room.id, 'message_id' : cfg.msg.id})
										importlib.import_module('bots.' + name + '.modules.' + module).main(cfg)
										print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
									except:
										pass
					except:
						pass
		if	cfg.InlineKeyBoard.active == False:
			bot.cfg.pop(user)
			pyTelegramApi.bots.pop(_thread.get_ident())
		return _thread.exit()

