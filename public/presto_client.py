#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-10 20:45
# @Author  : ziyezhang

from public.GiftPacks import get_config
import requests


class PrestoClient:
    """
    presto 客户端，实现分段获取数据
    """
    def __init__(self, section):
        self._host = get_config(section, 'host')
        self._port = get_config(section, 'port')
        self._schema = get_config(section, 'schema')
        self._catalog = get_config(section, 'catalog')
        self._user = get_config(section, 'user')
        self._URL_STATEMENT_PATH = '/v1/statement'
        self._URL_RESOURCE_PATH = '/v1/query'
        self._is_finished = False

    @property
    def __http_headers(self):
        header = dict()
        header['X-Presto-Catalog'] = self._catalog
        header['X-Presto-Schema'] = self._schema
        header['X-Presto-Source'] = 'GiftPacks'  # client name
        header['X-Presto-User'] = self._user
        return header

    @property
    def __get_statement_url(self):
        return "http://{host}:{port}{path}".format(
            host=self._host,
            port=self._port,
            path=self._URL_STATEMENT_PATH
        )

    @property
    def __get_resource_url(self):
        return "http://{host}:{port}{path}".format(
            host=self._host,
            port=self._port,
            path=self._URL_RESOURCE_PATH
        )

    def create_query(self, sql):
        http_response = requests.post(
            url=self.__get_statement_url,
            data=sql.encode('utf-8'),
            headers=self.__http_headers
        )
        if not http_response.ok:
            raise Exception(http_response.content)
        http_response.encoding = 'utf-8'
        response = http_response.json()
        return dict(query_id=response.get('id'), next_uri=response.get('nextUri'))

    def get_query_result(self, next_uri):
        uri = next_uri
        while not self._is_finished:
            http_response = requests.get(
                url=uri,
                headers=self.__http_headers
            )
            if http_response.status_code == 200:
                http_response.encoding = 'utf-8'
                response = http_response.json()
                uri = response.get('nextUri')
                data = response.get('data')
                columns = response.get('columns')
                if data is not None:
                    yield dict(code=0, data=data, columns=columns)
                if uri is None:
                    self._is_finished = True
                    if response.get("error") is not None:
                        yield dict(code=1, data=response.get("error").get("failureInfo").get("message"))
                    break
            elif http_response.status_code == 503:
                continue
            else:
                break

    def cancel_query(self, query_id):
        return requests.delete(self._URL_RESOURCE_PATH+"/"+query_id)

    def get_progress(self, query_id):
        return requests.get(self.__get_resource_url+"/"+query_id)

    def cancel_query(self, query_id):
        return requests.delete(self.__get_resource_url+"/"+query_id)

    def kill_query(self, query_id):
        return requests.put(self.__get_resource_url+"/"+query_id+"/killed")