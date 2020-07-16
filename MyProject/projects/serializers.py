from rest_framework import serializers
from .models import Projects
from interfaces.models import Interfaces

# from interfaces.serializers import InterfacesModelSerializer

import locale
locale.setlocale(locale.LC_CTYPE, 'chinese')
datatime_fmt = '%Y年%m月%d日 %H:%M:%S'


class ProjectModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, label='项目名称', help_text='项目名称', read_only=True)
    programmer = serializers.CharField(max_length=200, label='开发人员', help_text='开发人员')
    tester = serializers.CharField(max_length=200, label='测试负责人', help_text='测试负责人', read_only=True)
    update_time = serializers.DateTimeField(label='更新时间', help_text='更新时间', format=datatime_fmt, required=False)

    # 可以通过父表获取子表的信息
    # 默认可以使用子表名模型类名小写_set
    # interfaces_set = InterfacesModelSerializer(label='拥有的接口', many=True)
    # 如果某个字段返回的结果有多条，需要添加many=True
    # interfaces_set = serializers.PrimaryKeyRelatedField(many=True)
    # 如果模型类中外键字段定义了related_name，则会使用该名称作为字段名
    # interface = serializers.StringRelatedField(many=True)
    
    # 单字段校验
    def validate_name(self, value):
        if '-' in value:
            raise serializers.ValidationError("接口名称中不能包含'-'")
        return value
    
    # 多字段校验
    def validate(self, attrs):
        if len(attrs['name']) > 10 and '测试' not in attrs['tester']:
            raise serializers.ValidationError('项目名称过长或测试人员名称不含测试')

    class Meta:
        model = Projects
        fields = '__all__'
