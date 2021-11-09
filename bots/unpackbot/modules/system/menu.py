#!/usr/bin/env python
# -*- coding: utf-8 -*-
import classes.pyTelegramApi as api

def main(cfg):
    time.sleep(500)
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
    api.InlineKeyBoard.keyboard('Главное меню бота :)',item+','+item1+','+item2+','+item3+','+item4)

def kill():
	pass

def exit(cfg):
	pass
