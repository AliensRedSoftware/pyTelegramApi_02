#!/usr/bin/env python3

THREAD=False

name='undefined'

class InlineKeyBoard:
	active=False

class env:
	name='undefined'

class sticker:
	id=0
	def sendById(self, id):
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendSticker', {'chat_id' : chatid, 'sticker' : id})
	def send(self):
		chatid = pyTelegramApi.getChatId(self)
		pyTelegramApi.request(pyTelegramApi.getToken(self), 'sendSticker', {'chat_id' : chatid, 'sticker' : sticker.id})

class msg:
	id=0
	txt='undefined'

class room:
	id=0
	type='undefined'

class user:
	id=0
