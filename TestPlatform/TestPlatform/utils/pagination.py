from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination


class MyPagination(PageNumberPagination):
	page_size = 10
	page_query_param = 'page'
	page_size_query_param = 'size'
	max_page_size = 50
	page_query_description = '第几页'
	page_size_query_description = '每页几条'

	# default_limit = 10
	# limit_query_param = 'limit'
	# offset_query_param = 'offset'
	# max_limit = 50


	# def get_paginated_response(self, data):
	# 	response = super().get_paginated_response(data)
	# 	response.data['current_page'] = self.page.number
	# 	response.data['total_pages'] = self.page.paginator.num_pages
	# 	return response
