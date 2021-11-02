#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bot.classes.pyTelegramApi as api
import bot.modules.fun.art2d as art2d
import bot.modules.news.ixbt as newixbt
import bot.modules.system.about as about

def getNewIxbt():#Возвращаем новое новость
	newixbt.getNew()
	ixbt()

def getRandomIxbt():#Возвращаем рандомное новость
	newixbt.getRandom()
	ixbt()

def SendChatId():#Отправка айди конфы
	system()

def SendRandomWaifu2d():#Отправка рандомного картинки waifu2d
	art2d.SendRandomWaifu2d()
	roomArt2d()

def SendRandomWaifu2d5X():#Отправка рандомного картинки waifu2d 5X
	art2d.SendRandomWaifu2d(5)
	roomArt2d()

def SendRandomWaifu2d10X():#Отправка рандомного картинки waifu2d 10X
	art2d.SendRandomWaifu2d(10)
	roomArt2d()

def roomArt2d():
	api.InlineKeyBoard.UpdateRedirect('img2d')
	#Навигация
	bhk=api.InlineKeyBoard.getRedirect(__name__)
	#Кнопки
	X1=api.InlineKeyBoard.UXBtn({'txt':'1','func':'SendRandomWaifu2d@'+__name__}) #Кнопка
	X2=api.InlineKeyBoard.UXBtn({'txt':'5','func':'SendRandomWaifu2d5X@'+__name__}) #Кнопка
	X3=api.InlineKeyBoard.UXBtn({'txt':'10','func':'SendRandomWaifu2d10X@'+__name__}) #Кнопка
	#Ячейки
	item1=api.InlineKeyBoard.UXItem(X1)
	item2=api.InlineKeyBoard.UXItem(X2)
	item3=api.InlineKeyBoard.UXItem(X3)
	api.InlineKeyBoard.keyboard(api,'Кол-во отправок картинок',bhk+','+item1+','+item2+','+item3)

def getModules():
	about.main()
	system()

def img2d():#Меню картинок
	api.InlineKeyBoard.UpdateRedirect('main')
	#Навигация
	bhk=api.InlineKeyBoard.getRedirect(__name__)
	#Кнопки
	ava=api.InlineKeyBoard.UXBtn({'txt':'Арт 2д рандомный','func':'roomArt2d@'+__name__}) #Кнопка
	#Ячейки
	item3=api.InlineKeyBoard.UXItem(ava)
	api.InlineKeyBoard.keyboard(api,'Меню картинок :)',bhk+','+item3)

def system(): #Меню системные
	api.InlineKeyBoard.UpdateRedirect('main')
	chat_id=api.pyTelegramApi.getChatId(api)
	#Навигация
	bhk=api.InlineKeyBoard.getRedirect(__name__)
	#Ячейки
	api.InlineKeyBoard.keyboard(api,"Дополнительная информация\nID => {0}".format(chat_id),bhk)

def ixbt(): #Меню новости
	api.InlineKeyBoard.UpdateRedirect('news')
	#Навигация
	bhk=api.InlineKeyBoard.getRedirect(__name__)
	#Кнопки
	NEW=api.InlineKeyBoard.UXBtn({'txt':'🆕 Возвращаем новое','func':'getNewIxbt@'+__name__}) #Новая новость
	Random=api.InlineKeyBoard.UXBtn({'txt':'🎲 Возвращаем рандомное','func':'getRandomIxbt@'+__name__}) #Рандомное
	#Ячейки
	item=api.InlineKeyBoard.UXItem(NEW)
	item1=api.InlineKeyBoard.UXItem(Random)
	api.InlineKeyBoard.keyboard(api,"Меню новости ixbt :)",bhk+','+item+','+item1)

def news(): #Меню новости
	api.InlineKeyBoard.UpdateRedirect('main')
	#Навигация
	bhk=api.InlineKeyBoard.getRedirect(__name__)
	#Кнопки
	ixbt=api.InlineKeyBoard.UXBtn({'txt':'ixbt','func':'ixbt@'+__name__}) #Кнопка
	#Ячейки
	item=api.InlineKeyBoard.UXItem(ixbt)
	api.InlineKeyBoard.keyboard(api,"Меню новости :)\nВыбор сайта",bhk+','+item)

def donate():
	api.InlineKeyBoard.UpdateRedirect('main')
	#навигация
	bhk=api.InlineKeyBoard.getRedirect(__name__)
	#кнопки
	donetealerts=api.InlineKeyBoard.UXBtn({'txt':'DoneteAlerts','url':'https://www.donationalerts.com/r/mercurs'})
	yandex=api.InlineKeyBoard.UXBtn({'txt':'Яндекс Деньги','func':'donateYandex@'+__name__})
	#ячейки
	item=api.InlineKeyBoard.UXItem(donetealerts)
	item1=api.InlineKeyBoard.UXItem(yandex)
	api.InlineKeyBoard.keyboard(api,'Меню выбора способа оплаты :)',bhk+','+item1+','+item)

