from fastapi import APIRouter, HTTPException, Request,Depends,Body
from typing import List, Optional
from pydantic import BaseModel
from Table import Message
from datetime import datetime
from Redis import add_queue
import aioredis
from tortoise.contrib.pydantic import pydantic_model_creator
import json


router = APIRouter(prefix="/message", tags=["消息管理"] )
# 使用Pydantic模型创建消息输入验证
Message_Pydantic_Input = pydantic_model_creator(Message, name="Message_Pydantic", exclude_readonly=True)

# 获取消息列表
@router.get("/")
async def get_messages(
    request: Request,
    page: int = 1,
    pageSize: int = 10,
    serviceid: str = None,
    userid: str = None,
    startDate: str = None,
    endDate: str = None
):
    query = Message.all()
    
    if serviceid:
        query = query.filter(serviceid=serviceid)
    if userid:
        query = query.filter(userid=userid)
    if startDate:
        query = query.filter(created_at__gte=startDate)
    if endDate:
        query = query.filter(created_at__lte=endDate)
    
    total = await query.count()
    messages = await query.offset((page - 1) * pageSize).limit(pageSize).order_by('-created_at')
    
    return {"data": messages, "total": total}

# 获取用户最近的几条消息
@router.get("/new/{userid}")
async def get_user_new_message(userid: str):
    message = await Message.filter(userid=userid).order_by('-created_at').first()
    if not message:
        raise HTTPException(status_code=404, detail="未找到消息记录")
    answer = {"role": "assistant", "content": message.answer}
    message.messages.append(answer)
    return {"data": message.messages}

# 创建消息
@router.post("/", response_model=dict)
async def add_message(message: Message_Pydantic_Input=Body(...)):
    try:
        # 使用字典创建消息
        await Message.create(**message)
        return {"message": "消息添加成功", "status": "success"}
    except Exception as e:
        # 添加更详细的错误日志
        raise HTTPException(
            status_code=500,
            detail={
                "message": "添加消息失败",
                "error": str(e)
            }
        )

@router.get("/{id}")
async def get_message(id: int):
    message = await Message.get_or_none(id=id)
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    return {"data": message}

@router.delete("/{id}")
async def del_message(id: int):
    message = await Message.get_or_none(id=id)
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    
    await message.delete()
    return {"message": "消息删除成功"}

class MessageCreate(BaseModel):
    serviceid: str
    userid: str
    type: str
    content: str

# 发送消息
@router.post("/send")
async def send_message(M: MessageCreate=Body(...)):
    try:
        message_str = json.dumps(M.model_dump(),ensure_ascii=False)

        await add_queue(M.serviceid, message_str)
        return {"message": "消息发送成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发送消息失败: {str(e)}")