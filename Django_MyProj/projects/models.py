from django.db import models


class Projects(models.Model):
    """
    模型类名 -- 子应用名
    数据模型类，需要继承Model父类或者Model子类
    一个数据模型对应一个数据表, 类属性（Field对象）对应数据表中的字段
    """
    project_name = models.CharField(max_length=200)
    project_leader = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
