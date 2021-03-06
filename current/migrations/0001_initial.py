# Generated by Django 2.2.3 on 2019-11-01 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='m_menber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(help_text='关联用户', max_length=30)),
                ('nickname', models.CharField(default='', help_text='昵称', max_length=30)),
                ('password', models.CharField(help_text='密码', max_length=90)),
                ('phone', models.IntegerField(default=0, help_text='手机')),
                ('email', models.EmailField(default=0, help_text='邮箱', max_length=254)),
                ('header_img', models.CharField(default='https://thirdwx.qlogo.cn/mmopen/vi_32/jJEaSPkhKKq0oia9qpSvGRElZnR9AcOiaBGncIzAb1Eic04pcg2dTz9v5Twx47GGoMdnqmdsniaP7rW8MrrAaDP3mA/132', help_text='头像', max_length=50)),
                ('auth', models.IntegerField(default=1, help_text='封禁 1：正常 2：封禁')),
                ('auth_photo', models.IntegerField(default=400, help_text='图片上传次数限制')),
                ('auth_msg', models.IntegerField(default=3, help_text='发布设计或其它需求信息次数限制')),
                ('auth_photo_down', models.IntegerField(default=400, help_text='图片下载次数限制')),
                ('identity_type', models.IntegerField(default=0, help_text='第三方登录类型,0为未使用')),
                ('identity_token', models.CharField(help_text='第三方登录的刷新token', max_length=500)),
                ('update_time', models.IntegerField(default=1571453334, help_text='更新时间')),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='m_menber_ip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(help_text='ip地址', max_length=30)),
                ('create_time', models.IntegerField(default=1571453334, help_text='创建时间')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='current.m_menber')),
            ],
        ),
    ]
