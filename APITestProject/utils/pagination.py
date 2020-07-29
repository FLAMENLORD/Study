from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
	# 指定默认每一页的数据条数
	page_size = 4
	# 设置前端指定页码的查询字符串
	page_query_param = 'p'
	# 设置前端每一页显示的数据条数的查询字符串key名称
	# 指定显示之后，前端才支持指定每一页的数据条数
	page_size_query_param = 's'
	max_page_size = 50
