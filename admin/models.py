from django.db import models


# Create your models here.

class m_copyright(models.Model):
    titile = models.CharField(max_length=700, help_text="版权说明")
    content = models.CharField(max_length=700, help_text="此作品是原创商用作品，所有原创作品（含预览图）均受著作权法保护，著作权及相关权利归{}所有，未经许可，不得转售",
                               default="此作品是原创商用作品，所有原创作品（含预览图）均受著作权法保护，著作权及相关权利归{}所有，未经许可，不得转售")


class m_f_project(models.Model):
    title = models.CharField(max_length=80, help_text="大类别名称", unique=True)
    url = models.CharField(max_length=100, help_text="采集地址", default=0)
    update_time = models.IntegerField(help_text="更新时间", default=1571453334)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_c_project(models.Model):
    title = models.CharField(max_length=80, help_text="小类别名称", unique=True)
    contact = models.ForeignKey('m_f_project', on_delete=models.CASCADE)
    url = models.CharField(max_length=100, help_text="采集地址", default=0)
    update_time = models.IntegerField(help_text="更新时间", default=1571453334)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_project(models.Model):
    contact = models.ForeignKey('m_c_project', on_delete=models.CASCADE)
    url = models.CharField(max_length=100, help_text="采集地址", default=0)
    title = models.CharField(max_length=80, help_text="素材名称")
    size = models.CharField(max_length=50, help_text="素材尺寸", default=0)
    scale = models.CharField(max_length=100, help_text="缩略图", default=0)
    color_type = models.CharField(max_length=50, help_text="素材颜色模式", default=0)
    down_png = models.CharField(max_length=600, help_text="png文件路径", default=0)
    down_zip = models.CharField(max_length=600, help_text="压缩文件路径", default=0)
    file_type = models.CharField(max_length=50, help_text="素材文件格式", default=0)
    img_view = models.CharField(max_length=50, help_text="图片预览", default=0)
    share = models.CharField(max_length=50, help_text="分享者", default=0)
    update_time = models.IntegerField(help_text="更新时间", default=1571453334)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    type = models.CharField(max_length=30, help_text="类别", default='pic')
    collect_num = models.BigIntegerField(help_text="收藏", default=0)
    down_num = models.BigIntegerField(help_text="下载", default=0)
    up_num = models.BigIntegerField(help_text="点赞", default=0)


