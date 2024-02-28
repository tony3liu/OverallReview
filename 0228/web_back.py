#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2024/2/28
# @Author  : 
# @File    : web_back
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

db_cfg = {
    "host": 'localhost',
    "port": 3306,
    "user": 'root',
    "passwd": 'Q1w2e3r4',
    "database": 'stu_ python',
    "charset": 'utf8'
}


def db_execute(sql, *args, **kwargs):
    with pymysql.connect(**db_cfg) as con:
        try:
            with con.cursor() as cursor:
                cursor.execute(sql, *args, **kwargs)
            con.commit()
        except Exception as e:
            con.rollback()
            print(e)


def db_query(sql, *args, **kwargs):
    with pymysql.connect(**db_cfg) as con:
        try:
            with con.cursor() as cursor:
                cursor.execute(sql, *args, **kwargs)
                res = cursor.fetchall()
                for row in res:
                    print(row)
                return res
        except Exception as e:
            print(e)


@app.route("/user/info", methods=["GET", "POST"])
def inputUserInfo():
    if request.method == "GET":
        return render_template("userinfo.html")
    else:
        username = request.form.get("userName")
        age = request.form.get("age")
        insert_sql = "insert into dj_learn(username,age) values (%s,%s);"
        db_execute(insert_sql, (username, age))
        query_sql = "select * from dj_learn order by id desc;"
        db_query(query_sql)
        return '<script>alert("提交成功")</script>'


@app.route('/user/query', methods=['GET'])
def query_user():
    query_sql = "select * from dj_learn order by id desc;"
    res = db_query(query_sql)
    return render_template("userInfo.html", data_list=res)


if __name__ == '__main__':
    app.run()
