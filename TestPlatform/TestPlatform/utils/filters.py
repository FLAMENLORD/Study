# -*- coding: UTF-8 -*-

"""
@Project ：TestPlatform 
@File    ：filters.py
@IDE     ：PyCharm 
@Author  ：flamen
@Date    ：2021/1/22 19:58 
"""


class LimitFilter:
    def filter_queryset(self, request, queryset, view):
        # 前台固定用 ?size=... 传递过滤参数
        limit = request.query_params.get('size')
        if limit:
            limit = int(limit)
            return queryset[:limit]
        return queryset