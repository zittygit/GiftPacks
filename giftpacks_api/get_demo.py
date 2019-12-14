#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-11-25 14:55
# @Author  : ziyezhang
from flask import Blueprint
from flask_cors import CORS
from flasgger import swag_from
from public.GiftPacks import ApiResponse, CODE
from public.logger import Logger

logger = Logger(__name__)
blue_print = Blueprint(__name__, __name__)
CORS(blue_print)
_get_func = {
    "parameters": [],
    "responses": {
        "200": {
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "integer"
                            },
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "key": {
                                            "type": "integer"
                                        },
                                        "value": {
                                            "type": "string"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}


@swag_from(_get_func)
@blue_print.route("/getFunc", methods=['GET'])
def get_func():
    """
    获取集群信息
    Author: ziyezhang
    ---
    tags:
     - 母机上架
    """

    return ApiResponse(CODE.success, dict(key=122941, value="hello world"))