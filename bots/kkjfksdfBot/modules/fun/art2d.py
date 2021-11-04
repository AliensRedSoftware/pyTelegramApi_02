import classes.pyTelegramApi as api
import random

def SendRandomWaifu2d(count=1): #Отправка рандомного картинки waifu2d
	chatid = api.pyTelegramApi.getChatId(api)
	if	count==1:
		api.pyTelegramApi.sendPhotoId_ByUrl(api, "https://www.thiswaifudoesnotexist.net/example-{0}.jpg".format(random.randint(0, 99999)),chatid)
	else:
		for num in list(range(count)):
			api.pyTelegramApi.sendPhotoId_ByUrl(api, "https://www.thiswaifudoesnotexist.net/example-{0}.jpg".format(random.randint(0, 99999)),chatid)
def main():
	SendRandomWaifu2d(5)
