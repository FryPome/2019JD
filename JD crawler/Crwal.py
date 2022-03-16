#实现登录后爬取淘宝商品的信息

import requests
import re
import csv

def getHTML():
    name = input('请输入爬取商品的名字:')
    start_url = 'https://s.taobao.com/search?q={}&s='.format(name)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/70.0'
    }
    path = 'F:\mycookie.txt'
    with open(path, 'r')as f:
        mycookies = f.read()
    mycookies = mycookies.split(';')
    cookies = {}
    for cookie in mycookies:
        name, value = cookie.strip().split('=', 1)
        cookies[name] = value
    pages = input('请输入爬取的商品页数:')
    goods = ''
    for i in range(int(pages)):
        url = start_url + str(i * 44)
        r = requests.get(url, headers=header, cookies=cookies, timeout=60)
        r.encoding = r.apparent_encoding
        goods += r.text
    return goods


def findMS(html):
    print('=' * 20, '正在爬取商品信息', '=' * 20, '\n')
    marketnames = re.findall('"nick":"(.*?)"', html)
    titles = re.findall('"raw_title":"(.*?)"', html)
    prices = re.findall('"view_price":"(.*?)"', html)
    pays = re.findall('"view_sales":"(.*?)"', html)
    data = []
    try:
        for i in range(len(titles)):
            data.append([marketnames[i], titles[i], prices[i],pays[i]])
        if data == '':
            print('=' * 20, '暂无此商品信息', '=' * 20, '\n')
            return data
        print('=' * 20, '爬取成功', '=' * 20, '\n')
    except:
        print('异常，爬取中断')
    return data


def download(data):
    print('=' * 20, '正在保存商品信息', '=' * 20, '\n')
    path = 'F:\goods.csv'
    try:
        f = open(path, "w", newline="")
        writer = csv.writer(f)
        writer.writerow(['店铺名称', '商品', '价格(单位：元）', '付款人数'])
        writer.writerows(data)
        print('=' * 20, '保存成功', '=' * 20, '\n')
    except:
        print('保存失败')
    f.close()


def main():
    html = getHTML()
    data = findMS(html)
    download(data)


if __name__ == "__main__":
    main()