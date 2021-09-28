#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib3
import certifi
import importlib
import json
import os
import sys
import requests

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
			'Content-Type': 'application/json',
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
	token=0 #Токен
	message_id=0 #message id
	listcommand=[] #Лист комманд
	stickerid=False #Стикер id
	prefix='/' #Префикс
	def setToken(self, token): #Установка токена
		self.token = token
		print ('[Успешно :)] [Токен => {0}]'.format(token))
	def getToken(self): #Получение токена
		return 'https://api.telegram.org/bot{0}/'.format(self.token)
	def checkToken(token): #Проверка токена
		json_response = pyTelegramApi.request(token , 'getMe')
		if json_response['ok'] == True:
			print ('[Успешно :)] [Проверка => OK]')
			pyTelegramApi.getUpdates(token)
		else:
			print ('[Ошибка :(] [Проверка => Неверный токен]')
	def request(token, method, fields = {}): #Запрос к серверу и возвращение
		https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
		r = https.request('GET', token + method, fields)
		return json.loads(r.data.decode('utf-8'))
	def addcommand (name, module): #Добавить команду
		pyTelegramApi.listcommand.append(pyTelegramApi.prefix+name + '=' + module)
	def sendMessage_id(self, text = 'Привет', chatid = ''): #отправить сообщение с chatid
		if chatid == '':
			chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendMessage', {'chat_id' : chatid, 'text' : text})
	def sendMessage(self, text = 'Привет'): #отправить сообщение без chatid
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendMessage', {'chat_id' : chatid, 'text' : text})
	def sendPhoto_ByUrl(self , PhotoUrl): #Отправка фото по url адресу
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendPhoto', {'chat_id' : chatid, 'photo' : PhotoUrl})
	def getChatId(self): #Возвращаем chatid от сообщение
		json_response = pyTelegramApi.request(pyTelegramApi.getToken(self), 'getUpdates', {'offset' : -1})
		try:
			return json_response['result'][0]['message']['chat']['id']
		except:
			return json_response['result'][0]['callback_query']['message']['chat']['id']
	def getText(self): #Возвращаем текст
		json_response = pyTelegramApi.request(pyTelegramApi.getToken(self), 'getUpdates', {'offset' : -1})
		if json_response['result'][0]['message']['text']:
			return json_response['result'][0]['message']['text']
		else:
			json_response['result'][0]['message']['chat']['text']
	def sendMessage_array (self, text = ['Привет1', 'Привет2']):
		chatid = pyTelegramApi.getChatId(self)
		txt = ''
		for str in text:
			txt += str + "\n"
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendMessage', {'chat_id' : chatid, 'text' : txt})
	def getlist (): #Получить список команд
		return pyTelegramApi.listcommand
	def sendSticker (self, StickerId): #Отправить стикер
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendSticker', {'chat_id' : chatid, 'sticker' : StickerId})
	def getStickerId (): #Возвращаем id стикера
		return pyTelegramApi.stickerid
	def DeleteMessage(self,id):
		chatid=pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'deleteMessage', {'chat_id' : chatid,'message_id': id})
	def getUpdates(token):#Бесконечный цикл
		sys.setrecursionlimit(10000) #Кол-во запросов
		json_response = pyTelegramApi.request(token, 'getUpdates', {'offset' : -1})
		try:
			chatid = json_response['result'][0]['message']['chat']['id']
		except:
			try:
				if pyTelegramApi.message_id != json_response['result'][0]['callback_query']['message']['message_id']:
					json_response['result'][0]['callback_query']['data']
					chatid = json_response['result'][0]['callback_query']['message']['chat']['id']
					message_id = json_response['result'][0]['callback_query']['message']['message_id']
					func=json_response['result'][0]['callback_query']['data']
					execute=func.split('@')[0]
					func=func.split('@')[1]
					func=getattr(importlib.import_module(func), execute)
					pyTelegramApi.request(token, 'deleteMessage', {'chat_id' : chatid,'message_id': message_id})
					pyTelegramApi.message_id = json_response['result'][0]['callback_query']['message']['message_id']
					func()
			except:
				pass
			pyTelegramApi.getUpdates(token)
		if pyTelegramApi.message_id != json_response['result'][0]['message']['message_id']:
			for text in json_response['result'][0]['message']:
				if text == 'text':
					text = json_response['result'][0]['message']['text']
					for str in pyTelegramApi.getlist():
						module = str.split('=')[1]
						command = str.split('=')[0]
						text_gen = text.split('@')
						if command == text_gen[0]:
							print('[Успешно :)] [user] [Модуль выполнен => {0}]'.format(module))
							importlib.import_module('bot.modules.' + module).main()
						elif command == text.split(' ')[0]:
							print('[Успешно :)] [user] [Модуль выполнен => {0}]'.format(module))
							importlib.import_module('bot.modules.' + module).main()
					pyTelegramApi.message_id = json_response['result'][0]['message']['message_id']
					pyTelegramApi.getUpdates(token)
					return
				elif text == 'sticker':
					pyTelegramApi.stickerid = json_response['result'][0]['message']['sticker']['file_id']
		pyTelegramApi.message_id = json_response['result'][0]['message']['message_id']
		pyTelegramApi.getUpdates(token)
