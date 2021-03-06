# Generated by Django 3.0.7 on 2020-06-26 15:41

from django.db import migrations, models
import django_unixdatetimefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='项目名称', max_length=200, unique=True, verbose_name='项目名称')),
                ('tester', models.CharField(help_text='测试人员', max_length=50, verbose_name='测试人员')),
                ('programmer', models.CharField(help_text='开发人员', max_length=50, verbose_name='开发人员')),
                ('desc', models.CharField(blank=True, default='项目简介', help_text='项目简介', max_length=200, null=True, verbose_name='项目简介')),
                ('create_time', django_unixdatetimefield.fields.UnixDateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', django_unixdatetimefield.fields.UnixDateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '柠檬班项目表',
                'db_table': 'lemon_projects',
            },
        ),
    ]
