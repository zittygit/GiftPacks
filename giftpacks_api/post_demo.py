#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019-11-21 17:40
# @Author  : ziyezhang

from flask import Blueprint, request
from flask_cors import CORS
from flasgger import swag_from
from public.GiftPacks import ApiResponse, CODE
from public.logger import Logger

logger = Logger(__name__)
blue_print = Blueprint(__name__, __name__)
CORS(blue_print)
_post_func = {
    "requestBody": {
        "required": "true",
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "key1": {
                            "type": "string"
                        },
                        "key2": {
                            "type": "integer",
                        }
                    }
                }
            }
        }
    },
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
                                "type": "object",
                                "properties": {
                                    "value1": {
                                        "type": "string"
                                    },
                                    "value2": {
                                        "type": "integer"
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


@swag_from(_post_func)
@blue_print.route("/postFunc", methods=['POST'])
def post_func():
    """
    添加集群信息
    Author: ziyezhang
    ---
    tags:
     - 母机上架
    """
    parameters = request.get_json()
    if parameters is None:
        return ApiResponse(CODE.failure, None, "请求参数不符合json格式")
    key1 = parameters.get("key1")
    key2 = parameters.get("key2", 0)
    if key1 and key2:
        return ApiResponse(CODE.success, dict(value1=key1, value2=key2), "操作成功")
    else:
        return ApiResponse(CODE.failure, None, "操作失败")