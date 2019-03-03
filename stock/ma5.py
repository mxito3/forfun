# -*- coding: utf-8 -*-
from wxpy import *
import datetime
import tushare as ts
import time
from apscheduler.schedulers.background import BackgroundScheduler
# 登陆微信
bot = Bot(console_qr=2, cache_path="botoo.pkl")

# 获取股价并发送提醒
# stock_symbol = input('请输入股票代码 \n>  ')
stock_symbols = ["603728", "601166", "002600",
                 "000797", '300149', '603027', '002891', '000725']
# price_low = input('请输入最低预警价格 \n>  ')
needSleepTime=300 #五分钟提醒一次

hadRemind={}   #记录今天是不是提醒了
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
            messageMap=[]
            if abs(nowPrice - ma5) <= 0.1:
                if whetherRemindeTody(stock_symbol) == False  :
                    messageMap.append(stock_symbol)
                    messageMap.append(mes)
                    needRemindMes.append(messageMap)
        print(content)
        remind(needRemindMes)
        time.sleep(needSleepTime)

def remind(messages):
    my_friend = bot.friends().search(u'test')[0]        
    for item in messages:
        stock_symbol = item[0]
        mes =  item[1]
        try:
            my_friend.send(mes+"\n两者绝对值小于0.1") 
            setRemind(stock_symbol)   
        except Exception as e:
            print(e)
            print("发送失败")

def whetherRemindeTody(stock_symbol):
    if hadRemind.get(stock_symbol):
        return True
    else:
        return False

def setRemind(stock_symbol):
    hadRemind[stock_symbol] = True

def resetRemind(): #每天早上九点半清空是否已经通知
    hadRemind={}
    print("重置")

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(resetRemind, 'cron', hour=9,minute=30,second=0)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

    stock()
