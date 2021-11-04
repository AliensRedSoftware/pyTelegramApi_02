import classes.pyTelegramApi as api
import time

def main(name, cfg):
	time.sleep(50)
	api.pyTelegramApi.sendMessage('Привет :)', cfg)

def exit(name, cfg):
	pass
