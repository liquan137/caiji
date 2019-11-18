import scrapy
from scrapy.selector import Selector
from ..items import *
from pypinyin import pinyin, lazy_pinyin
from ..pipelines import *
from admin.models import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
from django.db import close_old_connections


def close_old_connections_wrapper(func):
    def wrapper(*args, **kwargs):
        close_old_connections()
        return func(*args, **kwargs)

    return wrapper


# scrapy crawl menu_1
class MenuSpider(scrapy.spiders.Spider):
    name = "menu_1"
    allowed_domains = [""]
    start_urls = [
        "http://669pic.com/",
    ]

    def parse(self, response):
        items = []
        filename = 'menu.html'
        start_urls = "http://669pic.com/"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for each in response.selector.xpath('//ul[@class="header-ul cl"]/li'):
            item = {}
            print('pinyin', lazy_pinyin(each.xpath('./a/text()').extract()[0]))
            item['title'] = each.xpath('./a/text()').extract()[0]
            item['url'] = start_urls + each.xpath('./a/@href').extract()[0]
            try:
                if 'VIP' not in item['title']:
                    father = m_f_project(url=item['url'], title=item['title'], update_time=round(time.time()),
                                         create_time=round(time.time()))
                    father.save()
            except:
                None
            items.append(item)
        print(items)
        return items


# scrapy crawl menu_2
class Menu2Spider(scrapy.spiders.Spider):
    name = "menu_2"
    allowed_domains = ["dmoz.org"]
    start_urls = []
    urls = list(m_project.objects.filter(size=0).values())
    index = 0
    for item in urls:
        print(item)
        start_urls.append(item['url'])
        break


    def parse(self, response):
        items = []
        fp = webdriver.FirefoxProfile()
        # 自定义路径下载
        fp.set_preference("browser.download.folderList", 2)

        options = webdriver.FirefoxOptions()
        # 设置静默模式
        options.add_argument('-headless')
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
        fp.set_preference("browser.download.dir", path)
        # 下载的格式
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
        driver = webdriver.Firefox(firefox_profile=fp)
        driver.get(response.url)
        filename = 'content.html'
        with open(filename, 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))
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
        time.sleep(2)
        diccookie = driver.get_cookies()
        fw = open('baiducookie.txt', 'w')
        json.dump(diccookie, fw)
        fw.close()
        # 关闭
        # driver.quit()
        # item = FileItem()
        # download_url = '0'
        # item['down_png'] = ['https:' + download_url]
        # item['title'] = response.selector.xpath('//div[@class="left-content-title-box"]/h2/text()').extract()[0]
        # item['size'] = 'UnKnow'
        # item['upload_time'] = round(time.time())
        # item['create_time'] = round(time.time())
        # item['file_type'] = 'UnKnow'
        # item['color_type'] = 'RBG'
        # item['image_urls'] = '0'
        # img = '0'
        # item['images'] = '0'
        # # 合成下载文件的路径
        # filePath = 'img/' + pathtime
        # # 查询当前图片所属的类别 并返回ID
        # id_title = response.selector.xpath('//div[@class="bread_nav"]/a[2]/text()').extract()[0]
        # id = m_c_project.objects.get(title=id_title).id
        # try:
        #     # 存入数据库
        #     child = m_project(contact_id=id, url=response.url, title=item['title'], down_png=filePath,
        #                       size=item['size'], color_type=item['color_type'], file_type=item['file_type'],
        #                       update_time=round(time.time()), create_time=round(time.time()))
        #     child.save()
        #     # 已经采集完图片的，就修改数据库中的采集状态
        #     commit = m_page_url.objects.get(url=response.url)
        #     commit.use = 1
        #     commit.save()
        # except:
        #     None
        # items.append(item)
        return items


