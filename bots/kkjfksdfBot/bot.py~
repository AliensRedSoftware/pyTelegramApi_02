import classes.pyTelegramApi as api
import importlib

token=''
listcommand=[] #Лист комманд
prefix='/' #Префикс

def main(name, token):
	api.pyTelegramApi.setToken(name, token) #Установка токена
	api.pyTelegramApi.setPrefix(name, '$') #Установка префикса
	#Команды
	api.pyTelegramApi.addcommand(name, 'str', 'str.str')
	#api.pyTelegramApi.addcommand(name, 'getStickerId', 'sticker.sticker')
	#api.pyTelegramApi.addcommand(name, 'sendSticker', 'sticker.sendSticker')
	#api.pyTelegramApi.addcommand(name, 'sendStickerById', 'sticker.sendStickerById')
	#api.pyTelegramApi.addcommand(name, 'art2d', 'fun.art2d')
	#api.pyTelegramApi.addcommand(name, 'about', 'system.about')
	#Меню
	#api.pyTelegramApi.addcommand(name, 'start', 'system.ver')
	#api.pyTelegramApi.addcommand(name, 'menu', 'system.ver')
	#api.pyTelegramApi.addcommand(name, 'help', 'system.ver')
	#Парсинг новостей
	#api.pyTelegramApi.addcommand(name, 'ixbt', 'news.ixbt')
	#Start proccess threads...
	api.pyTelegramApi.getUpdatesThreads(name)
