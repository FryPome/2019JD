from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

#定义一个taobao类
class TaobaoInfos:
    #对象初始化
    def __init__(self):
        url = "https://login.taobao.com/member/login.jhtml"
        self.url=url
        options = webdriver.ChromeOptions()
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option("excludeSwitches",['enable-automation'])
        self.browser=webdriver.Chrome(executable_path=chromedriver_path,options=options)
        self.wait=WebDriverWait(self.browser,10) #超时时长为10s

    # 登录淘宝
    def login(self):

        # 打开网页
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
    # 扫码登陆淘宝
    # def login(self):
    #     # 打开网页
    #     self.browser.get(self.url)
    #     time.sleep(1)
    #     time.sleep(15)
    #打开抢购商品首页
    def get_shop(self,shop_url,buy_time):
        print("正在打开需要抢购的页面")
        self.browser.get(shop_url)
        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if now < buy_time:
                print("ok\n")
                try:
                    #等待购买按钮出现
                    link_buy=self.wait.until(EC.presence_of_element_located((By.ID,'J_LinkBuy')))
                    print("1\n")
                    link_buy.click()
                    print("2\n")
                    sut_j=self.wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="wrapper"]/a')))
                    print("3\n")
                    sut_j.click()
                    print(f"抢购成功，请尽快付款")
                    break
                except:
                    self.browser.refresh()  # 刷新页面
                    link_buy = self.wait.until(EC.presence_of_element_located((By.ID, 'J_LinkBuy')))
                    link_buy.click()
                    sut_j = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="wrapper"]/a')))
                    sut_j.click()
                    print(f"抢购成功，请尽快付款")
                    break
    def gb(self):
        print(">>> 抢购完毕，关闭浏览器！")


if __name__ == '__main__':
    weibo_username = "15634102290"  # 改成你的微博账号
    weibo_password = "zzx20010206"  # 改成你的微博密码
    chromedriver_path = "E:\XXXTENTACION\Documents\Firefox下载\chromedriver.exe"
    a=TaobaoInfos()
    a.login()
    buy='2020-04-26 21:04:10'
    url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.21.1d2321baZB0Wph&id=524397896694&skuId=3713557516210&areaId=370100&user_id=890482188&cat_id=2&is_b=1&rn=a3e99469d26bcbe0c8528e358f49cc02'
    try:
        a.get_shop(url,buy)
    except:
        a.get_shop(url,buy)
    a.gb()