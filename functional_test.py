# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 上午9:48
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : functional_test.py
import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome(executable_path="tools/chromedriver")

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get("http://localhost:8000")

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
