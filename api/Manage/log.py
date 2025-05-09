from fastapi import APIRouter, HTTPException
from typing import List, Optional
from Table import Log
from pydantic import BaseModel

router = APIRouter(prefix="/log", tags=["日志管理"])

class LogCreate(BaseModel):
    type: str
    title: str
    content: str
    state: bool = True

@router.get("/", response_model=List[dict])
async def get_logs(
    type: Optional[str] = None,
    title: Optional[str] = None,
    state: Optional[bool] = None,
    content: Optional[str] = None
):
    query = Log.all()
    
    if type:
        query = query.filter(type=type)
    if title:
        query = query.filter(title__icontains=title)
    if state is not None:
        query = query.filter(state=state)
    if content:
        query = query.filter(content__icontains=content)
    
    logs = await query
    return [dict(log) for log in logs]

# 本地使用的日志添加函数
async def add_log_func(type: str, title: str, content: str, state: bool = True) -> None:
    await Log.create(type=type, title=title, content=content, state=state)

@router.post("/")
async def add_log(log: LogCreate):
    try:
        await Log.create(
            type=log.type,
            title=log.title,
            content=log.content,
            state=log.state
        )
        return {"message": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/")
async def delete_log(id: int):
    log = await Log.get_or_none(id=id)
    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")
    
    await log.delete()
    return {"message": "ok"}