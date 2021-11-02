import bot.classes.pyTelegramApi as api

def main(token):
	print(api.msg.id)
	api.pyTelegramApi.setToken(api, token) #Установка токена
	api.pyTelegramApi.prefix = '$' #Установка префикса
	#Команды
	api.pyTelegramApi.addcommand('str', 'str.str')
	api.pyTelegramApi.addcommand('getStickerId', 'sticker.sticker')
	api.pyTelegramApi.addcommand('sendSticker', 'sticker.sendSticker')
	api.pyTelegramApi.addcommand('art2d', 'fun.art2d')
	#Меню
	api.pyTelegramApi.addcommand('start', 'system.ver')
	api.pyTelegramApi.addcommand('menu', 'system.ver')
	api.pyTelegramApi.addcommand('help', 'system.ver')
	#Парсинг новостей
	api.pyTelegramApi.addcommand('ixbt' , 'news.ixbt')
	api.pyTelegramApi.getUpdates(api.pyTelegramApi.getToken(api))
