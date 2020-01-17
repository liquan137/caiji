# Generated by Django 2.2.3 on 2020-01-11 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='m_activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='活动标题', max_length=80)),
                ('desc', models.TextField(help_text='活动内容')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('update_time', models.IntegerField(default=1571453334, help_text='更新时间')),
                ('start_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('end_time', models.IntegerField(default=1571453334, help_text='结束时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_c_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='小类别名称', max_length=80, unique=True)),
                ('url', models.CharField(default=0, help_text='采集地址', max_length=100)),
                ('update_time', models.IntegerField(default=1571453334, help_text='更新时间')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_content_url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(help_text='地址', max_length=100, unique=True)),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_cookie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cookie', models.TextField(default=0, help_text='cookie')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_copyright',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titile', models.CharField(help_text='版权说明', max_length=700)),
                ('content', models.CharField(default='此作品是原创商用作品，所有原创作品（含预览图）均受著作权法保护，著作权及相关权利归{}所有，未经许可，不得转售', help_text='此作品是原创商用作品，所有原创作品（含预览图）均受著作权法保护，著作权及相关权利归{}所有，未经许可，不得转售', max_length=700)),
            ],
        ),
        migrations.CreateModel(
            name='m_f_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='大类别名称', max_length=80, unique=True)),
                ('url', models.CharField(default=0, help_text='采集地址', max_length=100)),
                ('update_time', models.IntegerField(default=1571453334, help_text='更新时间')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_json',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('path', models.CharField(help_text='json存储位置', max_length=80)),
                ('title', models.CharField(help_text='缓存标识', max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='m_menber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(default=0, help_text='昵称', max_length=80, unique=True)),
                ('desc', models.TextField(default=0, help_text='描述')),
                ('headerimg', models.CharField(default='https://blogs.4apn.cn/uploads/18027046690/20190415/fdbbb4e0e41a7e6f074c6135dd919d03.jpg', help_text='头像', max_length=255)),
                ('phone', models.BigIntegerField(default=0, help_text='手机号码', unique=True)),
                ('email', models.CharField(default=0, help_text='邮箱', max_length=80, unique=True)),
                ('auth', models.IntegerField(default=0, help_text='权限：1：终身会员 2：年费会员 3：季度会员 4：月费会员 0：普通会员')),
                ('openid', models.CharField(default=0, help_text='openid', max_length=80)),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('update_time', models.IntegerField(default=1571453334, help_text='修改时间')),
                ('token', models.CharField(default=0, help_text='登陆密匙', max_length=250)),
                ('unionid', models.CharField(default=0, help_text='唯一unionid', max_length=80)),
                ('sex', models.CharField(default=0, help_text='性别', max_length=80)),
                ('province', models.BigIntegerField(default=0, help_text='省')),
                ('city', models.BigIntegerField(default=0, help_text='市')),
                ('county', models.BigIntegerField(default=0, help_text='地区')),
                ('address', models.CharField(default=0, help_text='详细地址', max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='m_menber_collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(default=0, help_text='绑定的用户ID')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('down_id', models.BigIntegerField(default=0, help_text='文件图片ID')),
            ],
        ),
        migrations.CreateModel(
            name='m_menber_designer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(default=0, help_text='绑定的用户ID', unique=True)),
                ('phone', models.BigIntegerField(default=0, help_text='手机号码')),
                ('name', models.CharField(default=0, help_text='姓名', max_length=250)),
                ('card_1', models.CharField(default=0, help_text='身份证正面', max_length=250)),
                ('idCard', models.CharField(default=0, help_text='身份证号码', max_length=250)),
                ('card_2', models.CharField(default=0, help_text='身份证反面', max_length=250)),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('states', models.CharField(default=0, help_text='状态', max_length=250)),
                ('update', models.BigIntegerField(default=1, help_text='修改')),
                ('msg', models.TextField(default='', help_text='提示信息')),
                ('agree', models.CharField(default='false', help_text='用户同意授权证明', max_length=50)),
                ('agree_time', models.IntegerField(default=1571453334, help_text='签约时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_menber_resources_down_limit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(default=0, help_text='绑定的用户ID')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('down_id', models.BigIntegerField(default=0, help_text='下载的文件ID')),
            ],
        ),
        migrations.CreateModel(
            name='m_menber_resources_limit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth', models.IntegerField(default=0, help_text='权限：1：终身会员 2：年费会员 3：季度会员 4：月费会员 5：普通会员')),
                ('limit_day', models.IntegerField(default=0, help_text='天下载限制')),
                ('limit_hour', models.IntegerField(default=0, help_text='小时下载限制')),
                ('limit_minute', models.IntegerField(default=0, help_text='分钟下载限制')),
            ],
        ),
        migrations.CreateModel(
            name='m_menber_sms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.BigIntegerField(default=0, help_text='关联手机号码')),
                ('code', models.CharField(default=0, max_length=5)),
                ('is_use', models.IntegerField(default=0, help_text='是否使用 1：已经使用')),
                ('use_type', models.IntegerField(default=0, help_text='使用场景 1：注册 2：找回密码 3：重设密码 4：支付验证 0：未启用')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('ip', models.CharField(default=0, help_text='ip地址', max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='m_menber_upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(default=0, help_text='绑定的用户ID')),
                ('file', models.CharField(default=0, help_text='上传的文件路径', max_length=250)),
                ('md5', models.CharField(default=0, help_text='计算得出的文件MD5', max_length=250, unique=True)),
                ('type', models.IntegerField(default=0, help_text='1：身份证图片上传 2：其它图片上传 3：头像上传 4：原图上传 5：压缩文件上传 6：文档上传（ppt、word等） 7：源文件 8：视频文件')),
                ('title', models.CharField(default=0, help_text='文件标题', max_length=250)),
                ('file_suffix', models.CharField(default=0, help_text='文件后缀', max_length=250)),
                ('is_scale', models.IntegerField(default=1, help_text='上传时候是否有缩略图 1：有 2：无')),
                ('scale', models.CharField(default='', help_text='缩略图', max_length=250)),
                ('is_auth', models.IntegerField(default=2, help_text='是否释放上传单次限制 1：释放 2：冻结')),
                ('remarks', models.TextField(default='', help_text='备注')),
                ('keyword', models.TextField(default='', help_text='备注')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_navbar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_f', models.CharField(help_text='首推关键词一', max_length=80)),
                ('title_c', models.CharField(help_text='首推关键词二', max_length=80)),
                ('contact_id', models.IntegerField(default=0, help_text='链接ID')),
                ('contact_type', models.IntegerField(default=0, help_text='链接级别 1：一级； 2：二级')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_page_url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(help_text='地址', max_length=100, unique=True)),
                ('use', models.IntegerField(default=0, help_text='爬取状态')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=0, help_text='采集地址', max_length=100)),
                ('title', models.CharField(help_text='素材名称', max_length=80)),
                ('size', models.CharField(default=0, help_text='素材尺寸', max_length=50)),
                ('scale', models.CharField(default=0, help_text='缩略图', max_length=100)),
                ('color_type', models.CharField(default=0, help_text='素材颜色模式', max_length=50)),
                ('down_png', models.CharField(default=0, help_text='png文件路径', max_length=600)),
                ('down_zip', models.CharField(default=0, help_text='压缩文件路径', max_length=600)),
                ('file_type', models.CharField(default=0, help_text='素材文件格式', max_length=50)),
                ('img_view', models.CharField(default=0, help_text='图片预览', max_length=50)),
                ('share', models.CharField(default=0, help_text='分享者', max_length=50)),
                ('update_time', models.IntegerField(default=1571453334, help_text='更新时间')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('type', models.CharField(default='pic', help_text='类别', max_length=30)),
                ('collect_num', models.BigIntegerField(default=0, help_text='收藏')),
                ('down_num', models.BigIntegerField(default=0, help_text='下载')),
                ('up_num', models.BigIntegerField(default=0, help_text='点赞')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.m_c_project')),
            ],
        ),
        migrations.CreateModel(
            name='m_seo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=0, help_text='网站标题', max_length=80, unique=True)),
                ('keyword', models.TextField(default=0, help_text='网站keyword')),
                ('desc', models.CharField(default=0, help_text='网站描述', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='m_project_keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(help_text='关键词', max_length=50, unique=True)),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.m_project')),
            ],
        ),
        migrations.AddField(
            model_name='m_c_project',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin.m_f_project'),
        ),
    ]
