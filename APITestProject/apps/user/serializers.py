from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from django.contrib.auth.models import User


class RegisterModelSerializer(serializers.ModelSerializer):
	password_confirm = serializers.CharField(label='确认密码', help_text='确认密码', min_length=6, max_length=20, write_only=True, error_messages={
		'min_length': '请输入长度为6-20个字符的确认密码',
		'max_length': '请输入长度为6-20个字符的确认密码',
	})
	token = serializers.CharField(label='token', help_text='token', read_only=True)

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'password', 'password_confirm', 'token')

		extra_kwargs = {
			'username': {
				'label': '用户名',
				'help_text': '用户名',
				'min_length': 6,
				'max_length': 20,
				'error_messages': {
					'min_length': '请输入长度为6-20个字符的用户名',
					'max_length': '请输入长度为6-20个字符的用户名',
				},
				'validators': [UniqueValidator(queryset=User.objects.all(), message="该用户已被注册")]
			},
			'email': {
				'label': '邮箱',
				'help_text': '邮箱',
				'validators': [UniqueValidator(queryset=User.objects.all(), message="该邮箱已被注册")]
			},
			'password': {
				'label': '用户密码',
				'help_text': '用户密码',
				'write_only': True,
				'min_length': 6,
				'max_length': 20,
				'error_messages': {
					'min_length': '请输入长度为6-20个字符的用户密码',
					'max_length': '请输入长度为6-20个字符的用户密码'
				}
			},
		}

	def validate(self, attrs):
		if attrs.get('password') != attrs.get('password_confirm'):
			raise serializers.ValidationError('输入密码与确认密码不一致')
		return attrs

	def create(self, validated_data):
		validated_data.pop('password_confirm')
		user = User.objects.create_user(**validated_data)
		payload = jwt_payload_handler(user)
		token = jwt_encode_handler(payload)
		user.token = token
		return user
