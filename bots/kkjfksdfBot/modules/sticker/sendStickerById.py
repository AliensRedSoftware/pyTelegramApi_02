import bot.classes.pyTelegramApi as api

def main():
	TXT=api.pyTelegramApi.getText(api)
	selected=TXT.split(' ')
	try:
		api.sticker.sendById(api, selected[1])
	except:
		pass
