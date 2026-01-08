from pydantic import BaseModel, Field
from typing import Optional, List

# 标签模型
class Tag(BaseModel):
    id: Optional[int] = None  # TinyDB 的 doc_id
    name: str

# 基础设备信息（复用字段）
class BaseNode(BaseModel):
    mac: str
    local_ipv6: str
    tag_id: int  # 存储 Tag 的 ID 而不是字符串
    alias: Optional[str] = None

class Device(BaseNode):
    pass

class Gateway(BaseNode):
    pass