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
import http.client
import hashlib
import random
import json
from urllib import parse
DJANGO_PROJECT_PATH = '../../caiji'
DJANGO_SETTINGS_MODULE = 'caiji.settings'

sys.path.insert(0, DJANGO_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE
application = get_wsgi_application()
from admin.models import *

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
    urls = m_c_project.objects.filter(contact_id=16).values()
    for item in urls:
        start_urls.append({
            'url': item['url'],
            'id': item['id']
        })
    return start_urls


def scaleCutImg(path, filename, id, title, url):
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
    try:
        img.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
        scaleName = str(round(name)) + 'scale' + '.' + path_arr[1]
        viewName = str(round(name)) + 'view' + '.' + path_arr[1]
        with open(path + '/%sscale.%s' % (path_arr[0], path_arr[1]), 'rb') as fp:
            response = client.put_object(
                Bucket=tong,
                Body=fp,
                Key='/scale/' + viewName,
                StorageClass='STANDARD',
                EnableMD5=False
            )
    except:
        img.save(path + '/%sscale.%s' % (path_arr[0], 'png'))
        scaleName = str(round(name)) + 'scale' + '.png'
        viewName = str(round(name)) + 'view' + '.png'
        with open(path + '/%sscale.%s' % (path_arr[0], path_arr[1]), 'rb') as fp:
            response = client.put_object(
                Bucket=tong,
                Body=fp,
                Key='/scale/' + viewName,
                StorageClass='STANDARD',
                EnableMD5=False
            )
    print('图片缩放完成，文件名：' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'success')
    try:
        m_c_project.objects.get(title=title)
    except:
        print(title)
        child = m_project(contact_id=id, url=url, title=title, down_png=downName,
                          size=imgSize, color_type=mode, file_type=type.mime,
                          scale=scaleName, img_view=viewName,
                          update_time=round(time.time()), create_time=round(time.time()))
        child.save()


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
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('Referer=' + url)
    # 指定谷歌浏览器路径
    prefs = {"download.default_directory": path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options, executable_path=os.getcwd() + '\\' + 'chromedriver.exe')
    driver.delete_all_cookies()
    print('打开目标网站', 'success')
    for url in start_urls:
        time.sleep(1)
        driver.get(url['url'])
        filename = 'content.html'
        with open(filename, 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))
            print('保存采集HTML', 'success')
        # 模拟点击，进行下载
        time.sleep(1)
        href = driver.find_element_by_xpath('//span[@class="last"]/a').get_attribute('href')
        # driver.find_element_by_xpath('//span[@class="last"]/a').click()
        count = href.split('page=')[1]
        href = href.split('page=')[0] + 'page='
        try:
            for i in range(int(count)):
                if i != 0:
                    driver.get(href + str(i))
                    time.sleep(2)
                    driver.save_screenshot('page%s.png' % (i))
                    for each in driver.find_elements_by_xpath(
                            '//div[@class="js-masonry-grid"]/div[@class="grid__item grid__item--desktop-up-third"]'):
                        element = each.find_element_by_css_selector(
                            '.photo-tile__action.marketing-button.tile__overlay-trigger')
                        title = element.get_attribute(
                            'data-photo-title')
                        title = baidu(title)
                        try:
                            m_c_project.objects.get(title=title)
                        except:
                            driver.execute_script("arguments[0].click();", element)
                            filename = element.get_attribute(
                                'data-modal-image-url')
                            print(filename)
                            print(filename.split('/'))
                            print(filename.split('/')[4].split('?')[0])
                            name = filename.split('/')[4].split('?')[0]

                            runtime = 0
                            isExists = path + '/' + name
                            print('下载文件的名称：' + title, 'success')
                            print('下载文件的名称：' + name, 'success')
                            while True:
                                print('没有文件')
                                if not os.path.exists(isExists):
                                    print('没有文件', '下载用时：', runtime)
                                    time.sleep(1)
                                    runtime += 1
                                    if runtime == 60:
                                        print('下载超时！退出程序')
                                        exit()
                                else:
                                    print('下载完成', '下载用时：', runtime)
                                    scaleCutImg(path, name, url['id'], title, url['url'])
                                    break
                            print('下载文件的名称：' + name, 'success')
        except:
            print('采集出现错误，关闭驱动,005')
            driver.quit()
    # os.remove(path)
    driver.quit()
    print('采集完成，关闭驱动,006')

def baidu(q):
    appid = '20191202000362221'  # 填写你的appid
    secretKey = '4YLuhrQwQ689G3oK4z9r'  # 填写你的密钥

    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'  # 原文语种
    toLang = 'zh'  # 译文语种
    salt = random.randint(32768, 65536)
    print('salt', salt)
    sign = str(appid) + str(q) + str(salt) + str(secretKey)
    sign = hashlib.md5(sign.encode()).hexdigest()
    q = str(q)
    print('quote', parse.quote(q))
    myurl = myurl + '?appid=' + str(appid) + '&q=' + parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign
    title = False
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)
        print('result', result)
        print('result', result['trans_result'])
        print('result', result['trans_result'][0]['dst'])
        title = result['trans_result'][0]['dst']
        return result['trans_result'][0]['dst']

    except Exception as e:
        print(e)
        return False
    return title

def main():
    caiji()


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


if __name__ == '__main__':
    # print('quote',parse.quote('translate'))
    # create({
    #     'id': 0,
    #     'size': 0,
    #     'down_png': 0,
    #     'file_type': 0,
    #     'color_type': 0,
    #     'scale': 0,
    #     'key': 'admin'
    # })
    # exit()
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
