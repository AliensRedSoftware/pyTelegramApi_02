#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib3
import certifi
import importlib
import json
import sys
import requests
import _thread

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
class sticker:
	id=0
	def sendById(self, id): #Отправить стикер
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendSticker', {'chat_id' : chatid, 'sticker' : id})
	def send(self): #Отправить стикер
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendSticker', {'chat_id' : chatid, 'sticker' : sticker.id})
class msg:
	id=0
class user:
	id=0
class pyTelegramApi:
	token=0 #Токен
	prefix='/' #Префикс
	listcommand=[] #Лист комманд
	def setToken(self, token): #Установка токена
		self.token = token
		print('[Успешно :)] [Токен => {0}]'.format(token))
		if	pyTelegramApi.checkToken(pyTelegramApi.getToken(self)) == False:
			sys.exit()
	def getToken(self): #Получение токена
		return 'https://api.telegram.org/bot{0}/'.format(self.token)
	def	checkToken(token): #Проверка токена
		json_response = pyTelegramApi.request(token, 'getMe')
		if	json_response['ok'] == True:
			print('[Успешно :)] [Проверка => OK]')
			return True
		else:
			print('[Ошибка :(] [Проверка => Неверный токен]')
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
	def addcommand(name, module): #Добавить команду
		pyTelegramApi.listcommand.append(pyTelegramApi.prefix+name + '=' + module)
		print("[Успешно :)] [module] [Load] => {0}".format(pyTelegramApi.prefix+name + '=' + module))
	def sendMessage_id(self, txt = 'Привет', chatid = ''): #отправить сообщение с chatid
		if chatid == '':
			chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendMessage', {'chat_id' : chatid, 'text' : txt})
	def sendMessage(self, txt = 'Привет'): #отправить сообщение без chatid
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendMessage', {'chat_id' : chatid, 'text' : txt})
	def sendPhotoId_ByUrl(self, PhotoUrl, chatid): #Отправка фото по url адресу
		_thread.start_new_thread(pyTelegramApi.request,(pyTelegramApi.getToken(self), 'sendPhoto', {'chat_id' : chatid, 'photo' : PhotoUrl}))
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
	def sendMessage_array(self, arr = ['Привет1', 'Привет2']):
		chatid = pyTelegramApi.getChatId(self)
		txt = ''
		for str in arr:
			txt += str + "\n"
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendMessage', {'chat_id' : chatid, 'text' : txt})
	def getlist(): #Получить список команд
		return pyTelegramApi.listcommand
	def DeleteMessageId(self,id): # del Msg
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'deleteMessage', {'chat_id' : chatid, 'message_id' : id})
	def sniffer(json_response):
		try:
			json_response['result'][0]['message']['message_id']
			#msg
			msg.id=json_response['result'][0]['message']['message_id']
			user.id=json_response['result'][0]['message']['from']['id']
			try:
				sticker.id=json_response['result'][0]['message']['sticker']['file_id']
			except:
				pass
		except:
			try:
				#msg
				msg.id=json_response['result'][0]['callback_query']['message']['message_id']
				user.id=json_response['result'][0]['callback_query']['message']['from']['id']
				try:
					sticker.id=json_response['result'][0]['callback_query']['message']['sticker']['file_id']
				except:
					pass
			except:
				pass
	def getUpdates(token):#Бесконечный цикл
		try:
			json_response = pyTelegramApi.request(token, 'getUpdates', {'offset' : -1})
			try:
				chatid = json_response['result'][0]['message']['chat']['id']
			except:
				try:
					if	msg.id != json_response['result'][0]['callback_query']['message']['message_id']:
						json_response['result'][0]['callback_query']['data']
						chatid = json_response['result'][0]['callback_query']['message']['chat']['id']
						message_id = json_response['result'][0]['callback_query']['message']['message_id']
						func=json_response['result'][0]['callback_query']['data']
						execute=func.split('@')[0]
						func=func.split('@')[1]
						func=getattr(importlib.import_module(func), execute)
						pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : message_id})
						func()
				except:
					pass
				#Нюхаем значение для быстрого хода (HACK)
				if	json_response['result']:
					pyTelegramApi.sniffer(json_response)
				pyTelegramApi.getUpdates(token)
			if	msg.id != json_response['result'][0]['message']['message_id']:
				for	txt in json_response['result'][0]['message']:
					if	txt == 'text':
						txt = json_response['result'][0]['message']['text']
						try:
							chatid = json_response['result'][0]['message']['chat']['id']
							message_id = json_response['result'][0]['message']['message_id']
						except:
							chatid = json_response['result'][0]['callback_query']['message']['chat']['id']
							message_id = json_response['result'][0]['callback_query']['message']['message_id']
						for str in pyTelegramApi.getlist():
							module = str.split('=')[1]
							command = str.split('=')[0]
							txt_gen = txt.split('@')
							if	command == txt_gen[0]:
								pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : message_id})
								print('[Успешно :)] [user] [Модуль выполнен => {0}]'.format(module))
								importlib.import_module('bot.modules.' + module).main()
							elif command == txt.split(' ')[0]:
								pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid, 'message_id' : message_id})
								print('[Успешно :)] [user] [Модуль выполнен => {0}]'.format(module))
								importlib.import_module('bot.modules.' + module).main()
						#Нюхаем значение для быстрого хода (HACK)
						pyTelegramApi.sniffer(json_response)
						pyTelegramApi.getUpdates(token)
			#Нюхаем значение для быстрого хода (HACK)
			pyTelegramApi.sniffer(json_response)
		except:
			pass
		pyTelegramApi.getUpdates(token)
