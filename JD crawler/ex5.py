import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.action_chains import ActionChains

def main():
    # os.system(r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application/chrome.exe --remote-debugging-port=9999 --user-data-dir="C:\selenum\AutomationProfile"')
    chrome_debug_port = 9999
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{chrome_debug_port}")

    browser = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(browser, 5)
    print(browser.title)

    # 当前句柄
    current_handle = browser.current_window_handle

    # browser.execute_script('window.open("https://login.taobao.com/member/login.jhtml")')
    browser.execute_script('window.open("http://www.baidu.com")')

    # 所有句柄
    all_handle = browser.window_handles
    second_handle = all_handle[-1]

    # 切回first
    browser.switch_to.window(current_handle)

    url = 'https://s.taobao.com/search?q=电脑'
    browser.get(url)

    produce_info_xpath = '//div[contains(@class, "J_MouserOnverReq")]//div[@class="row row-2 title"]/a'
    produce_info = browser.find_elements_by_xpath(produce_info_xpath)
    for produce in produce_info:
        print(produce.text.replace(' ', ''))

    # 这里是演示，所以只爬了前 5 页
    for page_num in range(2, 6):
        next_page_xpath = '//li[@class="item next"]'
        next_page = browser.find_element_by_xpath(next_page_xpath)
        next_page_enable = False if 'disabled' in next_page.get_attribute('class') else True
        if next_page_enable:
            print('*' * 100)
            print(f'第 {page_num} 页')
            next_page.click()
            # browser.refresh()
            produce_info_xpath = '//div[contains(@class, "J_MouserOnverReq")]//div[@class="row row-2 title"]/a'

            wait.until(EC.presence_of_all_elements_located((By.XPATH, produce_info_xpath)))
            time.sleep(random.randint(3, 5))
            produce_info = browser.find_elements_by_xpath(produce_info_xpath)
            for produce in produce_info:
                print(produce.text.replace(' ', ''))
        else:
            break


if __name__ == '__main__':
    main()
