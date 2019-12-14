#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    GiftPacks Flask Framework
    ~~~~~
    flask 框架模块化
    GiftPacks  : 工程目录
      - api_*  : api目录
      - public : 公共目录
      - app.py : application 文件，启动时自动注册api_*目录中的文件

    规范：1.不同业务创建对应的"api_业务"名目录。
          2.一个API对应一个文件名。
          3.API的tags对应业务。
          4.请尽量多一点注释。

    目标：使开发和维护过程中能有愉悦的心情。


    @Author: ziyezhang
    @date: 2019-08-28
"""
from flask import Flask
from flasgger import Swagger
from public.GiftPacks import FlaskConfig
from public.GiftPacks import load_module
from public.GiftPacks import job_scheduler


app = Flask(__name__)
load_module(app)
job_scheduler.start()
app.config['SWAGGER'] = FlaskConfig.swaggerConf
Swagger(app)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

