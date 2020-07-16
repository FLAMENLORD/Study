from django.db import models


class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=50, verbose_name='项目负责人', help_text='项目负责人')
    tester = models.CharField(max_length=50, verbose_name='测试人员', help_text='测试人员')
    programmer = models.CharField(max_length=50,verbose_name='开发人员', help_text='开发人员')
    desc = models.TextField(verbose_name='项目简介', help_text='项目简介', blank=True, default='项目简介', null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        db_table = 'tb_projects'
        verbose_name = '项目表'

    def __repr__(self):
        return f"{self}"


