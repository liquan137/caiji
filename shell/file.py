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

def main():
    response = client.get_presigned_download_url(
        Bucket='kutucn-1256750707',
        Key='15747547313522.jpg'
    )
    print(response)

if __name__ == '__main__':
    main()
