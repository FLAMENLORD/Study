from rest_framework.views import APIView, Response, status
from django.contrib.auth.models import User
from rest_framework.decorators import action

from .serializers import RegisterModelSerializer


class UserView(APIView):
	def post(self, request):
		serializer_obj = RegisterModelSerializer(data=request.data)
		serializer_obj.is_valid(raise_exception=True)
		serializer_obj.save()
		return Response(serializer_obj.data, status=status.HTTP_200_OK)


class UserInfoView(APIView):
	def get(self, request):
		user_info = {
				'roles': '管理员' if request.user.is_superuser else '普通用户',
				'name': request.user.username
		}
		return Response(user_info, status=status.HTTP_200_OK)


# 校验用户名是否存在，并返回校验结果
class UsernameIsExistedView(APIView):
	def get(self, request, username):
		count = User.objects.filter(username=username).count()
		data = {
			'username': username,
			'count': count
		}
		return Response(data)


# 校验邮箱是否存在，并返回校验结果
class EmailIsExistedView(APIView):
	def get(self, request, email):
		count = User.objects.filter(email=email).count()
		data = {
			'email': email,
			'count': count
		}
		return Response(data)


