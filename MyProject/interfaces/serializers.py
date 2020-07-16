from rest_framework import serializers, validators
from .models import Interfaces

from projects.serializers import ProjectModelSerializer


def is_name_contain_x(value):
    if 'x' in value:
        raise serializers.ValidationError("接口名称中不能包含'X'")


# 使用模型序列化器类，作用：简化序列化器类中字段的创建
# 需要继承ModelSerializer
class InterfacesModelSerializer(serializers.ModelSerializer):
    # 如果在模型序列化器中显示指定了模型类中的某个字段，那么会将自动生成的字段覆盖
    name = serializers.CharField(max_length=10, label='接口名称', help_text='接口名称', validators=[
        validators.UniqueValidator(queryset=Interfaces.objects.all(), message='接口名称已存在'), is_name_contain_x])

    # projects = serializers.PrimaryKeyRelatedField(read_only=True)
    tester = serializers.CharField(label='测试人员', max_length=50, help_text='测试人员')

    # 添加了一个模型类里不存在的字段，需添加到fields中
    # email = serializers.EmailField(write_only=True, required=False)
    # 会将父表的主键id返回
    # 此处的字段名一定要与模型中的字段名一致
    # projects = serializers.PrimaryKeyRelatedField(read_only=True)
    # 将父表中对应对象的__str__方法结果返回
    # project_str = serializers.StringRelatedField()
    # 指定序列化输出时返回的父表某个字段值
    # projects = serializers.SlugRelatedField(slug_field='tester', read_only=True)
    # 可以将某个序列化器对象定义为字段，支持Field中的所有参数
    projects = ProjectModelSerializer(label='所属项目信息', help_text='所属项目信息', read_only=True)

    class Meta:
        # model类属性：在Meta内部类中指定具体的模型类
        # fields类属性 指定模型类中需要输入或输出的字段
        # 默认id主键会自动添加read_only=True
        # create_time、update_time自动添加read_only=True
        model = Interfaces
        # 将模型类的所有字段都声明到模型序列化器中
        fields = '__all__'
        # 可以将需要/输出的字段放在fields元组中，在序列化器中定义的所有字段必须添加到fields中
        # fields = ('id', 'name', 'tester', 'desc', 'email', 'projects', 'projects_info')
        # 把需要排除的字段放在exclude中，既不参与输入，也不参与输出
        # exclude = ('desc',)
        # 可以在read_only_fields中指定只输出，不输入的字段
        read_only_fields = ('id',)
        # 可以在extra_kwargs属性中定制某些字段，可以覆盖，也可以新增，序列化器中定义的字段优先级最高
        extra_kwargs = {
            'tester': {
                'label': '测试负责人',
                'write_only': False,
                'max_length': 10,
                'min_length': 1
            },
            'name': {
                'max_length': 10,
                'min_length': 2,
                'label': '接口名称',
                'help_text': '接口名称',
                'validators': [validators.UniqueValidator(queryset=Interfaces.objects.all(), message='接口名称已存在')]
            }
        }

    # def create(self, validated_data):
    #     # 场景：用户注册的密码和确认密码，产生模型类里不存在的字段
    #     # validated_data.pop('email')
    #     # return super().create(**validated_data)
    #     return Interfaces.objects.create(**validated_data)
