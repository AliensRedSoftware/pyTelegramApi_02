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
	def keyboard(self, desc='Описание', items=''): #Возвращаем inline клавиаутуру
		chat_id = str(pyTelegramApi.getChatId(self))
		headers={
			'Content-Type' : 'application/json',
		}
		data = '{"chat_id":'+chat_id+', "text":"'+desc+'", "reply_markup": {'+items+'}}"'
		data=data.encode('utf-8')
		requests.post(pyTelegramApi.getToken(self)+'sendMessage', headers=headers, data=data)
	def UpdateRedirect(selected): #Обновить пути
		InlineKeyBoard.Redirect=selected
	def getRedirect(name):
		#Кнопки
		B=InlineKeyBoard.UXBtn({'txt': '⬅️','func':InlineKeyBoard.Redirect+'@'+name}) #Назад
		H=InlineKeyBoard.UXBtn({'txt':'🏠','func':'main@'+name}) #Домой
		K=InlineKeyBoard.UXBtn({'txt':'❌','func':'kill@'+name}) #Покончить
		#Ячейки
		return InlineKeyBoard.UXItem(B+','+H+','+K)

class pyTelegramApi:

	bots=[]

	def setToken(name, token): #Установка токена
		token='https://api.telegram.org/bot{0}/'.format(token)
		if	pyTelegramApi.checkToken(name, token) == False:
			sys.exit()
		else:
			bot=pyTelegramApi.getBot(name)
			bot.token=token
			#bots.append(name)
			#print('[THREAD] [CFG] [@{0}] => OK...'.format(name))

	def getToken(name): #Получение токена
		bot=pyTelegramApi.getBot(name)
		return bot.token

	def getBot(name):
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

	def sendMessage_id(txt = 'Привет', chatid = '', cfg=False): #отправить сообщение с chatid
		#if chatid == '':
		#	chatid = pyTelegramApi.getChatId(self)
		bot=pyTelegramApi.getBot(cfg.bot.name)
		pyTelegramApi.request(bot.token, 'sendMessage', {'chat_id' : chatid, 'text' : txt})

	def sendMessage(txt = 'Привет', cfg=False): #отправить сообщение без chatid
		if	cfg == False:
			cfg=pyTelegramApi.getCfgThread()
		bot=pyTelegramApi.getBot(cfg.bot.name)
		pyTelegramApi.request(bot.token, 'sendMessage', {'chat_id' : cfg.room.id, 'text' : txt})

	def sendPhotoId_ByUrl(self, PhotoUrl, chatid): #Отправка фото по url адресу
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendPhoto', {'chat_id' : chatid, 'photo' : PhotoUrl})

	def getChatId(self): #Возвращаем chatid от сообщение
		json_response = pyTelegramApi.request(pyTelegramApi.getToken(self), 'getUpdates', {'offset' : -1})
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

	def thread(name):
		config='a' + uuid.uuid4().hex
		cfg=os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + config + '.py'
		Path(cfg).touch()
		cfg = open(cfg, 'r+')
		cfg.write(open(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'cfg.py', 'r').read().strip())
		cfg.close()
		_thread.start_new_thread(pyTelegramApi.getUpdates,(name, config))
		return config

	def getUpdatesThreads(name, cfg=False):
		time.sleep(1)
		cfg=pyTelegramApi.thread(name)
		pyTelegramApi.getUpdatesThreads(name, cfg)

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

	def getCfgThread():
		for bot in os.scandir(os.getcwd() + os.sep + 'bots'):
			for thread in os.scandir(os.getcwd() + os.sep + 'bots' + os.sep + bot.name + os.sep + 'threads'):
				config=os.path.splitext(os.path.basename(thread.name))[0]
				cfg=pyTelegramApi.getModuleCfgThread(bot.name, config)
				thread=cfg.THREAD
				if	_thread.get_ident() == thread:
					return cfg
		return False

	def DestroyUseThread(bot, ID):
		list=[]
		for active in bot.active:
			if	active != ID:
				list+=active
		bot.active=list

	def clearCache(name, config):
		try:
			os.remove(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + config + '.py')
			os.remove(os.getcwd() + os.sep + 'bots' + os.sep + name + os.sep + 'threads' + os.sep + '__pycache__' + os.sep + config + '.cpython-38.pyc')
		except:
			pass

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

	def getUpdates(name, config):#Бесконечный цикл
		try:
			cfg=pyTelegramApi.getModuleCfgThread(name, config)
			cfg.THREAD=_thread.get_ident()
			cfg.bot.name=name
			token=pyTelegramApi.getToken(name)
			json_response = pyTelegramApi.request(token, 'getUpdates', {'offset' : -1})
			pyTelegramApi.sniffer(cfg, json_response)
			cfg=pyTelegramApi.getModuleCfgThread(name, config)
			bot=pyTelegramApi.getBot(name)
			if	pyTelegramApi.isIgnoreThread(bot, json_response):
					return _thread.exit()
			if	pyTelegramApi.isUseThread(bot, json_response):
				try:
					chatid=json_response['result'][0]['callback_query']['message']['chat']['id']
					pyTelegramApi.message_ids.append(json_response['result'][0]['callback_query']['message']['message_id'])
				except:
					chatid=json_response['result'][0]['message']['chat']['id']
					bot.message_ids.append(json_response['result'][0]['message']['message_id'])
				if	pyTelegramApi.getNameModule(name, json_response):
					pyTelegramApi.sendMessage('Пожалуйста ожидайте завершение прошлого сеанса', cfg)
				pyTelegramApi.clearCache(name, config)
				return _thread.exit()
			else:
				push=True
				try:
					ID=json_response['result'][0]['callback_query']['message']['from']['id']
				except:
					ID=json_response['result'][0]['message']['from']['id']
				for active in bot.active:
					if	active == ID:
						push=False
				if	push:
					bot.active+=[ID]
			try:
				chatid = json_response['result'][0]['message']['chat']['id']
			except:
				try:
					json_response['result'][0]['callback_query']['data']
					chatid = json_response['result'][0]['callback_query']['message']['chat']['id']
					message_id = json_response['result'][0]['callback_query']['message']['message_id']
					func=json_response['result'][0]['callback_query']['data']
					module=func.split('@')[0]
					func=func.split('@')[1]
					try:
						func=getattr(importlib.import_module(func), module)
						pyTelegramApi.sniffer(cfg, json_response)
						pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : message_id})
						bot.message_ids.append(json_response['result'][0]['callback_query']['message']['message_id'])
						func()
					except:
						pass
					finally:
						print('[Успешно :)] [user] [Модуль выполнен => {0}]'.format(module))
				except:
					pass
				if	json_response['result']:
					pyTelegramApi.message_ids.append(json_response['result'][0]['message']['message_id'])
				pyTelegramApi.clearCache(name, config)
				pyTelegramApi.DestroyUseThread(bot, ID)
				return _thread.exit()
			for	txt in json_response['result'][0]['message']:
				if	txt == 'text':
					txt = json_response['result'][0]['message']['text']
					try:
						chatid = json_response['result'][0]['message']['chat']['id']
						message_id = json_response['result'][0]['message']['message_id']
					except:
						chatid = json_response['result'][0]['callback_query']['message']['chat']['id']
						message_id = json_response['result'][0]['callback_query']['message']['message_id']
					for str in pyTelegramApi.getlist(name):
						module = str.split('=')[1]
						cmd = str.split('=')[0]
						cmdm=cmd + '=' + module
						txt_gen = txt.split('@')
						if	cmd == txt_gen[0]:
							try:
								print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
								pyTelegramApi.sniffer(cfg, json_response)
								pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : message_id})
								importlib.import_module('bots.' + name + '.modules.' + module).main(name, cfg)
							except:
								print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => FAILED!...".format(cfg.THREAD, name, cmdm))
							finally:
								print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
								try:
									print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
									importlib.import_module('bots.' + name + '.modules.' + module).exit(name, cfg)
								except:
									print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => FAILED!...".format(cfg.THREAD, name, cmdm))
								finally:
									bot.message_ids.append(json_response['result'][0]['message']['message_id'])
									print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
						elif cmd == txt.split(' ')[0]:
							try:
								print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
								pyTelegramApi.sniffer(cfg, json_response)
								pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : message_id})
								importlib.import_module('bots.' + name + '.modules.' + module).main(name, cfg)
							except:
								print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => FAILED!...".format(cfg.THREAD, name, cmdm))
							finally:
								print("[THREAD] [{0}] [@{1}] [{2}] [MAIN] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
								try:
									print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => CLONE...".format(cfg.THREAD, name, cmdm))
									importlib.import_module('bots.' + name + '.modules.' + module).exit(name, cfg)
								except:
									print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => FAILED!...".format(cfg.THREAD, name, cmdm))
								finally:
									bot.message_ids.append(json_response['result'][0]['message']['message_id'])
									print("[THREAD] [{0}] [@{1}] [{2}] [EXIT] [PROCCESS] => SUCCESS!...".format(cfg.THREAD, name, cmdm))
					pyTelegramApi.clearCache(name, config)
					pyTelegramApi.DestroyUseThread(bot, ID)
					return _thread.exit()
		except:
			pass
		pyTelegramApi.clearCache(name, config)
		return _thread.exit()