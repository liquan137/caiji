from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from admin.models import *
from current.models import *
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from dwebsocket.decorators import accept_websocket


# Create your views here.
def test(request):
    start_urls = []
    urls = list(m_project.objects.filter(size=0).values())
    index = 0
    fr = open('baiducookie.txt', 'r')
    cookielist = json.load(fr)
    fr.close()
    for item in urls:
        print(item)
        start_urls.append(item['url'])
        index += 1
        if index == 10:
            break

    for url in urls:
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('Referer=' + url['url'])

        # 取当前时间戳
        pathtime = str(round(time.time()))
        # 定义图片存放路径
        path = os.getcwd() + '\\img\\' + pathtime
        # 判断路径目录文件夹是否存在
        isExists = os.path.exists(path)
        if not isExists:
            # 不存在则创建文件夹
            os.makedirs(path)
        # 自定义路径位置
        # 指定谷歌浏览器路径
        prefs = {"download.default_directory": path}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(url)
        for cookie in cookielist:
            driver.add_cookie(cookie)
        driver.get(url)
        filename = 'content.html'
        with open(filename, 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))
        # 模拟点击，进行下载
        driver.find_element_by_xpath(
            '//div[@class="right_content fl"]/div[@class="like_down_box right_sub_box"]/a[1]').click()
        time.sleep(2)
        # 关闭
        driver.quit()
    return HttpResponse(json.dumps(start_urls))


def setCookie(request):
    start_urls = []
    urls = list(m_project.objects.filter(size=0).values())
    index = 0
    for item in urls:
        print(item)
        start_urls.append(item['url'])
        index += 1
        if index == 1:
            break
    fp = webdriver.FirefoxProfile()
    # 自定义路径下载
    fp.set_preference("browser.download.folderList", 2)
    options = webdriver.FirefoxOptions()
    # 设置静默模式
    options.add_argument('-headless')
    # 下载的格式
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
    driver = webdriver.Firefox(firefox_profile=fp, options=options)
    driver.get(start_urls[0])
    # 模拟点击，进行下载
    driver.find_element_by_xpath('//div[@class="login-reg fr"]/a[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@class="login_b_x"]/a[1]').click()
    # 延时 2秒等待下载完毕
    time.sleep(1)
    iframe = driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')
    driver.switch_to_frame(iframe)
    driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
    user = driver.find_element_by_xpath('//input[@id="u"]')
    user.send_keys('1031308775')
    password = driver.find_element_by_xpath('//input[@id="p"]')
    password.send_keys('liquan137')
    driver.find_element_by_xpath('//input[@id="login_button"]').click()
    time.sleep(1)
    diccookie = driver.get_cookies()
    fw = open('baiducookie.txt', 'w')
    json.dump(diccookie, fw)
    fw.close()
    return HttpResponse(json.dumps(diccookie))


@accept_websocket
def login(request):
    if request.is_websocket():
        for message in request.websocket:
            message = json.loads(message.decode('utf8'))
            # 将信息发至自己的聊天框
            request.websocket.send(json.dumps(
                {'code': 0, 'message': message,
                 'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
    else:
        template = loader.get_template('login.html')
        context = {

        }
        return HttpResponse(template.render(context, request))

@accept_websocket
def main(request):
    if request.is_websocket():
        for message in request.websocket:
            message = json.loads(message.decode('utf8'))
            if message['type'] == 'cookie':
                status = setCookie()
                if status:
                    # 将信息发至自己的聊天框
                    request.websocket.send(json.dumps(
                        {'code': 0, 'message': message,
                         'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
                else:
                    # 将信息发至自己的聊天框
                    request.websocket.send(json.dumps(
                        {'code': 1, 'message': message,
                         'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
    else:
        template = loader.get_template('login.html')
        context = {

        }
        return HttpResponse(template.render(context, request))

def setCookie():
    try:
        start_urls = []
        urls = list(m_project.objects.filter(size=0).values())
        index = 0
        for item in urls:
            print(item)
            start_urls.append(item['url'])
            index += 1
            if index == 1:
                break
        fp = webdriver.FirefoxProfile()
        # 自定义路径下载
        fp.set_preference("browser.download.folderList", 2)
        options = webdriver.FirefoxOptions()
        # 设置静默模式
        options.add_argument('-headless')
        # 下载的格式
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
        driver = webdriver.Firefox(firefox_profile=fp, options=options)
        driver.get(start_urls[0])
        # 模拟点击，进行下载
        driver.find_element_by_xpath('//div[@class="login-reg fr"]/a[1]').click()
        time.sleep(1)
        driver.find_element_by_xpath('//div[@class="login_b_x"]/a[1]').click()
        # 延时 2秒等待下载完毕
        time.sleep(1)
        iframe = driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')
        driver.switch_to_frame(iframe)
        driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
        user = driver.find_element_by_xpath('//input[@id="u"]')
        user.send_keys('1031308775')
        password = driver.find_element_by_xpath('//input[@id="p"]')
        password.send_keys('liquan137')
        driver.find_element_by_xpath('//input[@id="login_button"]').click()
        time.sleep(1)
        diccookie = driver.get_cookies()
        fw = open('baiducookie.txt', 'w')
        json.dump(diccookie, fw)
        fw.close()
        return  True
    except:
        return False
