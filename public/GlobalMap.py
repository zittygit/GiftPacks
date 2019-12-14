# -*- coding: utf-8 -*-


def init():
    global _global_map
    _global_map = dict()

def set(k,v):
    _global_map[k] = v

def get(k):
    return _global_map.get(k)

def delete(k):
    del _global_map[k]