#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/1/13
# @Author  : 
# @File    : pytest自动化测试框架0106复习默写
# 对浏览器进行封装
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Service


def ini_browser():
    service = Service('./chromedriver')
    opt =  webdriver.ChromeOptions()
    """加无头设置"""
    opt.add_argument('--headless')
    """设置代理"""
    opt.add_argument('--proxy-server=http://100.100.152.37:7000')
    """关闭浏览器提示栏"""
    opt.add_argument('--disable-infobars')
    """设置窗口全屏"""
    opt.add_extension('--maximize-window')
    """隐藏"Chrome正在受到自动软件的控制"""
    opt.add_experimental_option('useAutomationExtension',False)
    """去掉开发者警告"""
    opt.add_experimental_option('excludeSwitches',['enable-automation'])
    driver = webdriver.Chrome(service=service,options=opt)
    return driver