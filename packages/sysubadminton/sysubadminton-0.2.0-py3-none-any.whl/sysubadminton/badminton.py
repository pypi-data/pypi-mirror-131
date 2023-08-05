#!/usr/bin/env python

import json
import configparser
import sys
import argparse
from json.decoder import JSONDecodeError
from itertools import groupby
from time import sleep
from datetime import datetime, timedelta, date, time
import requests
from bs4 import BeautifulSoup


class Badminton():
    def __init__(self, configpath, max_times=10, begin_time='00:01'):
        self.session = requests.Session()
        self.headers = {
            "Origin": "https://gym.sysu.edu.cn",
            "Referer": "https://gym.sysu.edu.cn/order/show.html?id=161",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
        }
        self.stocks, self.selects, self.results = [], [], []
        self.capt, self.imbyte = None, None
        self.max_times = max_times
        self.begin_time = begin_time

        conf_par = configparser.ConfigParser()
        try:
            conf_par.read(configpath, encoding='utf-8')
            conf = dict(conf_par['badminton'])
        except KeyError:
            print('检查配置文件是否存在且正确填写')
            sys.exit()

        self.first, self.stock_number = conf['first'], conf['stock_number']
        self.netid, self.password = conf['netid'], conf['password']
        if (self.netid == '') or (self.password == ''):
            print('填写 netid 和密码')
            sys.exit()
        try:
            self.stock_name = [int(i) for i in conf['stock_name'].split(',')]
            self.stock_time = [int(i) for i in conf['stock_time'].split(',')]
            self.stock_number = int(conf['stock_number'])
            if conf['stock_date'] == '':
                self.stock_date = date.today() + timedelta(days=2)
            else:
                self.stock_date = datetime.strptime(
                    conf['stock_date'], "%Y-%m-%d").date()
        except ValueError:
            print('检查配置文件填写是否正确')
            sys.exit()

        print(f'预定日期：{self.stock_date}')
        print(f"预定场次：{conf['stock_name']}\n预定时间：{conf['stock_time']}")


    def get_stocks(self):
        '''获取指定日期可预定的场次列表
        '''
        gym_url = 'https://gym.sysu.edu.cn/product/findOkArea.html'
        try_times = 0
        while try_times < self.max_times:
            try_times += 1
            r = requests.post(
                f'{gym_url}?s_date={self.stock_date}&serviceid=161')
            try:
                json_data = json.loads(r.text)
            except JSONDecodeError:
                if r.status_code == 502:
                    print('目测服务器崩溃了，等待一分钟后重试')
                    sleep(60)
                    continue
                print(f'获取场地信息失败，第 {try_times} 次重试')
                print(r.status_code)
                sleep(3)
                continue
            stocks = json_data['object']

            for stock in stocks:
                dic = {}
                if stock['status'] == 1:
                    for keys in ['id', 'stockid']:
                        dic[keys] = stock[keys]
                    for keys in ['price', 's_date']:
                        dic[keys] = stock['stock'][keys]
                    dic['sname'] = int(stock['sname'][2:])
                    dic['time_full'] = stock['stock']['time_no']
                    dic['time_no'] = int(dic['time_full'][:2])
                    self.stocks.append(dic)
            if len(self.stocks) == 0:
                print("凉了，没场地了，告辞")
                sys.exit()
            print(f'{self.stock_date} 共计 {len(self.stocks)} 个场地可以预订，开始按条件筛选')
            break


    def select(self):
        ''' 根据条件筛选场次
        '''
        select = []
        for stock in self.stocks:
            if stock['sname'] in self.stock_name and stock['time_no'] in self.stock_time:
                select.append(stock)
        if len(select) == 0:
            print('没有满足条件的场地了')
            sys.exit()
        select.sort(key=lambda elem: (self.stock_time.index(elem['time_no']),
                                      self.stock_name.index(elem['sname'])))
        reselect = []
        for _, items in groupby(select,
                                key=lambda elem: self.stock_time.index(elem['time_no'])):
            i = 0
            for stock in items:
                reselect.append(stock)
                i += 1
                if i >= self.stock_number:
                    break
        self.selects = reselect
        if self.first == 'name':
            self.selects.sort(key=lambda elem: (self.stock_name.index(elem['sname']),
                                                self.stock_time.index(elem['time_no'])))
        print(f"共筛选出 {len(self.selects)} 个场地")
        for stock in self.selects:
            print(f"{stock['id']}  场地{stock['sname']}  {stock['time_full']}")


    def recognize(self):
        ''' 调用某位不知名好心人的在线识别验证码后端
        '''
        files = {'img': ('captcha.jpg', self.imbyte, 'image/jpeg')}
        recg_times = 0
        while recg_times < 6:
            r = requests.post('http://tony-space.top:8989/captcha', files=files)
            if len(r.text) == 4:
                self.capt = r.text
                print(f'验证码识别成功：{self.capt}')
                return True
            recg_times += 1
            print(f'识别失败：{r.text}，第 {recg_times} 次重试')
            sleep(1)
            continue

        with open('capt.jpg', 'wb') as f:
            f.write(self.imbyte)
        self.capt = input('验证码识别失败，请手动打开 capt.jpg 识别后输入')


    def login(self):
        headers = {"User-Agent": self.headers['User-Agent']}
        login_url = "https://cas.sysu.edu.cn/cas/login"
        captcha_url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
        self_url = "https://gym.sysu.edu.cn/yyuser/personal.html"
        login_form = {"username": "",
                      "password": "",
                      "captcha": "",
                      "_eventId": "submit",
                      "geolocation": "",
                      }
        login_times = 0

        while login_times < 6:
            login_times += 1
            r = self.session.get(self_url, headers=headers)
            if '欢迎' in r.text:
                print('登录成功')
                return True

            self.imbyte = self.session.get(captcha_url).content
            self.recognize()
            login_form['captcha'] = self.capt

            r = self.session.get(login_url)
            soup = BeautifulSoup(r.text, features="html.parser")
            login_form['execution'] = soup.select(
                "input[name='execution']")[0]['value']
            login_form["username"] = self.netid
            login_form["password"] = self.password

            r = self.session.post(login_url, headers=headers, data=login_form)
            if 'success' in r.text:
                print('登录成功')
                r = self.session.get(self_url, headers=headers)
                return True
            if 'credential' in r.text:
                print('用户名或密码错误')
                sys.exit()

            print(f'验证码错误，第 {login_times} 次重试')
            sleep(1)

        print('登录重试次数太多，终止')
        sys.exit()

    def waite(self):
        ''' 系统正常开启时间为 00:00-22:00，选择合适等待策略
        '''
        # 判断预订系统是否开放
        today = date.today()
        begin_hour = time(7, 0)
        begin_time = datetime.combine(today, begin_hour)
        end_time = datetime.combine(today, time(22, 0))
        now_time = datetime.now()
        if now_time < begin_time:
            # 早了
            stock = 0
        elif now_time > end_time:
            # 晚了
            stock = -1
        else:
            # 刚好
            stock = 1

        # 判断选定的日期是否可以预订
        if self.stock_date < today:
            print(f'预订日期已经过去，你可以穿越回 {self.stock_date}，再见')
            sys.exit()
        if self.stock_date == today:
            if stock == 1:
                print(f'当前时间 {datetime.now()}，开始预订')
                return True
            if stock == -1:
                print('预订日期已经过去，你可以穿越回 22:00 前，再见')
                sys.exit()
            if stock == 0:
                begin_time = datetime.combine(self.stock_date, begin_hour)

        elif self.stock_date == (today + timedelta(days=1)):
            if stock == 1:
                print(f'当前时间 {datetime.now()}，开始预订')
                return True
            if stock == -1:
                begin_time = datetime.combine(self.stock_date, begin_hour)
                print('预订系统已关闭')
            elif stock == 0:
                begin_time = datetime.combine(
                    self.stock_date - timedelta(days=1), begin_hour)

        elif self.stock_date > (today + timedelta(days=1)):
            # 等到前一天 00:00 才能预订
            begin_time = datetime.combine(
                self.stock_date - timedelta(days=1), begin_hour)
            print('超过目前可预订日期')
        else:
            print('超出判断条件，你也是个人才')
            sys.exit()

        print(f'等到 {begin_time} 预订，开始 sleep')
        if (begin_time - datetime.now()).days > 0:
            print('等待时间超过一天，个人建议等到明天再来预定')
            sleep((begin_time - datetime.now()).days * 86400)

        while ((begin_time - datetime.now()).seconds - 1) > 200:
            print(f'{begin_time - datetime.now()} 后开始预订')
            sleep((begin_time - datetime.now()).seconds - 180)

        print(f'{begin_time - datetime.now()} 后开始预订')
        if self.login():
            sleep((begin_time - datetime.now()).seconds + 3)
            return True
        print(f'{datetime.now()} 登录无效，尝试重新登录')
        return False


    def book(self):
        stock_index = 0
        book_times = 0
        while len(self.results) < 2 and book_times < 10:
            book_times += 1
            try:
                stock = self.selects[stock_index]
            except IndexError:
                print('可以预定的都试过了')
                break
            param = ('{"activityPrice":0,"activityStr":null,"address":null,"dates":null,'
                     '"extend":null,"flag":"0","isbookall":"0","isfreeman":"0","istimes":"1",'
                     '"merccode":null,"order":null,"orderfrom":null,"remark":null,"serviceid":'
                     'null,"shoppingcart":"0","sno":null,"stock":{"%s":"1"},"stockdetail":'
                     '{"%s":"%s"},"stockdetailids":"%s","subscriber":"0",'
                     '"time_detailnames":null,"userBean":null}') \
                % (stock['stockid'], stock['stockid'], stock['id'], stock['id'])
            data = {"param": param, "json": "true"}
            r = self.session.post("https://gym.sysu.edu.cn/order/book.html",
                                  headers=self.headers, data=data)
            try:
                return_data = json.loads(r.text)
            except JSONDecodeError:
                print(f'预定失败，第 {book_times} 次重试')
                sleep(10)
                continue

            if return_data['result'] == '2':
                print(
                    f'场地{stock["sname"]} {stock["s_date"]} {stock["time_full"]} 预订成功，待支付')
                stock_index += 1
                self.results.append([return_data['object']['orderid'],
                                    stock["sname"], stock["s_date"], stock["time_no"]])

            elif return_data['message'] == 'USERNOTLOGINYET':
                print('JSESSIONID 过期了')
                self.login()
                continue

            elif '已被预定' in return_data['message']:
                stock_index += 1
                print('座位已被预定，尝试下一个')
                continue

            else:
                print(f'预定失败，第 {book_times} 次重试')
                sleep(10)
                continue

        if len(self.results) == 0:
            print('预定失败，重试次数过多，退出')
            sys.exit()
        print(f'预订成功 {len(self.results)} 个场地，1 分钟后自动支付订单')


    def pay(self):
        pay_times = 0
        while pay_times < 10 and len(self.results) != 0:
            pay_times += 1
            result = self.results[0]
            print('支付订单  ' + str(result[0]))
            data1 = {"orderid": result[0], "payid": 2}
            headers = self.headers
            headers['Referer'] = f'https://gym.sysu.edu.cn/pay/show.html?id={result[0]}'
            data2 = {'param': json.dumps(
                {"payid": 2, "orderid": str(result[0]), "ctypeindex": 0})}

            r = self.session.get("https://gym.sysu.edu.cn/pay/account/showpay.html",
                                 headers=headers, data=data1)
            r = self.session.post("https://gym.sysu.edu.cn/pay/account/topay.html",
                                  headers=headers, data=data2)
            try:
                return_data = json.loads(r.text)
            except JSONDecodeError:
                print(f'支付失败，第 {pay_times} 次重试')
                sleep(5)
                self.login()
                continue
            if return_data["result"] == "1":
                print(f'{str(result[0])} 支付成功')
                self.results.remove(result)
            else:
                print(f'支付结果：{return_data["message"]}，重试')
                sleep(5)

        if len(self.results) != 0:
            print('可能有未成功支付的订单，请手动支付')


    def run(self):
        try_times = 0
        while try_times < 10:
            self.login()
            if not self.waite():
                # 重新登录
                sleep(3)
                try_times += 1
                continue

            self.get_stocks()
            self.select()
            self.book()
            sleep(60)
            self.pay()
            sys.exit()

def main():
    parser = argparse.ArgumentParser(description='预定中山大学珠海校区羽毛球场地')
    parser.add_argument('-c', '--config', type=str, help='配置文件路径', required=True)
    par = parser.parse_args()
    badminton = Badminton(par.config)
    badminton.run()

if __name__ == '__main__':
    main()
