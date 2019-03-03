# -*- coding: utf-8 -*-
from wxpy import *
import datetime
import tushare as ts
import time
# 登陆微信
bot = Bot(console_qr=2, cache_path="botoo.pkl")

# 获取股价并发送提醒
# stock_symbol = input('请输入股票代码 \n>  ')
stock_symbols = ["603728", "601166", "002600",
                 "000797", '300149', '603027', '002891', '000725']
# price_low = input('请输入最低预警价格 \n>  ')
needSleepTime=300  #五分钟提醒一次

def stock():
    while True:
        needRemindMes = []
        content = []
        for stock_symbol in stock_symbols:
            data = ts.get_realtime_quotes(stock_symbol)    # 获取股票信息
            hisData = ts.get_hist_data(stock_symbol)
            nowPrice = float(data['price'])
            ma5 = hisData['ma5'][0]
            name = data['name'][0]
            mes = name + ' 的当前价格为 ' + str(nowPrice) + "五日均值为"+str(ma5)
            content.append(mes)
            # 设置预警价格并发送预警信息
            if abs(nowPrice - ma5) <= 0.1:
                needRemindMes.append(mes)
        print(content)
        remind(needRemindMes)
        time.sleep(needSleepTime)

def remind(messages):
    my_friend = bot.friends().search(u'lxy')[0]            
    for mes in messages:
        try:
            my_friend.send(mes+"  　　　两者绝对值小于0.1")    
        except Exception as e:
            print(e)
            print("发送失败")


if __name__ == '__main__':
    stock()
