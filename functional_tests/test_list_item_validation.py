# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 上午9:48
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : tests.py
# 运行功能测试:python manage.py test functional_tests
from unittest import skip

from selenium.webdriver.common.keys import Keys

from .base import FunctionslTest


class ItemValidationTest(FunctionslTest):
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # self.wait_for(lambda: self.assertEqual(
        #     self.get_error_element().text,
        #     "你不能创建一个空待办事项"
        # ))

        self.get_item_input_box().send_keys('购买牛奶')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 购买牛奶")

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))
        # self.wait_for(lambda: self.assertEqual(
        #     self.get_error_element().text,
        #     "你不能创建一个空待办事项"
        # ))

        self.get_item_input_box().send_keys('制作奶茶')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: 购买牛奶")
        self.wait_for_row_in_list_table("2: 制作奶茶")

    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('购买长筒雨靴')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 购买长筒雨靴')

        self.get_item_input_box().send_keys('购买长筒雨靴')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has_error').text,
            "你已经添加过该项了"
        ))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('开个玩笑')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: 开个玩笑')
        self.get_item_input_box().send_keys('开个玩笑')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        self.get_item_input_box().send_keys('a')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
