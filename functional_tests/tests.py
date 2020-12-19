# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 上午9:48
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : tests.py
# 运行功能测试:python manage.py test functional_tests
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    CHROME_DRIVER = "./tools/chromedriver"

    def setUp(self) -> None:
        self.browser = webdriver.Chrome(executable_path=self.CHROME_DRIVER)

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        t0 = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - t0 > MAX_WAIT:
                    raise e
                time.sleep(0.1)

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn('待办事项', self.browser.title)

        # 存在h1标题「待办事项列表」
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('待办事项列表', header_text)

        # 存在一个输入框，默认值是「请输入待办事项」
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '请输入待办事项')

        # 输入一个待办事项：「购买羽毛」 后等待1秒
        inputbox.send_keys('购买羽毛')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: 购买羽毛')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('使用孔雀羽毛做一只鸟')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.wait_for_row_in_list_table('1: 购买羽毛')
        self.wait_for_row_in_list_table('2: 使用孔雀羽毛做一只鸟')

        self.fail('Finish the test!')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('购买羽毛')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 购买羽毛')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        self.browser.quit()

        self.browser = webdriver.Chrome(executable_path=self.CHROME_DRIVER)
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买羽毛', page_text)
        self.assertNotIn('做一只鸟', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('购买牛奶')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 购买牛奶')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('购买羽毛', page_text)
        self.assertIn('购买牛奶', page_text)
