import bot.classes.pyTelegramApi as api

def main():
	if api.sticker.id == False:
		api.pyTelegramApi.sendMessage(api, 'StickerId => ' + 'Не был найден id!')
	else:
		api.pyTelegramApi.sendMessage(api, 'StickerId => ' + api.sticker.id)
