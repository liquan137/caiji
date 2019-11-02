from django.db import models

# Create your models here.

class m_menber(models.Model):
    username = models.CharField(max_length=30, help_text="关联用户")
    nickname = models.CharField(max_length=30, help_text="昵称", default="")
    password = models.CharField(max_length=90, help_text="密码")
    phone = models.IntegerField(help_text="手机", default=0)
    email = models.EmailField(help_text="邮箱", default=0)
    header_img = models.CharField(max_length=50, help_text="头像",
                                  default="https://thirdwx.qlogo.cn/mmopen/vi_32/jJEaSPkhKKq0oia9qpSvGRElZnR9AcOiaBGncIzAb1Eic04pcg2dTz9v5Twx47GGoMdnqmdsniaP7rW8MrrAaDP3mA/132")
    auth = models.IntegerField(help_text="封禁 1：正常 2：封禁", default=1)
    auth_photo = models.IntegerField(help_text="图片上传次数限制", default=400)
    auth_msg = models.IntegerField(help_text="发布设计或其它需求信息次数限制", default=3)
    auth_photo_down = models.IntegerField(help_text="图片下载次数限制", default=400)
    identity_type = models.IntegerField(help_text="第三方登录类型,0为未使用", default=0)
    identity_token = models.CharField(max_length=500, help_text="第三方登录的刷新token")
    update_time = models.IntegerField(help_text="更新时间", default=1571453334)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_menber_ip(models.Model):
    ip = models.CharField(max_length=30, help_text="ip地址")
    contact = models.ForeignKey('m_menber', on_delete=models.CASCADE)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
