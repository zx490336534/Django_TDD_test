# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 下午7:39
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : gunicorn_config.py.py
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = '123.56.13.233:8080'  # 绑定ip和端口号
backlog = 512  # 监听队列
chdir = '/home/zx/Django_TDD_test'  # gunicorn要切换到的目的工作目录
timeout = 30  # 超时
worker_class = 'gevent'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式

workers = multiprocessing.cpu_count() * 2 + 1  # 进程数
threads = 2  # 指定每个进程开启的线程数
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
accesslog = "/home/zx/Django_TDD_test/log/gunicorn_access.log"  # 访问日志文件
errorlog = "/home/zx/Django_TDD_test/log/gunicorn_error.log"  # 错误日志文件
