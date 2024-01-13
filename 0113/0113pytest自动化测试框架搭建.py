#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/1/13
# @Author  : 
# @File    : 0113pytest自动化测试框架搭建
import csv
import logging
import os.path
import pathlib

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import Service

# 获取路径怎么写？
## 通常写法,很容易理解
current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
a = os.path.join(parent_path, '/target')
## 傻瓜写法
c_path = f"{current_path}/target"
## 高级写法
d_path = pathlib.Path(__file__).parent / 'target'

# 创建日志logger
logger = logging.getLogger(__name__)


# conftest中写fixture
@pytest.fixture(scope='module')
def init_driver():
    """初始化浏览器"""
    opt = ChromeOptions()
    opt.add_argument('--disable-infobars')
    opt.add_extension('--maximize-window')
    opt.add_experimental_option('useAutomationExtension', False)
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service, options=opt)
    driver.get('https://www.baidu.com')
    yield driver
    driver.quit()


# conftest中写fixture
@pytest.mark.usefixtures('init_driver')
@pytest.fixture(scope='module')
def init_login(init_driver):
    '''登陆'''
    ele_user_name = ['xpath', '//*[@id="TANGRAM__PSP_10__userName"]']
    ele_password = ['xpath', '//input[@classname="password"]']
    ele_submit = ['xpath', '//btn[@classname="sumit"]']
    init_driver.find_element(*ele_user_name).send_keys('13800138000')
    init_driver.find_element(*ele_password).send_keys('123456')
    init_driver.find_element(*ele_submit).click()
    yield init_driver
    init_driver.quit()


# 定义钩子，pytest框架可以用钩子函数在用例执行开始和用例执行结束前做一些事，如打日志
# 其实也可以在用例中主动去调用logging的方法打日志，或者写一个单独写fixture方法去打日志，但是pytest其实已经准备好了这样的方法
def pytest_runtest_setup(item):
    logger.info(f'开始执行测试用例:{item.nodeid}'.center(60, '-'))


def pytest_runtest_teardown(item):
    logger.info(f'执行完成：{item.nodeid}'.center(60, '-'))


# 为了让日志能够记录测试用例执行结果，需要单独写一个钩子方法，钩子函数会在框架运行中默认执行
# 一般来说copy这个方法即可，死的东西不会有什么变化
# 页面截图的方法要在钩子函数中写，尽量不要直接在用例中写，太low而且麻烦,如果每一步都要截图，在用例中写会让人累死
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    try:
        # 获取测试结果
        outcome = yield
        report = outcome.get_result()
        # 根据测试结果做一些处理
        if report.when == 'call':
            if report.passed:
                logger.info(f'{item.nodeid}用例执行成功')
            elif report.failed:
                logger.error(f'{item.nodeid}用例执行失败')
            elif report.skipped:
                logger.warning(f'{item.nodeid}用例执行跳过')
        if "init_driver" in item.fixturenames:
            # 截图
            # item.session._outcome = report
            # item.session._report = report
            # screenshot_file = f'./{item.nodeid}.png'
            # driver = item.function.__self__
            # logger.info(f"截图保存在{screenshot_file}")
            # driver.save_screenshot(screenshot_file)

            # 用下面的来驱动，driver = item.function.__self__是测试用例是基于类和实例方法时才用的
            driver = item.funcargs['init_driver']
            screenshot_file = f'./{item.nodeid}.png'
            logger.info(f"截图保存在{screenshot_file}")
            driver.save_screenshot(screenshot_file)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


# 读取csv中测试数据的方法，主要时记住csv读取的文件格式是[{a:1,b:2},{a:3,b:4}]，要迭代输出[1,2]和[3,4]
# 为什么要迭代输出，不能直接输出完整的list么，如[[1,2],[3,4]]?
# --可以，无论是yield生成可迭代对象，还是这里直接return一个大列表均可以，因为[[1,2],[3,4]]本身也是可迭代对象
# 为什么仍旧推荐用yield呢？
# --因为生成器函数在处理大型数据集时可能更加高效，因为它逐个生成数据，减少了内存的使用
def read_csv(path):
    with open(path, 'utf-8') as f:
        content_raw_list = csv.DictReader(f)
        for i in content_raw_list:
            content_list = list(i.values())
            if len(content_list) > 0:
                yield content_list


# 使用fixture,并通过读取csv进行数据驱动
@pytest.mark.usefixtures('init_driver', 'init_login')
@pytest.mark.parametrize("a，b", read_csv(d_path))
def test_case(init_driver, init_login, a, b):
    ...
