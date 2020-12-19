# -*- coding: utf-8 -*-
# @Time    : 2020/12/19 上午9:48
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : functional_test.py
from selenium import webdriver

browser = webdriver.Chrome(executable_path="tools/chromedriver")
browser.get("http://localhost:8000")

assert 'Django' in browser.title
