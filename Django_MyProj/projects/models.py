from django.db import models


class Projects(models.Model):
    """
    模型类名 -- 子应用名
    数据模型类，需要继承Model父类或者Model子类
    一个数据模型对应一个数据表, 类属性（Field对象）对应数据表中的字段
    """
    project_id = models.AutoField(primary_key=True)
    # verbose_name：个性化信息，help_text帮助文本信息，在api接口文档平台和admin后端站点中会用于提示，一般和verbose_name一致
    # unique：字段值唯一
    # charField至少指定一个max_length，限制最大长度
    name = models.CharField(max_length=200, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=50, verbose_name='项目负责人', help_text='项目负责人')
    tester = models.CharField(max_length=50, verbose_name='测试人员', help_text='测试人员')
    programmer = models.CharField(max_length=50,verbose_name='开发人员', help_text='开发人员')
    # null：指定数据在保存时是否可以为空，默认必填，如果null为True，则可以为空
    # blank：指定前端用户在创建数据时，是否需要传递，默认需要，如不传递，则blank为True
    # defalut：为某一个字段指定默认值，往往会和blank一起使用
    desc = models.TextField(verbose_name='项目简介', help_text='项目简介', blank=True, default='项目简介', null=True)
    # auto_now_add：自动添加记录创建的时间，auto_now：记录更新的时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', help_text='创建时间')
    # update_time只有在调用save方法的时候才会自动更新
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', help_text='更新时间')

    class Meta:
        """
        可在模型类下定义子类，子类名称固定为Meta
        可使用db_table属性，指定表名
        """
        db_table = 'tb_projects'
        verbose_name = '项目表'

    def __str__(self):
        return f"{self}"


