#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/1/6
# @Author  : 
# @File    : 0106_selenium基础操作
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

# executable_path
driver = webdriver.Chrome()
# 对浏览器的基础操作
# 最大化窗口
driver.maximize_window()
# 跳转指定页面
url = 'https://www.baidu.com'
driver.get(url)
# 刷新
driver.refresh()
# 前进
driver.forward()
# 后退
driver.back()
# 截图为png
driver.get_screenshot_as_png()
# 截图为文件
filename = '123'
driver.get_screenshot_as_file(filename)
# 获取当前窗口url
driver.current_url
# 获取当前窗口的源码
driver.page_source
# 当前窗口
driver.current_window_handle
# 所有窗口
driver.window_handles
# 处理弹窗
driver.switch_to.alert
# 切换框架
iframe = './'
driver.switch_to.frame(iframe)
# 切换窗口
windows = 'baidu'
driver.switch_to.window(windows)

#### selenium的元素操作
element = ['XPATH', '//*[@class=\'321\']']
# 获取元素坐标
loc = driver.find_element(*element).location
# 获取元素大小
element_size = driver.find_element(*element).size
# 获取元素范围,元素范围即元素的大小+坐标
element_range = driver.find_element(*element).rect
# 获取webdriver实例
parent_ele = driver.find_element(*element).parent
# 获取元素截图
image = driver.find_element(*element).screenshot_as_png
image2 = driver.find_element(*element).screenshot(filename)
# 获取元素的html属性
attr_ele = driver.find_element(*element).get_attribute(name='a')
# 获取元素的css属性
css_attr_ele = driver.find_element(*element).value_of_css_property('a')
# 获取元素文本
ele_text = driver.find_element(*element).text
# 点击元素
driver.find_element(*element).click()
# 清空
driver.find_element(*element).clear()
# 输入
driver.find_element(*element).send_keys('123')

#### 鼠标操作
# 鼠标移动到指定位置
action = ActionChains(driver)
action.move_to_element(driver.find_element(*element))
# 鼠标移动到指定元素的偏移位置附近（x,y）
action.move_to_element_with_offset(driver.find_element(*element), 10, 10)
# 鼠标移动到某个坐标
action.move_by_offset(10, 10)
# 鼠标左键点击
action.click(driver.find_element(element))
# 鼠标双击
action.double_click(driver.find_element(*element))
# 鼠标右击
action.context_click(driver.find_element(*element))
# 鼠标点击元素不松开然后拖动到指定位置(指定位置是元素)
element2 = ['XPATH', '//*[@class=\'1122\']/a']
action.drag_and_drop(driver.find_element(*element), driver.find_element(*element2))
# 鼠标点击元素不松开然后拖动到指定位置(指定位置是坐标)
action.drag_and_drop_by_offset(driver.find_element(*element), 10, 10)
# 点击元素不松开，之后等待10秒,之后松开
action.click_and_hold(driver.find_element(*element)).pause(10).release()

# 三种等待
### 强制等待
time.sleep(4)
### 隐式等待
driver.implicitly_wait(4)
### 显示等待元素出现,两种写法
ele = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(*element))
ele2 = WebDriverWait(driver, 10).until(lambda ele: driver.find_element(*element))

# 三种点击
### 直接click()
ele.click()
## 处理click()点击无效的情况
### 可以在元素可见后用鼠标点
action.click(ele)
### 还可以用js点击,可以绕过一些特殊问题
ele.execute_script('argument[0].click()', ele)

# 2种切换iframe
### 这是最基础的切换操作，因为ifarme有可能不能及时可用，往往失败率很高
iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)
### 为了处理，我们用excepted_condition去做切换
WebDriverWait(driver, 10).until(ec.frame_to_be_available_and_switch_to_it('iframe'))

# 从iframe切换回来
driver.switch_to.default_content()

# 处理2种弹窗
### 第一种普通弹窗，跟正常操作一样，等待弹窗出现后再定位目标元素,之后正常操作
ele = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(*element))
### 第二种是alert警告弹窗，这个就需要调用alert的方法
#### 1\直接switch过去,再去操作如获取文字，点击按钮之类的。这个的缺点是有时会还没弹出来alert就执行，容易报错
alert = driver.switch_to.alert
"""获取alert中的文字"""
get_text = alert.text
"""点击alert中的拒绝按钮"""
alert.dismiss()
"""输入文字"""
alert.send_keys('对对对')
"""点击alert中的确定按钮"""
alert.accept()
#### 2\还是用excepted_conditions的方法，就可以避免方法1的问题
alert2 = WebDriverWait(driver, 10).until(ec.alert_is_present())
get_text2 = alert2.text
alert2.dismiss()
alert2.accept()

# 窗口切换
## 1\获取所有窗口
windows = driver.window_handles
## 2\切换到最新打开的窗口
driver.switch_to.window(windows[-1])
## 3\切回第一个窗口
driver.switch_to.window(windows[0])
## 4\获取当前窗口的对象，也叫句柄
current_win = driver.current_window_handle

# 关闭浏览器
driver.quit()

# 处理滚动条
"""将滚动条滑到可见区域,ele元素与windows的顶部对齐"""
driver.execute_script('argument[0].scrollIntoView(true);', ele)
"""将滚动条滑到可见区域,ele元素与windows的底部对齐"""
driver.execute_script('arguments[0].scrollIntoView(false);', ele)
### 两种不常用的操作，移动到windows顶部或底部
"""顶部"""
driver.execute_script('window.scrollTo(document.body.scrollHeight,0)')
"""底部"""
driver.execute_script('window.scrollTo(document.body.scrollHeight)')

# 处理日期控件，有些日期控件只能点选不能输入，这样直接去点选操作非常繁琐，直接js去禁掉控件的ReadOnly
driver.execute_script('document.getElementById("控件id").readOnly = false;')
"""输入前，先清理"""
driver.find_element('id','控件id').clear()
"""再输入"""
driver.find_element('id','控件id').send_keys('2024-01-06')
"""或者用js直接输入日期，效果相同"""
driver.execute_script('document.getElementByID("控件id").value("2024-01-06")')