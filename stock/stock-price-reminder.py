# -*- coding: utf-8 -*-
from wxpy import *
import datetime
import tushare as ts

# 登陆微信
bot = Bot(console_qr=2, cache_path="botoo.pkl")

# 获取股价并发送提醒
stock_symbol = input('请输入股票代码 \n>  ')
price_low = input('请输入最低预警价格 \n>  ')


def stock():
    time = datetime.datetime.now()    # 获取当前时间
    now = time.strftime('%H:%M:%S')
    data = ts.get_realtime_quotes(stock_symbol)    # 获取股票信息
    print(data)
    r1 = float(data['price'])
    r2 = str(stock_symbol) + ' 的当前价格为 ' + str(r1) + ''
    content = now + '\n' + r2
    # 设置预警价格并发送预警信息
    print(content)
    if r1 <= float(price_low):
        try:
            my_friend = bot.friends().search(u'lxy')[0]
            my_friend.send(content+"  　　低于最低预警")
        except Exception as e:
            print(e)
            print("发送失败")


if __name__ == '__main__':
    stock()
