import bot.classes.pyTelegramApi as api

def main():
	if api.pyTelegramApi.getStickerId() == False:
		api.pyTelegramApi.sendMessage(api, 'StickerId => ' + 'Не был найден id!')
	else:
		api.pyTelegramApi.sendMessage(api, 'StickerId => ' + api.pyTelegramApi.getStickerId())