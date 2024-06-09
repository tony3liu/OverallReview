#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/6/9
# @Author  : 
# @File    : 属性和方法复习

class Human():

    """
    属性访问的查找顺序：
    1.__getattribute__
    2.数据描述符
    3.当前对象的所属成员
    4.类的所属成员
    5.非数据描述符
    6.父类的所属成员
    7.__getattr__
    """
    live = 100
    def __init__(self,name):
        self.name = name
        self.age = 18
    # 魔术方法
    def __getattr__(self, item):
        """
        拦截不存在属性
        :param item:
        :return:
        """
        print('Human class: __getattr__')

    def __setattr__(self, key, value):
        pass

    def __delattr__(self, item):
        pass

    def __getattribute__(self, item):
        """
        拦截已存在的属性
        :param item:
        :return:
        """
        print('Human class: __getattribute__')

    def __dir__(self):
        pass

if __name__ == '__main__':
    h1 = Human('张三')
    print(h1.name)
    print(h1.fly)
