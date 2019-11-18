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
    share = models.CharField(max_length=50, help_text="分享者", default=0)
    update_time = models.IntegerField(help_text="更新时间", default=1571453334)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_project_keyword(models.Model):
    contact = models.ForeignKey('m_project', on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50, help_text="关键词", unique=True)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_content_url(models.Model):
    url = models.CharField(max_length=100, help_text="地址", unique=True)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)



class m_page_url(models.Model):
    url = models.CharField(max_length=100, help_text="地址", unique=True)
    use = models.IntegerField(help_text="爬取状态", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)


class m_cookie(models.Model):
    cookie = models.TextField(help_text="cookie", default=0)
    create_time = models.IntegerField(help_text="创建时间", default=1571453334)
