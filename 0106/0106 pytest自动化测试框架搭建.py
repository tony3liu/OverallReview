#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/1/6
# @Author  : 
# @File    : 0106 pytest自动化测试框架搭建
# 浏览器驱动Webdriver相关知识点
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

"""以下内容均为了封装浏览器驱动时进行初始化浏览器，同时在写测试框架时注意，driver的创建放在fixture中，会有比较好用的效果"""
## 实例化驱动
driver = webdriver.Chrome()
### excuteable_path:webdriver路径，如果不给chrome()传此参数，默认是chromedriver,会自动从系统的环境变量中读取
driver1 = webdriver.Chrome(excuteable_path='./')
# 但是已经不在支持excuteable_path，而变成了service参数，而这个参数只接收service中的Service()类，所以需要将参数传入Service()实例化
excuteable_path = Service('./chromedriver/path')
driver2 = webdriver.Chrome(service=excuteable_path)
### Options一个ChromeOptions实例，用于设置Chrome浏览器的选项,对浏览器进行一些初始化操作
options_example = webdriver.ChromeOptions()
"""无头操作"""
options_example.add_argument('--headless')
"""设置代理"""
options_example.add_argument('--proxy-server=http://100.100.152.37:7000')
"""关闭浏览器提示栏"""
options_example.add_argument('--disable-infobars')
"""隐藏"Chrome正在受到自动软件的控制"""
options_example.add_experimental_option('useAutomationExtension', False)
"""去掉开发者警告"""
options_example.add_experimental_option('excludeSwitches', ['enable-automation'])
"""拓展使用某插件"""
options_example.add_extension('./chrome/被测插件/path')
driver3 = webdriver.Chrome(options=options_example)

"""元素的定位"""
# 八大定位元素的方式：id/classname/tagname/link_text/text/xpath/css/name
# 复习1种较容易忽视的定位，模糊定位链接文字：partial_link_text
driver3.find_element(by=By.PARTIAL_LINK_TEXT, value='这是一个链接后面还有')
# 复习xpath
"""从任意节点定位，用 // """
"""选取当前节点，用 . """
"""选取父级节点，用 .. """
"""选取所有，用 * """
"""选取当前节点属性用 []"""
"""选择具体属性，用 @ """
"""定位对应元素的文字，用 text()"""
driver3.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]//div[@name=\'测试\'][1]/text()')
"""获取定位元素的文字，在获取的元素上执行text"""
driver3.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/div[1]/').text
"""选择指定类型标签，用 标签名 """
driver3.find_element(by=By.XPATH, value='//input[@id="content"]/div[1]/div[2]/div[1]/').text
"""高级用法，xpath函数：contains"""
doc_element = '<img scr="www.baidu.com/text/pic.img">'
xpath = '//*[contains(@src, "www.baidu.com")]'
xpath2 = '//img[contains(@src,"pic.img")]'
text_test1 = '复习自动化测试技术'
xpath3 = '//div[contains(text(), "化测试技")]'
