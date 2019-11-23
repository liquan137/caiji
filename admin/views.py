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
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import filetype
from PIL import Image

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKID4wviFY9ckrkSuITusKXYP6f17xYsRnOj'  # 替换为用户的 secretId
secret_key = 'HI4arreAQQCi293mGUSAduymNincEbke'  # 替换为用户的 secretKey
region = 'ap-beijing'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


# Create your views here.
@accept_websocket
def index(request):
    if request.is_websocket():
        for message in request.websocket:
            message = json.loads(message.decode('utf8'))
            request.websocket.send(json.dumps(
                {'code': 0, 'message': '采集开始，默认跳过已经完成的结果', 'type': 'success',
                 'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
            status = test(request)
            if status == True:
                request.websocket.send(json.dumps(
                    {'code': 0, 'message': '采集完成', 'type': 'success',
                     'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
            else:
                request.websocket.send(json.dumps(
                    {'code': 1, 'message': message, 'type': 'error',
                     'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
    else:
        template = loader.get_template('index.html')
        context = {

        }
        return HttpResponse(template.render(context, request))


def returnUrl():
    start_urls = []
    index = 0
    urls = list(m_project.objects.filter(size=0).values())
    for item in urls:
        print(item)
        start_urls.append(item['url'])
        index += 1
        if index == 10:
            break
    return start_urls


def loadCookie():
    fr = open('baiducookie.txt', 'r')
    cookielist = json.load(fr)
    fr.close()
    return cookielist


def createFile(request):
    # 取当前时间戳
    pathtime = str(round(time.time()))
    # 定义图片存放路径
    path = os.getcwd() + '\\img\\' + pathtime
    # 判断路径目录文件夹是否存在
    isExists = os.path.exists(path)
    if not isExists:
        # 不存在则创建文件夹
        os.makedirs(path)
        request.websocket.send(json.dumps(
            {'code': 0, 'message': '创建文件夹：' + str(path), 'type': 'success',
             'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
    return path


def scaleCutImg(path, filename, request):
    try:
        file_path = path + '\\' + filename
        scale = 0.2
        type = filetype.guess(file_path)
        print(type.mime)
        img = Image.open(file_path)
        size = list(img.size)
        if img.size[0] > 5000:
            scale = 0.2
        elif img.size[0] > 3000 and img.size[0] < 5000:
            scale = 0.3
        elif img.size[0] > 2000 and img.size[0] < 3000:
            scale = 0.4
        elif img.size[0] > 1000 and img.size[0] < 2000:
            scale = 0.6
        path_arr = filename.split('.')
        print(path_arr)
        if img.size[0] > 1000:
            print('尺寸', scale, '/', (int(img.size[0] * scale), int(img.size[1] * scale)))
            img.thumbnail((int(img.size[0] * scale), int(img.size[1] * scale)))
            img.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
            callSocket(request, '图片缩放完成，文件名：' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'success')
            if img.size[0] == 1152:
                cropped = img.crop((176, 0, 800, 648))  # (left, upper, right, lower)
                os.remove(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                cropped.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                img = Image.open(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                img.thumbnail((int(img.size[0] * 0.7), int(img.size[1] * 0.7)))
                img.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                callSocket(request, '缩放剪裁完成，文件名：' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'success')
    except:
        callSocket(request, '文件格式错误缩放剪裁处理失败！文件名：' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'success')


def callSocket(request, msg, type):
    request.websocket.send(json.dumps(
        {'code': 0, 'message': msg, 'type': type,
         'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))


def test(request):
    start_urls = returnUrl()
    cookielist = loadCookie()
    path = createFile(request)
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('Referer=' + url)
    # 指定谷歌浏览器路径
    prefs = {"download.default_directory": path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for url in start_urls:
        driver.get(url)
        callSocket(request, '打开目标网站', 'success')
        for cookie in cookielist:
            driver.add_cookie(cookie)
        driver.get(url)
        filename = 'content.html'
        with open(filename, 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))
            callSocket(request, '保存采集HTML', 'success')
        # 模拟点击，进行下载
        time.sleep(1)
        driver.find_element_by_xpath(
            '//div[@class="right_content fl"]/div[@class="like_down_box right_sub_box"]/a[1]').click()
        callSocket(request, '开始下载', 'success')
        time.sleep(3)
        # 关闭
        # driver.quit()
        filename = driver.find_element_by_xpath('//form[@id="downloadForm"]/input[2]').get_attribute('value')
        callSocket(request, '下载文件的名称：' + filename, 'success')
        scaleCutImg(path, filename, request)

    return True


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
    fp.set_preference("browser.download.folderList", 2)
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
    driver = webdriver.Firefox(firefox_profile=fp, options=options)
    driver.get(start_urls[0])
    callSocket(request, '打开目标网站', 'success')
    driver.find_element_by_xpath('//div[@class="login-reg fr"]/a[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@class="login_b_x"]/a[1]').click()
    callSocket(request, '跳转QQ登陆网站', 'success')
    time.sleep(1)
    iframe = driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')
    driver.switch_to_frame(iframe)
    driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
    user = driver.find_element_by_xpath('//input[@id="u"]')
    user.send_keys('1031308775')
    password = driver.find_element_by_xpath('//input[@id="p"]')
    password.send_keys('liquan137')
    driver.find_element_by_xpath('//input[@id="login_button"]').click()
    callSocket(request, 'QQ登陆完成，返回目标网站', 'success')
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
            if message['type'] == 'login':
                if message['data']['user'] == 'admin' and message['data']['pwd'] == 'quanli137':
                    callSocket(request, '登陆成功', 'success')
                else:
                    callSocket(request, '登陆错误,请检测账号密码', 'error')
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
                callSocket(request, 'QQ互联登陆进程开始', 'success')
                status = setCookie(request)
                if status == True:
                    callSocket(request, '网站登陆COOKIE保存完成', 'success')
                else:
                    callSocket(request, message, 'error')
    else:
        template = loader.get_template('main.html')
        context = {

        }
        return HttpResponse(template.render(context, request))


def setCookie(request):
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
        request.websocket.send(json.dumps(
            {'code': 0, 'message': '已经打开目标网站', 'type': 'success',
             'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
        driver.find_element_by_xpath('//div[@class="login_b_x"]/a[1]').click()
        # 延时 2秒等待下载完毕
        time.sleep(1)
        request.websocket.send(json.dumps(
            {'code': 0, 'message': '跳转至QQ登陆', 'type': 'success',
             'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
        iframe = driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')
        driver.switch_to_frame(iframe)
        request.websocket.send(json.dumps(
            {'code': 0, 'message': '切换到账号密码登陆', 'type': 'success',
             'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
        driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
        user = driver.find_element_by_xpath('//input[@id="u"]')
        user.send_keys('1031308775')
        password = driver.find_element_by_xpath('//input[@id="p"]')
        password.send_keys('liquan137')
        driver.find_element_by_xpath('//input[@id="login_button"]').click()
        request.websocket.send(json.dumps(
            {'code': 0, 'message': '输入完毕，登陆成功', 'type': 'success',
             'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
        time.sleep(1)
        diccookie = driver.get_cookies()
        fw = open('baiducookie.txt', 'w')
        json.dump(diccookie, fw)
        fw.close()
        request.websocket.send(json.dumps(
            {'code': 0, 'message': '已保存cookie为txt文件', 'type': 'success',
             'time': time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))}))
        return True
    except:
        return False