# scrapy crawl client
class ClientSpider(scrapy.spiders.Spider):
    name = "client"
    start_urls = []
    urls = list(m_project.objects.filter(size=0).values())
    index = 0
    for item in urls:
        print(item)
        start_urls.append(item['url'])
        index += 1
        if index == 10:
            break

    def parse(self, response):
        fr = open('baiducookie.txt', 'r')
        cookielist = json.load(fr)
        fr.close()
        items = []
        fp = webdriver.FirefoxProfile()
        # 自定义路径下载
        fp.set_preference("browser.download.folderList", 2)

        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('Referer=' + response.url)

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
        fp.set_preference("browser.download.dir", path)
        # 下载的格式
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
        # 指定谷歌浏览器路径
        prefs = {"download.default_directory": path}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(response.url)
        for cookie in cookielist:
            driver.add_cookie(cookie)
        driver.get(response.url)
        filename = 'content.html'
        with open(filename, 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))
        # 模拟点击，进行下载
        driver.find_element_by_xpath(
            '//div[@class="right_content fl"]/div[@class="like_down_box right_sub_box"]/a[1]').click()
        time.sleep(2)
        # 关闭
        driver.quit()
        item = FileItem()
        download_url = '0'
        item['down_png'] = ['https:' + download_url]
        item['title'] = response.selector.xpath('//div[@class="left-content-title-box cl"]/h2/text()').extract()[0]
        item['size'] = 'UnKnow'
        item['upload_time'] = round(time.time())
        item['create_time'] = round(time.time())
        item['file_type'] = 'UnKnow'
        item['color_type'] = 'RBG'
        item['image_urls'] = '0'
        img = '0'
        item['images'] = '0'
        # 合成下载文件的路径
        filePath = 'img/' + pathtime
        # 查询当前图片所属的类别 并返回ID
        id_title = response.selector.xpath('//div[@class="bread_nav"]/a[2]/text()').extract()[0]
        id = m_c_project.objects.get(title=id_title).id
        try:
            # 存入数据库
            child = m_project(contact_id=id, url=response.url, title=item['title'], down_png=filePath,
                              size=item['size'], color_type=item['color_type'], file_type=item['file_type'],
                              update_time=round(time.time()), create_time=round(time.time()))
            child.save()
            # 已经采集完图片的，就修改数据库中的采集状态
            commit = m_page_url.objects.get(url=response.url)
            commit.use = 1
            commit.save()
        except:
            None
        items.append(item)
        return items


# scrapy crawl list
class ListSpider(scrapy.spiders.Spider):
    name = "list"
    allowed_domains = ["dmoz.org"]
    urls = list(m_f_project.objects.all().values())
    start_urls = []
    for urlItem in urls:
        print('url', urlItem['url'])
        start_urls.append(urlItem['url'])

    def parse(self, response):
        urls = list(m_f_project.objects.all().values())
        items = []
        filename = 'list.html'
        start_urls = "http://669pic.com"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for urlItem in urls:
            if urlItem['title'] in response.selector.xpath('//div[@class="bread_nav"]/h1/text()').extract()[0]:
                id = urlItem['id']
        for each in response.selector.xpath('//div[@class="cate"]/h2'):
            item = {}
            # print('pinyin', lazy_pinyin(each.xpath('./a/text()').extract()[0]))
            item['title'] = each.xpath('./a/text()').extract()[0]
            item['url'] = start_urls + each.xpath('./a/@href').extract()[0]
            try:
                child = m_c_project(contact_id=id, url=item['url'], title=item['title'],
                                    update_time=round(time.time()), create_time=round(time.time()))
                child.save()
            except:
                None
            items.append(item)
        print(items)
        return items


