import json
import time

import scapy
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from tinydb import TinyDB, Query

import neigh
from db import devices_table, gateways_table, tags_table
from main import IFACE
from models import Device, Gateway, Tag

app = FastAPI()
# 配置允许的源
# ["*"] 表示允许任意域名、任意端口
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # 允许的源列表
    allow_credentials=True,         # 允许携带 Cookie
    allow_methods=["*"],             # 允许的 HTTP 方法（GET, POST 等）
    allow_headers=["*"],             # 允许的 HTTP 请求头
)
# --- 逻辑核心：匹配查询 ---

@app.get("/match/{device_mac}")
def get_gateway_for_device(device_mac: str):
    # 1. 查找设备
    DeviceQ = Query()
    device_data = devices_table.get(DeviceQ.mac == device_mac)
    if not device_data:
        raise HTTPException(status_code=404, detail="Device not found")

    # 2. 根据设备的 tag_id 查找匹配的 Gateway
    GatewayQ = Query()
    # 这里假设一个 Tag 对应一个 Gateway，或者取第一个
    matched_gateway = gateways_table.get(GatewayQ.tag_id == device_data['tag_id'])

    if not matched_gateway:
        raise HTTPException(status_code=404, detail="No gateway found for this tag")

    return {
        "gateway_mac": matched_gateway['mac'],
        "gateway_ipv6": matched_gateway['local_ipv6'],
        "tag_id": matched_gateway['tag_id']
    }


# --- CRUD 示例 (以 Tag 为例) ---

@app.post("/tags/")
def create_tag(name: str):
    new_id = len(tags_table) + 1
    tag = Tag(id=new_id, name=name)
    tags_table.insert(tag.to_dict())
    return tag


@app.put("/tags/{tag_id}")
def update_tag_name(tag_id: int, new_name: str):
    TagQ = Query()
    if not tags_table.contains(TagQ.id == tag_id):
        raise HTTPException(status_code=404, detail="Tag not found")

    tags_table.update({'name': new_name}, TagQ.id == tag_id)
    return {"message": "Update success", "new_name": new_name}


# --- 设备管理 ---

@app.post("/devices/")
def add_device(device: Device):
    devices_table.insert(device.to_dict())
    return {"status": "success"}



#获取未添加的设备列表
@app.get("/lan/active_devices")
def get_active_devices():
    return {
        "mac":"1111",
        "local_ipv6": "111",
        "tag_id": 0,
        "alias": "666"
    }

'''from scapy.all import *
IFACE=conf.iface
sniffer = neigh.start_discovery_thread(IFACE)

neigh.refresh_neighbors(IFACE)'''