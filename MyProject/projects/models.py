from django_unixdatetimefield import UnixDateTimeField

from django.db import models



class Projects(models.Model):
    # 设计项目表字段
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='项目名称', help_text='项目名称', unique=True)
    tester = models.CharField(max_length=50, verbose_name='测试人员', help_text='测试人员')
    programmer = models.CharField(max_length=50, verbose_name='开发人员', help_text='开发人员')
    desc = models.CharField(max_length=200, verbose_name='项目简介', help_text='项目简介', blank=True, default='项目简介', null=True)
    create_time = UnixDateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = UnixDateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        db_table = 'lemon_projects'
        verbose_name = '柠檬班项目表'

    def __str__(self):
        return f"<{self.name}>"
