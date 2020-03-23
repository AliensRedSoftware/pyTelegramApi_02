import bot.classes.pyTelegramApi as api
import requests
from bs4 import BeautifulSoup

def getNew(): #Возвращаем новое
    ARR=[]
    HTML=requests.get('https://www.ixbt.com/news/?show=tape').text
    R=BeautifulSoup(HTML, 'lxml')
    for B in R.find('div', class_="item__text"):
        if B.name == 'p':
            ARR.append(B.text)
        elif B.name == 'div':
            if ARR:
                api.pyTelegramApi.sendMessage_array(api, ARR)
                ARR=[]
            IMG=B.find('img')
            IMG='https://www.ixbt.com'+IMG['data-original-src']
            api.pyTelegramApi.sendPhoto_ByUrl(api,IMG)
    if ARR:
        api.pyTelegramApi.sendMessage_array(api, ARR)
    api.pyTelegramApi.sendSticker(api, 'CAACAgQAAx0CWAABe5cAAg3wXndV-fNtQb-htywOUuKERgVLwBAAAq0AAyg5Vw-IeDJbNkZythgE');

def getRandom(): #Возвращаем рандомное
	print('test')

def main():
    getRandom()
