# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 上午9:48
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : tests.py
# 运行功能测试:python manage.py test functional_tests
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome(executable_path="./tools/chromedriver")

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('待办事项', self.browser.title)

        # 存在h1标题「待办事项列表」
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('待办事项列表', header_text)

        # 存在一个输入框，默认值是「请输入待办事项」
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '请输入待办事项')

        # 输入一个待办事项：「购买假蝇」 后等待1秒
        inputbox.send_keys('购买假蝇')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: 购买假蝇')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('使用孔雀羽毛做假蝇')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: 购买假蝇')
        self.check_for_row_in_list_table('2: 使用孔雀羽毛做假蝇')

        self.fail('Finish the test!')
