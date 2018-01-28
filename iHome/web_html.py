 # _*_ coding:utf-8 _*_
from flask import Blueprint
from flask import current_app

html = Blueprint('html',__name__)


@html.route('/<re(".*"):filename>')
def get_html_file(filename):
    # 如果没有传filename，默认是首页
    print 'For Test'
    if not filename:
        filename='index.html'
    if filename != 'favicon.ico':
        filename = '/html'+filename
    return current_app.send_static_file(filename) # 系统默认使用的通过文件名去查找模板并渲染