class m_project_keyword(models.Model):
    contact = models.ForeignKey('m_project', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50, help_text="关键词", unique=True)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_content_url(models.Model):
    url = models.CharField(max_length=100, help_text="地址", unique=True)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_navbar(models.Model):
    title_f = models.CharField(max_length=80, help_text="首推关键词一")
    title_c = models.CharField(max_length=80, help_text="首推关键词二")
    contact_id = models.IntegerField(help_text="链接ID", default=0)
    contact_type = models.IntegerField(help_text="链接级别 1：一级； 2：二级", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_json(models.Model):
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    path = models.CharField(max_length=80, help_text="json存储位置")
    title = models.CharField(max_length=80, help_text="缓存标识", unique=True)


class m_page_url(models.Model):
    url = models.CharField(max_length=100, help_text="地址", unique=True)
    use = models.IntegerField(help_text="爬取状态", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_cookie(models.Model):
    cookie = models.TextField(help_text="cookie", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_seo(models.Model):
    title = models.CharField(max_length=80, help_text="网站标题", unique=True, default=0)
    keyword = models.TextField(help_text="网站keyword", default=0)
    desc = models.CharField(max_length=255, help_text="网站描述", unique=True, default=0)


class m_menber(models.Model):
    nickname = models.CharField(max_length=80, help_text="昵称", unique=True, default=0)
    desc = models.TextField(help_text="描述", default=0)
    headerimg = models.CharField(max_length=255, help_text="头像",
                                 default='https://blogs.4apn.cn/uploads/18027046690/20190415/fdbbb4e0e41a7e6f074c6135dd919d03.jpg')
    phone = models.BigIntegerField(help_text="手机号码", default=0, unique=True)
    email = models.CharField(max_length=80, help_text="邮箱", unique=True, default=0)
    auth = models.IntegerField(help_text="权限：1：终身会员 2：年费会员 3：季度会员 4：月费会员 0：普通会员", default=0)
    openid = models.CharField(max_length=80, help_text="openid", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    update_time = models.IntegerField(help_text="修改时间", default=1571453334)
    token = models.CharField(max_length=250, help_text="登陆密匙", default=0)
    unionid = models.CharField(max_length=80, help_text="唯一unionid", default=0)
    sex = models.CharField(max_length=80, help_text="性别", default=0)
    province = models.BigIntegerField(help_text="省", default=0)
    city = models.BigIntegerField(help_text="市", default=0)
    county = models.BigIntegerField(help_text="地区", default=0)
    address = models.CharField(max_length=80, help_text="详细地址", default=0)


class m_menber_resources_limit(models.Model):
    auth = models.IntegerField(help_text="权限：1：终身会员 2：年费会员 3：季度会员 4：月费会员 5：普通会员", default=0)
    limit_day = models.IntegerField(help_text="天下载限制", default=0)
    limit_hour = models.IntegerField(help_text="小时下载限制", default=0)
    limit_minute = models.IntegerField(help_text="分钟下载限制", default=0)


class m_menber_resources_down_limit(models.Model):
    user_id = models.BigIntegerField(help_text="绑定的用户ID", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    down_id = models.BigIntegerField(help_text="下载的文件ID", default=0)


class m_menber_collect(models.Model):
    user_id = models.BigIntegerField(help_text="绑定的用户ID", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    down_id = models.BigIntegerField(help_text="文件图片ID", default=0)


class m_menber_sms(models.Model):
    phone = models.BigIntegerField(help_text="关联手机号码", default=0)
    code = models.CharField(max_length=5, help_text="", default=0)
    is_use = models.IntegerField(help_text="是否使用 1：已经使用", default=0)
    use_type = models.IntegerField(help_text="使用场景 1：注册 2：找回密码 3：重设密码 4：支付验证 0：未启用", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    ip = models.CharField(max_length=80, help_text="ip地址", default=0)


class m_menber_designer(models.Model):
    user_id = models.BigIntegerField(help_text="绑定的用户ID", default=0, unique=True)
    phone = models.BigIntegerField(help_text="手机号码", default=0)
    name = models.CharField(max_length=250, help_text="姓名", default=0)
    card_1 = models.CharField(max_length=250, help_text="身份证正面", default=0)
    idCard = models.CharField(max_length=250, help_text="身份证号码", default=0)
    card_2 = models.CharField(max_length=250, help_text="身份证反面", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    states = models.CharField(max_length=250, help_text="状态", default=0)
    update = models.BigIntegerField(help_text="修改", default=1)
    msg = models.TextField(help_text="提示信息", default='')
    agree = models.CharField(max_length=50, help_text="用户同意授权证明", default='false')
    agree_time = models.IntegerField(help_text="签约时间", default=1571453334)


class m_menber_upload(models.Model):
    user_id = models.BigIntegerField(help_text="绑定的用户ID", default=0)
    file = models.CharField(max_length=250, help_text="上传的文件路径", default=0)
    md5 = models.CharField(max_length=250, help_text="计算得出的文件MD5", default=0, unique=True)
    type = models.IntegerField(help_text="1：身份证图片上传 2：其它图片上传 3：头像上传 4：原图上传 5：压缩文件上传 6：文档上传（ppt、word等） 7：源文件 8：视频文件",
                               default=0)
    title = models.CharField(max_length=250, help_text="文件标题", default=0)
    file_suffix = models.CharField(max_length=250, help_text="文件后缀", default=0)
    is_scale = models.IntegerField(help_text="上传时候是否有缩略图 1：有 2：无", default=1)
    scale = models.CharField(max_length=250, help_text="缩略图", default='')
    size = models.CharField(max_length=250, help_text="尺寸", default='')
    mine = models.CharField(max_length=250, help_text="文件类型", default='')
    c_type = models.CharField(max_length=250, help_text="类型", default='')
    is_auth = models.IntegerField(help_text="是否释放上传单次限制 1：释放（通过审核） 2：冻结(待审核，占用上传次数) 3:审核失败", default=2)
    remarks = models.TextField(help_text="备注", default='')
    keyword = models.TextField(help_text="关键词", default='')
    error = models.CharField(max_length=250, help_text="错误提示", default='')
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_activity(models.Model):
    title = models.CharField(max_length=80, help_text="活动标题")
    desc = models.TextField(help_text="活动内容")
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
    update_time = models.IntegerField(help_text="更新时间", default=1571453334)
    start_time = models.IntegerField(help_text="创建时间", default=1571453334)
    end_time = models.IntegerField(help_text="结束时间", default=1571453334)
