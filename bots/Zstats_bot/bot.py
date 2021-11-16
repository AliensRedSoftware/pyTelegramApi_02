import classes.pyTelegramApi as api

token=''
listcommand=[] #Лист комманд
prefix='/' #Префикс
message_ids=[]
cfg={} # cfg threads...

def main(name, token):
	api.pyTelegramApi.setToken(name, token) #Установка токена
	api.pyTelegramApi.setPrefix(name, '$') #Установка префикса
	#Команды
	api.pyTelegramApi.addcommand(name, 'stats', 'stats.init')
	#Start proccess threads...
	api.pyTelegramApi.InitThread(name)
	api.pyTelegramApi.thread(name)
