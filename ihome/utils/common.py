# -*- coding:utf8 -*-
from werkzeug.routing import BaseConverter


# 自定义正则转化器
class RegxConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegxConverter, self).__init__(url_map)
        self.regex = args[0]