# scrapy crawl content
class ContentSpider(scrapy.spiders.Spider):
    name = "content"
    allowed_domains = ["content.org"]
    urls = list(m_content_url.objects.all().values())
    start_urls = []
    for urlItem in urls:
        print('url', urlItem['url'])
        start_urls.append(urlItem['url'])

    def parse(self, response):
        urls = list(m_c_project.objects.all().values())
        items = []
        filename = 'list.html'
        start_urls = "http://669pic.com"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for urlItem in urls:
            print('title', response.selector.xpath('//div[@class="bread_nav"]/a[last()]/text()').extract()[0])
            if urlItem['title'] in response.selector.xpath('//div[@class="bread_nav"]/a[last()]/text()').extract()[0]:
                id = urlItem['id']
        for each in response.selector.xpath('//div[@class="content_list"]/li'):
            item = {}
            # print('pinyin', lazy_pinyin(each.xpath('./a/text()').extract()[0]))
            item['id'] = id
            item['title'] = each.xpath('./div[@class="imgTxtInfo"]/h3/a/text()').extract()[0]
            item['url'] = start_urls + each.xpath('./div[@class="imgTxtInfo"]/h3/a/@href').extract()[0]
            try:
                child = m_project(contact_id=id, url=item['url'], title=item['title'],
                                  update_time=round(time.time()), create_time=round(time.time()))
                child.save()
            except:
                None
            items.append(item)
        print(items)
        return items


# scrapy crawl page
class PageSpider(scrapy.spiders.Spider):
    name = "page"
    allowed_domains = []
    urls = list(m_c_project.objects.all().values())
    start_urls = []
    for urlItem in urls:
        print('url', urlItem['url'])
        start_urls.append(urlItem['url'])

    def parse(self, response):
        urls = list(m_c_project.objects.all().values())
        items = []
        filename = 'list.html'
        start_urls = "http://669pic.com"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for urlItem in urls:
            if urlItem['title'] in response.selector.xpath('//div[@class="bread_nav"]/a[last()]/text()').extract()[0]:
                id = urlItem['id']
            else:
                id = 0
        for each in response.selector.xpath('//div[@class="pager-linkPage"]/a'):
            item = {}
            # print('pinyin', lazy_pinyin(each.xpath('./a/text()').extract()[0]))
            item['id'] = id
            item['title'] = each.xpath('text()').extract()[0]
            item['url'] = each.xpath('@href').extract()[0]
            try:
                child = m_content_url(url=item['url'], create_time=round(time.time()))
                child.save()
            except:
                None
            items.append(item)
        return items


# scrapy crawl ip
class IpSpider(scrapy.spiders.Spider):
    name = 'ip'
    allowed_domains = []

    def start_requests(self):
        url = 'http://ip.chinaz.com/getip.aspx'

        for i in range(4):
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(response.text)


# 爬取天堂图片网
# scrapy crawl menu_3
class Menu3Spider(scrapy.spiders.Spider):
    name = "menu_3"
    allowed_domains = [""]
    start_urls = [
        "https://www.ivsky.com/bizhi/",
    ]

    def parse(self, response):
        items = []
        filename = 'menu.html'
        start_urls = "https://www.ivsky.com/bizhi"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for each in response.selector.xpath('//ul[@class="bzmenu"]/li'):
            item = {}
            item['title'] = each.xpath('./a/text()').extract()[0]
            item['url'] = start_urls + each.xpath('./a/@href').extract()[0]
            try:
                father = m_c_project(contact_id=5, url=item['url'], title=item['title'],
                                     update_time=round(time.time()),
                                     create_time=round(time.time()))
                father.save()
            except:
                None
            items.append(item)
        return items


# 爬取天堂图片网
# scrapy crawl list2
class List2Spider(scrapy.spiders.Spider):
    name = "list2"
    allowed_domains = [""]
    urls = list(m_c_project.objects.filter(contact_id=5).values())
    start_urls = []
    for urlItem in range(0, 100):
        start_urls.append("https://www.ivsky.com/bizhi/" + 'index_' + str(urlItem) + '.html')

    def parse(self, response):
        items = []
        filename = 'menu.html'
        start_urls = "https://www.ivsky.com/"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for each in response.selector.xpath('//ul[@class="ali"]/li'):
            item = {}
            item['title'] = each.xpath('./p/a/text()').extract()[0]
            item['url'] = start_urls + each.xpath('./p/a/@href').extract()[0]
            try:
                father = m_contents_url(url=item['url'], create_time=round(time.time()))
                father.save()
            except:
                None
            items.append(item)
        return items


