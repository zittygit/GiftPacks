#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-11-21 18:46
# @Author  : docker_management
from public.GiftPacks import DB
from public.logger import Logger

logger = Logger(__name__)


def getTables(condition_1: int, condition_2: str) -> list:
    db = DB("mysql")
    result = db.select( "select column_1,columns_2 from table where c=%d and c2=%s" % (
            condition_1, condition_2))
    db.close()
    data = list()
    for tmp in result:
        data.append(dict(column_1=tmp[0], column_2=tmp[1]))
    return data
