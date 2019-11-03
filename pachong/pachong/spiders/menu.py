import scrapy
from scrapy.selector import Selector
from ..items import *
from pypinyin import pinyin, lazy_pinyin
from ..pipelines import *
from admin.models import *
import time
import json
from scrapy_splash import SplashRequest


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
    start_urls = [
        "http://669pic.com/",
    ]

    def parse(self, response):
        items = []
        filename = 'menu.html'
        start_urls = "http://669pic.com"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for each in response.selector.xpath('//ul[@class="header-ul cl"]/li'):
            item = {}
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
        file = 'menu_json/nav.json'
        with open(file, 'w') as f:
            data = json.dumps({'object': items}, ensure_ascii=False)
            f.write(data)
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
class List3Spider(scrapy.spiders.Spider):
    name = "list3"
    allowed_domains = [""]
    urls = list(m_contents_url.objects.all().values())
    start_urls = []
    # for urlItem in urls:
    #     url = urlItem['url'].split('/bizhi')
    #     start_urls.append('https://www.ivsky.com/bizhi' + url[2])

    for urlItem in range(1447, 1510):
        print(urls[urlItem])
        url = urls[urlItem]['url'].split('/bizhi')
        print('当前位置：', urlItem)
        start_urls.append('https://www.ivsky.com/bizhi' + url[2])

    def parse(self, response):
        items = []
        filename = 'menu.html'
        start_urls = "https://www.ivsky.com"
        with open(filename, 'wb') as f:
            f.write(response.body)
        for each in response.selector.xpath('//ul[@class="pli"]/li'):
            item = {}
            item['title'] = each.xpath('./p/a/text()').extract()[0]
            item['url'] = start_urls + each.xpath('./p/a/@href').extract()[0]
            try:
                father = m_page_url(url=item['url'], create_time=round(time.time()))
                father.save()
            except:
                None
            items.append(item)
        return items


# 爬取天堂图片网
# scrapy crawl imgselect
class ImgselectSpider(scrapy.spiders.Spider):
    name = "imgselect"
    allowed_domains = [""]
    urls = list(m_page_url.objects.all().values())
    start_urls = []
    for index in range(0, 10):
        start_urls.append(urls[index]['url'])

    def parse(self, response):
        items = []
        filename = 'menu.html'
        start_urls = "https://www.ivsky.com/bizhi"
        with open(filename, 'wb') as f:
            f.write(response.body)
        title = response.selector.xpath('//div[@class="pos"]/a[3]/text()').extract()[0]
        id = m_c_project.objects.get(title=title).contact_id
        item = FileItem()
        download_url = response.selector.xpath('//div[@id="pic_btn"]/a[3]/@href').extract()[0]
        item['down_png'] = [download_url]
        item['title'] = response.selector.xpath('//div[@id="al_tit"]/h1/text()').extract()[0]
        item['size'] = response.selector.xpath('//div[@id="pic_info"]/span[1]/text()').extract()[0]
        item['upload_time'] = round(time.time())
        item['create_time'] = round(time.time())
        item['file_type'] = 'jpg/png'
        item['color_type'] = 'RBG'
        print(item)
        items.append(item)
        return items
