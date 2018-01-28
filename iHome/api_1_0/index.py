# -*- coding:utf-8 -*-

from . import api

print '34567890-'
@api.route('/', methods=['GET', "POST"])
def index():
    return "index"
