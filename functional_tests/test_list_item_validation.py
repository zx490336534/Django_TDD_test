# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 上午9:48
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : tests.py
# 运行功能测试:python manage.py test functional_tests
from unittest import skip
from .base import FunctionslTest


class ItemValidationTest(FunctionslTest):
    def test_cannot_add_empty_list_items(self):
        self.fail('write me!')
