from pydantic import BaseModel, Field
from typing import Optional, List

# 标签模型
class Tag(BaseModel):
    tag_id: Optional[int] = None
    alias: str

# 基础设备信息（复用字段）
class BaseNode(BaseModel):
    mac: str
    tag_id: int  # 存储 Tag 的 ID 而不是字符串
    alias: Optional[str] = None

class Device(BaseNode):
    pass

class Gateway(BaseNode):
    local_ipv6: str