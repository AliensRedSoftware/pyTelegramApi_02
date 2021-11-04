import os
import _thread
import time
import importlib

def connect(name, token):
    print("[THREAD] [CONNECT] [@{0}] => WAIT...".format(name))
    importlib.import_module('bots.'+ name + '.bot').main(name, token)

if __name__ == '__main__':
    for bot in os.scandir(os.getcwd() + os.sep + 'tokens'):
        token=open(os.getcwd() + os.sep + 'tokens' + os.sep + bot.name, 'r').read().strip()
        _thread.start_new_thread(connect, (bot.name, token))
    while 1:
        pass
    #main.main(open(os.getcwd()+os.sep+'token', 'r').read().strip())
