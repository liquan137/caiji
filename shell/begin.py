import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import filetype
from PIL import Image
from django.core.wsgi import get_wsgi_application
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
import base64
import requests
from urllib import parse
import urllib
DJANGO_PROJECT_PATH = '../../caiji'
DJANGO_SETTINGS_MODULE = 'caiji.settings'

sys.path.insert(0, DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
application = get_wsgi_application()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

secret_id = 'AKID4wviFY9ckrkSuITusKXYP6f17xYsRnOj'  # 替换为用户的 secretId
secret_key = 'HI4arreAQQCi293mGUSAduymNincEbke'  # 替换为用户的 secretKey
region = 'ap-beijing'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'http'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)

# display = Display(visible=0, size=(1440, 1080))
# display.start()

class rsaKey:
    def create_key(self):
        RANDOM_GENERATOR = Random.new().read
        rsa = RSA.generate(1024, RANDOM_GENERATOR)
        # 秘钥对的生成
        PRIVATE_PEM = rsa.exportKey()
        PUBLIC_PEM = rsa.publickey().exportKey()
        return {
            'public': PUBLIC_PEM.decode('utf-8'),
            'private': PRIVATE_PEM.decode('utf-8')
        }


def login():
    start_urls = []
    post = requests.post('http://49.233.200.55/api/list', {})
    print(post.text)
    urls = json.loads(post.text)
    index = 0
    for item in urls:
        print(item)
        start_urls.append(item['url'])
        index += 1
        if index == 1:
            break

    path = createFile()
    chrome_options = Options()
    chrome_options.add_argument('window-size=1920x3000')
    chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('Referer=' + url)
    # 指定谷歌浏览器路径
    prefs = {"download.default_directory": path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options, executable_path=os.getcwd() + '\\' + 'chromedriver.exe')
    driver.get(start_urls[0])
    driver.save_screenshot('full_snap.png')
    driver.find_element_by_xpath('//div[@class="login-reg fr"]/a[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@class="login_b_x"]/a[1]').click()
    print('跳转QQ登陆网站', 'success')
    driver.save_screenshot('full_snap1.png')
    iframe = driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')
    driver.switch_to_frame(iframe)
    driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
    user = driver.find_element_by_xpath('//input[@id="u"]')
    user.send_keys('1031308775')
    password = driver.find_element_by_xpath('//input[@id="p"]')
    password.send_keys('liquan137')
    driver.find_element_by_xpath('//input[@id="login_button"]').click()
    driver.save_screenshot('full_snap.png')
    print('QQ登陆完成，返回目标网站', 'success')
    driver.save_screenshot('full_snap2.png')
    time.sleep(1)
    diccookie = driver.get_cookies()
    fw = open('cookie.txt', 'w')
    json.dump(diccookie, fw)
    fw.close()
    driver.quit()
    return True


def loadPublic():
    f = open('public.txt', 'r')
    return f.read()


def checkCookie():
    timeSoft = os.getcwd() + '\\log.txt'
    logExists = os.path.exists(timeSoft)
    if not logExists:
        with open(timeSoft, 'wb') as f:
            f.write((json.dumps({'time': str(round(time.time()))})).encode('utf-8'))
            print('保存cookie时间', 'success')
        print('创建文件夹：' + str(timeSoft), 'success',
              time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
        return False
    else:
        timeLog = open(timeSoft, 'r')
        timeDate = json.load(timeLog)
        print(timeDate, '上次保存时间')
        timeLog.close()
        if int(timeDate['time']) + 600 > round(time.time()):
            return True
        else:
            return False


def createFile():
    pathtime = str(round(time.time()))
    # 定义图片存放路径
    path = os.getcwd() + '\\img'
    # 判断路径目录文件夹是否存在
    isExists = os.path.exists(path)
    if not isExists:
        # 不存在则创建文件夹
        os.makedirs(path)
        print('创建文件夹：' + str(path), 'success',
              time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time())))
    return path


def loadCookie():
    fr = open('cookie.txt', 'r')
    cookielist = json.load(fr)
    fr.close()
    return cookielist


def returnUrl():
    start_urls = []
    index = 0
    post = requests.post('http://49.233.200.55/api/list', {})
    print(post.text)
    urls = json.loads(post.text)
    for item in urls:
        start_urls.append({
            'url': item['url'],
            'id': item['id']
        })
    return start_urls


