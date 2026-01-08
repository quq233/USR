from tinydb import TinyDB

db = TinyDB('db.json')

# 定义表
devices_table = db.table('devices')
gateways_table = db.table('gateways')
tags_table = db.table('tags')