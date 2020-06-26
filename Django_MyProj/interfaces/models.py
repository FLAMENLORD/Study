from django.db import models


class Interfaces(models.Model):
    name = models.CharField(verbose_name='接口名称', max_length=200, unique=True, help_text='接口名称')
    # ForeignKey指定外键字段
    # 第一个参数必传，是父表模型类的引用（模型类名or子应用名.父表模型类名）
    # 第二个参数on_delete必传，指定父表记录被删除之后，子表中对应记录的处理方式
    # models.CASCADE：父表记录被删，子表自动删除
    # models.SET_NULL, null=True：父表记录删除，子表自动设置为空
    # models.DEFAULT：父表记录删除，子表自动设置默认值
    projects = models.ForeignKey('projects.Projects', on_delete=models.SET_NULL, null=True, verbose_name='所属项目', help_text='所属项目')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField(verbose_name='简要概述', max_length=200, help_text='简要概述', null=True, blank=True)

    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口信息'
        # 数据库模型类的复数
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name