def scaleCutImg(path, filename, id):
    path_arr = filename.split('.')
    response = client.list_buckets()
    tong = response['Buckets']['Bucket'][0]['Name']
    name = float(time.time()) * 10000
    downName = str(round(name)) + '.' + path_arr[1]
    print(downName)
    with open(path + '/' + filename, 'rb') as fp:
        response = client.put_object(
            Bucket=tong,
            Body=fp,
            Key='/vip/' + downName,
            StorageClass='STANDARD',
            EnableMD5=False
        )
    print(response['ETag'])
    scaleName = ''
    file_path = path + '/' + filename
    scale = 0.2
    type = filetype.guess(file_path)
    print(type.mime)

    img = Image.open(file_path)
    mode = img.mode
    size = list(img.size)
    imgSize = str(img.size[0]) + 'x' + str(img.size[1])
    if img.size[0] > 5000:
        scale = 0.2
    elif img.size[0] > 3000 and img.size[0] < 5000:
        scale = 0.3
    elif img.size[0] > 2000 and img.size[0] < 3000:
        scale = 0.4
    elif img.size[0] > 1000 and img.size[0] < 2000:
        scale = 0.6
    else:
        img.thumbnail((int(img.size[0] * 0.8), int(img.size[1] * scale)))
        img.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
        with open(path + '\\%sscale.%s' % (path_arr[0], path_arr[1]), 'rb') as fp:
            response = client.put_object(
                Bucket=tong,
                Body=fp,
                Key='/scale/' + str(round(name)) + '.' + path_arr[1],
                StorageClass='STANDARD',
                EnableMD5=False
            )
        scaleName = str(round(name)) + '.' + path_arr[1]
    path_arr = filename.split('.')
    print(path_arr)
    if img.size[0] > 1000:
        print('尺寸', scale, '/', (int(img.size[0] * scale), int(img.size[1] * scale)))
        img.thumbnail((int(img.size[0] * scale), int(img.size[1] * scale)))
        img.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
        print('图片缩放完成，文件名：' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'success')
        if img.size[0] == 1152:
            cropped = img.crop((176, 0, 800, 648))  # (left, upper, right, lower)
            os.remove(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
            cropped.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
            img = Image.open(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
            img.thumbnail((int(img.size[0] * 0.7), int(img.size[1] * 0.7)))
            img.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
            print('缩放剪裁完成，文件名：' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'success')
        scaleName = str(round(name)) + 'scale' + '.' + path_arr[1]
        with open(path + '\\' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'rb') as fp:
            response = client.put_object(
                Bucket=tong,
                Body=fp,
                Key='/scale/' + scaleName,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        os.remove(path + '\\' + filename)
        os.remove(path + '\\' + '%sscale.%s' % (path_arr[0], path_arr[1]))
        print(response['ETag'])
    states = create({
        'id': id,
        'size': imgSize,
        'down_png': downName,
        'file_type': type.mime,
        'color_type': mode,
        'scale': scaleName,
        'key': 'admin'
    })
    if states == True:
        print('修改成功')
    else:
        print('修改失败')


def create(data):
    rsakey = RSA.importKey(loadPublic())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    # 密码加密
    cipher_text = base64.b64encode(cipher.encrypt((bytes(data['key'].encode("utf8")))))
    cipher_text = cipher_text.decode('utf-8')
    print(cipher_text)
    data['key'] = cipher_text
    post = requests.post('http://49.233.200.55/api/create', data)
    print(post.text)
    res = json.loads(post.text)
    if int(res['code']) == 200:
        return True
    else:
        return False


def caiji():
    request = None
    start_urls = returnUrl()
    cookielist = loadCookie()
    start_urls = returnUrl()
    path = createFile()
    chrome_options = Options()
    chrome_options.add_argument('window-size=1920x3000')
    chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36"')
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('Referer=' + url)
    # 指定谷歌浏览器路径
    prefs = {"download.default_directory": path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options, executable_path=os.getcwd() + '\\' + 'chromedriver.exe')
    driver.delete_all_cookies()
    print('打开目标网站', 'success')
    try:
        driver.get(start_urls[0]['url'])
        for cookie in cookielist:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver.add_cookie(cookie)
        for url in start_urls:
            time.sleep(1)
            try:
                driver.get(url['url'])
                filename = 'content.html'
                with open(filename, 'wb') as f:
                    f.write(driver.page_source.encode('utf-8'))
                    print('保存采集HTML', 'success')
                # 模拟点击，进行下载
                driver.save_screenshot('codefull.png')
                time.sleep(1)
                print('开始下载', 'success')
                driver.find_element_by_xpath(
                    '//div[@class="right_content fl"]/div[@class="like_down_box right_sub_box"]/a[1]').click()
                time.sleep(2)
                driver.save_screenshot('codefull.png')
                try:
                    filename = driver.find_element_by_xpath('//form[@id="downloadForm"]/input[2]').get_attribute(
                        'value')
                    isExists = path + '/' + filename
                    runtime = 0
                except:
                    # print("检测到验证码！请输入验证码！")
                    # # js = """$("#captcha-img").click()"""
                    # # driver.execute_script(js)
                    # time.sleep(1)
                    # imgUrl = driver.find_element_by_xpath('//img[@id="captcha-img"]').get_attribute('src')
                    # img = driver.find_element_by_xpath('//img[@id="captcha-img"]')
                    # left = img.location['x']
                    # top = img.location['y']
                    # right = img.location['x'] + img.size['width']
                    # bottom = img.location['y'] + img.size['height']
                    # photo = Image.open('codefull.png')
                    # photo = photo.crop((left, top, right, bottom))
                    # photo.save('code.png')
                    # print('请输入你看见的验证码')
                    # code = input()
                    # post = """$.post("/?c=Public&a=check_verify", {
                    #             code : """+code+"""
                    #         }, function(data) {
                    #             if (data == true) {
                    #                 location.reload();
                    #             } else {
                    #                 $('#check_verify_txt').show();
                    #             }
                    #         });"""
                    # driver.execute_script(post)
                    while True:
                        try:
                            driver.find_element_by_xpath(
                                '//div[@class="right_content fl"]/div[@class="like_down_box right_sub_box"]/a[1]').click()
                            time.sleep(2)
                            filename = driver.find_element_by_xpath('//form[@id="downloadForm"]/input[2]').get_attribute(
                                'value')
                            isExists = path + '/' + filename
                            runtime = 0
                            break
                        except:
                            print("检测到验证码！请输入验证码！")
                            js = """$("#captcha-img").click()"""
                            driver.execute_script(js)
                            time.sleep(1)
                            driver.save_screenshot('codefull.png')
                            img = driver.find_element_by_xpath('//img[@id="captcha-img"]')
                            left = img.location['x']
                            top = img.location['y']
                            right = img.location['x'] + img.size['width']
                            bottom = img.location['y'] + img.size['height']
                            photo = Image.open('codefull.png')
                            photo = photo.crop((left, top, right, bottom))
                            photo.save('code.png')
                            print('请输入你看见的验证码')
                            code = input()
                            post = """$.post("/?c=Public&a=check_verify", {
                                                            code : """ + code + """
                                                        }, function(data) {
                                                            if (data == true) {
                                                                location.reload();
                                                            } else {
                                                                $('#check_verify_txt').show();
                                                            }
                                                        });"""
                            driver.execute_script(post)
                    # down = """$(".like_down_box a").eq(0).click()"""
                    # driver.execute_script(down)
                    # filename = driver.find_element_by_xpath('//form[@id="downloadForm"]/input[2]').get_attribute(
                    #     'value')
                    # isExists = path + '/' + filename
                    # runtime = 0
                while True:
                    print('没有文件')
                    if not os.path.exists(isExists):
                        print('没有文件', '下载用时：', runtime)
                        time.sleep(1)
                        runtime += 1
                        if runtime == 15:
                            print('下载超时！退出程序')
                            exit()
                    else:
                        print('下载完成', '下载用时：', runtime)
                        break
                print('下载文件的名称：' + filename, 'success')
                scaleCutImg(path, filename, url['id'])
            except:
                print('执行过程中出现错误，请在路径中查看相关网页截图确认错误！,004')
    except:
        print('出现错误，关闭驱动，005')
        driver.quit()
    # os.remove(path)
    driver.quit()
    print('采集完成，关闭驱动,006')


def main():
    print('采集脚本开始,请输入采集时间间隔单位')
    print('1:秒    |    2:分    |    3:时')
    y = input()
    size = '秒'
    sizeOf = 1
    print(y)
    if int(y) == 1:
        size = '秒'
        sizeOf = 1
    elif int(y) == 2:
        size = '分'
        sizeOf = 60
    elif int(y) == 3:
        size = '时'
        sizeOf = 3600

    print('采集脚本开始,请输入采集时间间隔（单位：', size, '）')
    x = input()
    print('您输入的时间为：', x, size)
    print('开始采集任务！')
    index = 1
    wait = 1
    while True:
        print('采集执行次数：', index, '   |   ', x, size, '之后将会执行下一个任务')
        if checkCookie():
            caiji()
        else:
            if login():
                caiji()
        # try:
        #     if checkCookie():
        #         caiji()
        #     else:
        #         if login():
        #             caiji()
        #     print('执行成功！')
        # except:
        #     print('执行错误！008')
        while True:
            print('等待中...', '当前时间：', wait)
            if wait == int(x) * int(sizeOf):
                break
            time.sleep(1)
            wait += 1
        time.sleep(int(x) * int(sizeOf))
        index += 1

    #


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    print('quote',parse.quote('translate'))
    # create({
    #     'id': 0,
    #     'size': 0,
    #     'down_png': 0,
    #     'file_type': 0,
    #     'color_type': 0,
    #     'scale': 0,
    #     'key': 'admin'
    # })
    exit()
    # RSAKEY = rsaKey()
    # key = RSAKEY.create_key()
    # PUBLIC_PEM = key['public']
    # PRIVATE_PEM = key['private']
    # with open('public.txt', 'wb') as f:
    #     f.write(PUBLIC_PEM.encode('utf-8'))
    #     f.close()
    # with open('private.txt', 'wb') as s:
    #     s.write(PRIVATE_PEM.encode('utf-8'))
    #     s.close()
    # print(PUBLIC_PEM)
    # print(PRIVATE_PEM)
    # exit()
    main()
