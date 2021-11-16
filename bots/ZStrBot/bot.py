import classes.pyTelegramApi as api

token		=	'undefined'
listcommand	=	[]	#Лист комманд
prefix		=	'/'	#Префикс
message_ids	=	[]
cfg			=	{}	# cfg threads...

def main(name):
	api.pyTelegramApi.setToken(name) #Установка токена
	api.pyTelegramApi.setPrefix(name, '$') #Установка префикса
	#Команды
	#Start proccess threads...
	api.pyTelegramApi.InitThread(name)
	api.pyTelegramApi.thread(name)
