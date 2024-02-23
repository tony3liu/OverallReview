#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/2/21
# @Author  : 
# @File    : web
from flask import Flask,render_template

app = Flask(__name__)


# url和函数的对应关系,即：路由
@app.route('/show/info',methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
