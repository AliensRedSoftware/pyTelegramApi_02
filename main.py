#!/usr/bin/env python3
import classes.pyTelegramApi
import os
import _thread
import faulthandler
import sys
import importlib

def init():
    pass

def connect(name, token):
    faulthandler.enable()
    sys.setrecursionlimit(10**9) #Кол-во запросов
    print("[THREAD] [CONNECT] [@{0}] => WAIT...".format(name))
    importlib.import_module('bots.'+ name + '.bot').main(name, token)

if __name__ == '__main__':
    init()
    for bot in os.scandir(os.getcwd() + os.sep + 'tokens'):
        token=open(os.getcwd() + os.sep + 'tokens' + os.sep + bot.name, 'r').read().strip()
        _thread.start_new_thread(connect, (bot.name, token))
    while 1:
        pass
    #main.main(open(os.getcwd()+os.sep+'token', 'r').read().strip())
