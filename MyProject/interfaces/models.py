from django_unixdatetimefield import UnixDateTimeField

from django.db import models


class Interfaces(models.Model):
    name = models.CharField(verbose_name='接口名称', max_length=200, unique=True, help_text='接口名称')
    projects = models.ForeignKey('projects.Projects', on_delete=models.SET_NULL, null=True, verbose_name='所属项目', help_text='所属项目', related_name='interface')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField(verbose_name='简要概述', max_length=200, help_text='简要概述', null=True, blank=True)

    class Meta:
        db_table = 'lemon_interfaces'
        verbose_name = '接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"<{self.name}>"
