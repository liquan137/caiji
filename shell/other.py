import os
import sys
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import filetype
from PIL import Image
from django.core.wsgi import get_wsgi_application
from pyvirtualdisplay import Display

# import pytesseract

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


def login():
    start_urls = []
    urls = list(m_project.objects.filter(size=0).values())
    index = 0
    for item in urls:
        print(item)
        start_urls.append(item['url'])
        index += 1
        if index == 1:
            break
    options = Options()
    options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    options.add_argument('--disable-gpu')
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--no-sandbox')
    prefs = {"download.default_directory": '/'}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)
    driver.get(start_urls[0])
    driver.find_element_by_xpath('//div[@class="login-reg fr"]/a[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//div[@class="login_b_x"]/a[1]').click()
    print('跳转QQ登陆网站', 'success')
    time.sleep(1)
    iframe = driver.find_element_by_xpath('//iframe[@id="ptlogin_iframe"]')
    driver.switch_to_frame(iframe)
    driver.find_element_by_xpath('//a[@id="switcher_plogin"]').click()
    user = driver.find_element_by_xpath('//input[@id="u"]')
    user.send_keys('1031308775')
    password = driver.find_element_by_xpath('//input[@id="p"]')
    password.send_keys('liquan137')
    driver.find_element_by_xpath('//input[@id="login_button"]').click()
    print('QQ登陆完成，返回目标网站', 'success')
    time.sleep(1)
    diccookie = driver.get_cookies()
    fw = open('cookie.txt', 'w')
    json.dump(diccookie, fw)
    fw.close()
    driver.quit()
    return True


def createFile():
    # 取当前时间戳
    pathtime = str(round(time.time()))
    # 定义图片存放路径
    path = os.getcwd() + '/img'
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
    urls = list(m_page_url.objects.filter(use=0).values())
    for item in urls:
        print(item)
        start_urls.append({
            'url': item['url'],
            'id': item['id']
        })
        index += 1
        if index == 20:
            break
    return start_urls


def scaleCutImg(path, filename, id, title, url):
    path_arr = filename.split('.')
    response = client.list_buckets()
    tong = response['Buckets']['Bucket'][0]['Name']
    name = float(time.time()) * 10000
    downName = str(round(name)) + '.' + path_arr[1]
    print(downName)
    try:
        with open(path + '/' + filename, 'rb') as fp:
            response = client.put_object(
                Bucket=tong,
                Body=fp,
                Key='/vip/' + downName,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        print(response['ETag'])
    except:
        print('文件下载出错！')

    scaleName = ''
    file_path = path + '/' + filename
    scale = 0.2
    type = filetype.guess(file_path)
    print(type.mime)

    img = Image.open(file_path)
    imgSize = str(img.size[0]) + 'x' + str(img.size[1])
    mode = img.mode
    size = list(img.size)
    if img.size[0] > 5000:
        scale = 0.3
    elif img.size[0] > 3000 and img.size[0] < 5000:
        scale = 0.35
    elif img.size[0] > 2000 and img.size[0] < 3000:
        scale = 0.4
    elif img.size[0] > 1000 and img.size[0] < 2000:
        scale = 0.6
    path_arr = filename.split('.')
    print(path_arr)
    viewName = 0
    if img.size[0] > 1000:
        print('尺寸', scale, '/', (int(img.size[0] * scale), int(img.size[1] * scale)))
        img.thumbnail((int(img.size[0] * scale), int(img.size[1] * scale)))
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
        if img.size[0] >= 1000:
            cropped = img.crop((176, 0, 800, 648))  # (left, upper, right, lower)

            try:
                os.remove(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                cropped.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                img = Image.open(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                img.thumbnail((int(img.size[0] * 0.7), int(img.size[1] * 0.7)))
                img.save(path + '/%sscale.%s' % (path_arr[0], path_arr[1]))
                scaleName = str(round(name)) + 'scale' + '.' + path_arr[1]
            except:
                os.remove(path + '/%sscale.%s' % (path_arr[0], 'png'))
                cropped.save(path + '/%sscale.%s' % (path_arr[0], 'png'))
                img = Image.open(path + '/%sscale.%s' % (path_arr[0], 'png'))
                img.thumbnail((int(img.size[0] * 0.7), int(img.size[1] * 0.7)))
                img.save(path + '/%sscale.%s' % (path_arr[0], 'png'))
                scaleName = str(round(name)) + 'scale' + '.png'
            print('缩放剪裁完成，文件名：' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'success')

        try:
            with open(path + '/' + '%sscale.%s' % (path_arr[0], path_arr[1]), 'rb') as fp:
                response = client.put_object(
                    Bucket=tong,
                    Body=fp,
                    Key='/scale/' + scaleName,
                    StorageClass='STANDARD',
                    EnableMD5=False
                )
        except:
            with open(path + '/' + '%sscale.%s' % (path_arr[0], 'png'), 'rb') as fp:
                response = client.put_object(
                    Bucket=tong,
                    Body=fp,
                    Key='/scale/' + scaleName,
                    StorageClass='STANDARD',
                    EnableMD5=False
                )
            os.remove(path + '/' + '%sscale.%s' % (path_arr[0], 'png'))
        print(response['ETag'])
        try:
            os.remove(path + '/' + filename)
            os.remove(path + '/' + '%sscale.%s' % (path_arr[0], path_arr[1]))
        except:
            print('没找到需要删除的文件,退出程序')
            exit()

    child = m_project(contact_id=id, url=url, title=title, down_png=downName,
                      size=imgSize, color_type=mode, file_type=type.mime,
                      scale=scaleName, img_view=viewName,
                      update_time=round(time.time()), create_time=round(time.time()))
    child.save()


def caiji():
    display = Display(visible=0, size=(800, 600))
    display.start()
    start_urls = returnUrl()
    path = createFile()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('Referer=' + url)
    # 指定谷歌浏览器路径
    prefs = {"download.default_directory": path}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options, executable_path=os.getcwd() + '/' + 'chromedriver')
    try:
        for url in start_urls:
            driver.get(url['url'])
            filename = 'content.html'
            with open(filename, 'wb') as f:
                f.write(driver.page_source.encode('utf-8'))
                print('保存采集HTML', 'success')
            # 模拟点击，进行下载

            # driver.quit()
            download_url = driver.find_element_by_xpath('//div[@id="pic_btn"]/a[3]').get_attribute('href')
            img = download_url.split('/')[len(download_url.split('/')) - 1].split('?')
            filename = img[0]
            title = driver.find_element_by_xpath('//div[@id="al_tit"]/h1').text
            print('下载文件的名称：' + filename, 'success')
            id_title = driver.find_element_by_xpath('//div[@class="pos"]/a[3]').text
            id = m_c_project.objects.get(title=id_title).id
            isExists = path + '/' + filename
            driver.find_element_by_xpath('//div[@id="pic_btn"]/a[3]').click()
            runtime = 0
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
            scaleCutImg(path, filename, id, title, url['url'])
            # 已经采集完图片的，就修改数据库中的采集状态
            commit = m_page_url.objects.get(id=url['id'])
            commit.use = 3
            commit.save()
        driver.quit()
        print('采集脚本完成，释放浏览器')
    except:
        print('采集脚本遇到错误，自动释放')
        driver.quit()


def main():
    print('采集脚本开始，自动登陆')
    caiji()
    # x = input()


if __name__ == '__main__':
    main()