def donateYandex(): #меню донат
	api.InlineKeyBoard.UpdateRedirect('donate')
	#навигация
	bhk=api.InlineKeyBoard.getRedirect(__name__)
	#кнопки
	donate1=api.InlineKeyBoard.UXBtn({'txt':'💸 Донат - 10 руб','url':'https://money.yandex.ru/quickpay/shop-widget?writer=seller&targets=Помочь автору&targets-hint=&default-sum=10&button-text=11&payment-type-choice=on&mobile-payment-type-choice=on&hint=&successURL=&quickpay=shop&account=410018314785030'}) 
	donate2=api.InlineKeyBoard.UXBtn({'txt':'💸 Донат - 50 руб','url':'https://money.yandex.ru/quickpay/shop-widget?writer=seller&targets=Помочь автору&targets-hint=&default-sum=50&button-text=11&payment-type-choice=on&mobile-payment-type-choice=on&hint=&successURL=&quickpay=shop&account=410018314785030'}) 
	donate3=api.InlineKeyBoard.UXBtn({'txt':'💸 Донат - 100 руб','url':'https://money.yandex.ru/quickpay/shop-widget?writer=seller&targets=Помочь автору&targets-hint=&default-sum=100&button-text=11&payment-type-choice=on&mobile-payment-type-choice=on&hint=&successURL=&quickpay=shop&account=410018314785030'}) 
	donate4=api.InlineKeyBoard.UXBtn({'txt':'💸 Донат - 500 руб','url':'https://money.yandex.ru/quickpay/shop-widget?writer=seller&targets=Помочь автору&targets-hint=&default-sum=500&button-text=11&payment-type-choice=on&mobile-payment-type-choice=on&hint=&successURL=&quickpay=shop&account=410018314785030'}) 
	donate5=api.InlineKeyBoard.UXBtn({'txt':'💸 Донат - 1000 руб','url':'https://money.yandex.ru/quickpay/shop-widget?writer=seller&targets=Помочь автору&targets-hint=&default-sum=1000&button-text=11&payment-type-choice=on&mobile-payment-type-choice=on&hint=&successURL=&quickpay=shop&account=410018314785030'})
	donate6=api.InlineKeyBoard.UXBtn({'txt':'💸 Донат - 5000 руб','url':'https://money.yandex.ru/quickpay/shop-widget?writer=seller&targets=Помочь автору&targets-hint=&default-sum=5000&button-text=11&payment-type-choice=on&mobile-payment-type-choice=on&hint=&successURL=&quickpay=shop&account=410018314785030'})
	#ячейки
	item=api.InlineKeyBoard.UXItem(donate1)
	item1=api.InlineKeyBoard.UXItem(donate2)
	item2=api.InlineKeyBoard.UXItem(donate3)
	item3=api.InlineKeyBoard.UXItem(donate4)
	item4=api.InlineKeyBoard.UXItem(donate5)
	item5=api.InlineKeyBoard.UXItem(donate6)
	api.InlineKeyBoard.keyboard(api,'Помощь автору :)',bhk+','+item+','+item1+','+item2+','+item3+','+item4+','+item5)

def main():
    api.InlineKeyBoard.UpdateRedirect('main')
	#Кнопки
    img=api.InlineKeyBoard.UXBtn({'txt':'🖼 Картинки','func':'img2d@'+__name__}) #Меню картинок
    news=api.InlineKeyBoard.UXBtn({'txt':'📰 Новости','func':'news@'+__name__}) #Меню новости
    about=api.InlineKeyBoard.UXBtn({'txt':'❇️ Доп описание','func':'system@'+__name__}) #Меню инфа
    K=api.InlineKeyBoard.UXBtn({'txt':'❌ Покончить','func':'kill@'+__name__}) #Покончить
    donate=api.InlineKeyBoard.UXBtn({'txt':'💰 Помочь автору','func':'donate@'+__name__})#Донат
    #Ячейки
    item=api.InlineKeyBoard.UXItem(K)
    item1=api.InlineKeyBoard.UXItem(about)
    item2=api.InlineKeyBoard.UXItem(news)
    item3=api.InlineKeyBoard.UXItem(img)
    item4=api.InlineKeyBoard.UXItem(donate)
    api.InlineKeyBoard.keyboard(api,'Главное меню бота :)',item+','+item1+','+item2+','+item3+','+item4)

def kill():
	pass
