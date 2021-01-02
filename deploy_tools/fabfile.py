# -*- coding: utf-8 -*-
# @Time    : 2021/1/2 下午6:50
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : fabfile.py
import random
from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run

REPO_URL = 'https://github.com/zx490336534/Django_TDD_test.git'


def _create_directory_structure_if_necessary(site_folder):
    """
    创建目录结构
    :param site_folder:
    :return:
    run的作用:在服务器中执行指定的shell命令
    """
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    """
    使用Git拉取源码
    :param source_folder:
    :return:
    """
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f'cd {source_folder} && git reset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    """
    更新settings.py
    sed 函数的作用是在文件中替换字符串
    append 的作用是在文件末尾添加一行内容
    :param source_folder:
    :param site_name:
    :return:
    """
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    """
    更新虚拟环境
    :param source_folder:
    :return:
    """
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')
        run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    """
    更新静态文件
    :param source_folder:
    :return:
    """
    run(f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    """
    迁移数据库
    :param source_folder:
    :return:
    """
    run(f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput')


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