# 爬取天堂图片网
# scrapy crawl list3
# class List3Spider(scrapy.spiders.Spider):
#     name = "list3"
#     allowed_domains = [""]
#     urls = list(m_contents_url.objects.all().values())
#     start_urls = []
#     for urlItem in urls:
#         url = urlItem['url'].split('/bizhi')
#         start_urls.append('https://www.ivsky.com/bizhi' + url[2])
#
#     for urlItem in range(1447, 1510):
#         print(urls[urlItem])
#         url = urls[urlItem]['url'].split('/bizhi')
#         print('当前位置：', urlItem)
#         start_urls.append('https://www.ivsky.com/bizhi' + url[2])
#
#     def parse(self, response):
#         items = []
#         filename = 'menu.html'
#         start_urls = "https://www.ivsky.com"
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         for each in response.selector.xpath('//ul[@class="pli"]/li'):
#             item = {}
#             item['title'] = each.xpath('./p/a/text()').extract()[0]
#             item['url'] = start_urls + each.xpath('./p/a/@href').extract()[0]
#             try:
#                 father = m_page_url(url=item['url'], create_time=round(time.time()))
#                 father.save()
#             except:
#                 None
#             items.append(item)
#         return items


# 爬取天堂图片网
# scrapy crawl imgselect
class ImgselectSpider(scrapy.spiders.Spider):
    name = "imgselect"
    allowed_domains = [""]

    # 获取数据库中需要采集的网址内容页
    url = list(m_page_url.objects.filter(use=0).values())
    start_urls = []
    # 遍历列表并生成url数组
    for index in url:
        start_urls.append(index['url'])

    @close_old_connections_wrapper
    def parse(self, response):
        items = []
        # 开启火狐浏览器驱动
        fp = webdriver.FirefoxProfile()
        # 自定义路径下载
        fp.set_preference("browser.download.folderList", 2)

        options = webdriver.FirefoxOptions()
        # 设置静默模式
        options.add_argument('-headless')
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
        fp.set_preference("browser.download.dir", path)
        # 下载的格式
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/jpeg")
        driver = webdriver.Firefox(firefox_profile=fp, options=options)
        driver.get(response.url)
        # 模拟点击，进行下载
        driver.find_element_by_xpath('//div[@id="pic_btn"]/a[3]').click()
        # 延时 2秒等待下载完毕
        time.sleep(3)
        # 关闭
        driver.quit()
        # 定义item，这里其实没必要了，我已经直接存数据库了
        item = FileItem()
        download_url = response.selector.xpath('//div[@id="pic_btn"]/a[3]/@href').extract()[0]
        item['down_png'] = ['https:' + download_url]
        item['title'] = response.selector.xpath('//div[@id="al_tit"]/h1/text()').extract()[0]
        item['size'] = response.selector.xpath('//div[@id="pic_info"]/span[1]/text()').extract()[0]
        item['upload_time'] = round(time.time())
        item['create_time'] = round(time.time())
        item['file_type'] = 'jpg/png'
        item['color_type'] = 'RBG'
        item['image_urls'] = ['https:' + download_url]
        img = download_url.split('/')[len(download_url.split('/')) - 1].split('?')
        item['images'] = [img[0]]
        # 合成下载文件的路径
        filePath = 'img/' + pathtime + '/' + img[0]
        # 查询当前图片所属的类别 并返回ID
        id_title = response.selector.xpath('//div[@class="pos"]/a[3]/text()').extract()[0]
        id = m_c_project.objects.get(title=id_title).id
        try:
            # 存入数据库
            child = m_project(contact_id=id, url=response.url, title=item['title'], down_png=filePath,
                              size=item['size'], color_type=item['color_type'], file_type=item['file_type'],
                              update_time=round(time.time()), create_time=round(time.time()))
            child.save()
            # 已经采集完图片的，就修改数据库中的采集状态
            commit = m_page_url.objects.get(url=response.url)
            commit.use = 1
            commit.save()
        except:
            None
        items.append(item)
        return items
