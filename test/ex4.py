from threading import Thread
from time import ctime,sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time
from tkinter import *
import tkinter.filedialog
import xlrd
from dateutil.parser import parse

class TaobaoInfos:
    #对象初始化
    def __init__(self,chromedriver_path):
        url = "https://login.taobao.com/member/login.jhtml"
        self.url=url
        options = webdriver.ChromeOptions()
        # 设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option("excludeSwitches",['enable-automation'])
        self.browser=webdriver.Chrome(executable_path=chromedriver_path,options=options)
        self.wait=WebDriverWait(self.browser,10)
        #超时时长为10s

    # 登录淘宝
    def login(self,weibo_username,weibo_password):
        # 打开网页
        self.browser.maximize_window()
        self.browser.get(self.url)
        # 自适应等待，点击密码登录选项
        self.browser.implicitly_wait(30)  # 智能等待，直到网页加载完毕，最长等待时间为30s
        # self.browser.find_element_by_xpath('//*[@class="forget-pwd J_Quick2Static"]').click()
        # 自适应等待，点击微博登录宣传
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="weibo-login"]').click()
        # 自适应等待，输入微博账号
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('username').send_keys(weibo_username)
        # 自适应等待，输入微博密码
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('password').send_keys(weibo_password)
        # 自适应等待，点击确认登录按钮
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()
        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
            '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print(taobao_name.text)

    def swipe_down(self):
        # for i in range(int(second / 0.1)):
        #     js = "var q=document.documentElement.scrollTop=" + str(300 + 200 * i)
        #     self.browser.execute_script(js)
        #     sleep(1)
        js = "var q=document.documentElement.scrollTop=" + str(100)
        self.browser.execute_script(js)
        sleep(1)
        js = "var q=document.documentElement.scrollTop=100000"
        self.browser.execute_script(js)
        sleep(1)

    def get_time_seconds(self,start_time, end_time):
        start = parse(start_time)
        end = parse(end_time)
        minus = (end-start).total_seconds()
        return int(minus)

    #打开抢购商品首页
    def get_shop(self,shop_url,buy_time):
        print("正在打开需要抢购的页面")
        self.browser.get(shop_url)
        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if buy_time > now:
                sleep(self.get_time_seconds(now,buy_time))
            try:
                print("ok")
                self.swipe_down()
                #等待购买按钮出现
                link_buy = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="tb-btn-buy"]/a')))
                link_buy.click()
                sut_j = self.wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="wrapper"]/a')))
                sut_j.click()
                print(f"抢购成功，请尽快付款")
                sleep(3)
                break
            except:
                self.browser.refresh()  # 刷新页面
                link_buy = self.wait.until(EC.presence_of_element_located((By.ID, 'J_LinkBuy')))
                link_buy.click()
                sut_j = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a')))
                sut_j.click()
                print(f"抢购成功，请尽快付款")
                sleep(3)
                break
    def gb(self):
        print(">>> 抢购完毕，关闭浏览器！")

def all(weibo_username,weibo_password,buy_time,but_text):
    # chromedriver_path = "E:\XXXTENTACION\Documents\Firefox下载\chromedriver.exe"
    # chormedriver_path = "D:\迅雷下载\chromedriver_win32\chromedriver.exe"
    chromedriver_path = r'.\tools\chromedriver.exe'
    a=TaobaoInfos(chromedriver_path)
    a.login(weibo_username,weibo_password)
    #"2020-05-14 10:43:40"
    url = but_text
    try:
        a.get_shop(url,buy_time)
    except:
        a.get_shop(url,buy_time)
    a.gb()

class ExcelUtil:
    def __init__(self, excel_path, sheet_name):
        self.data = xlrd.open_workbook(excel_path)
        self.table = self.data.sheet_by_name(sheet_name)
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols
    def dict_data(self):
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            r = []  # 存放读取数据
            j = 1
            for i in range(self.rowNum - 1):
                s = {}  # 存放每一行的键值对
                # 从第二行取对应的value值
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r

def xz():
    link_text.delete(0,END)
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        link_text.insert(0,filename)
    else:
        link_text.insert(0,'您没有选择任何文件,请重新选择')
    username_list = ExcelUtil(filename, "Sheet1").dict_data()
    count = 0
    for user_info in username_list:
        count = count+1
        user_name = str(round(user_info["username"]))
        label4 = Label(root, text="账号为： "+user_name)
        label4.place(x=20, y=180+30*(count-1), height=30, width=400)

def action():
    start_time = time.time()
    # 循环取出列表中的每一个值（字典），获取它的用户名和密码
    link = but_text.get()
    filename = link_text.get()
    buy_time = time_text.get()
    username_list = ExcelUtil(filename, "Sheet1").dict_data()
    count = 0
    threads = []
    for user_info in username_list:
        count = count+1
        user_name = str(round(user_info["username"]))
        user_password = str(user_info["password"])
        t = Thread(target=all, args=(user_name, user_password, buy_time,link))
        threads.append(t)
        t.start()
        print("%s is running thread_array[%d]" % (ctime(), count))
    for t in threads:
        t.join()
        print("%s thread_array ended" % (ctime()))
    end_time = time.time()
    print("Total time:{}".format(end_time - start_time))

root = Tk()
root.title("天猫抢购")
root.geometry('700x300')  # 这里的乘号不是*
label = Label(root, text="请输入抢购相关信息", font=('宋体', 20))
label.place(x=40, y=10, height=30, width=600)
btn = Button(root, text='选择账号信息文件的位置',justify='left',command=xz)
btn.place(x=20, y=50, height=30, width=130)
link_text = Entry(root,text = "",justify='left')
link_text.place(x=170, y=50, height=30, width=500)
label2 = Label(root,text = "请输入具体购买时间(格式如:2020-05-14 10:43:40): ")
label2.place(x=20, y=90, height=30, width=290)
time_text = Entry(root)
time_text.place(x=320, y=90, height=30, width=170)
label3 = Label(root,text = "请输入商品链接: ")
label3.place(x=20, y=140, height=30, width=100)
but_text = Entry(root)
but_text.place(x=130, y=140, height=30, width=430)
btn2 = Button(root, text='开始抢购',command=action)
btn2.place(x=260, y=230, height=30, width=220)
root.mainloop()