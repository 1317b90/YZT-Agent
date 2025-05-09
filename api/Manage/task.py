from fastapi import APIRouter, HTTPException,Body
from typing import List, Optional
from Table import Task
from pydantic import BaseModel
import json
from datetime import datetime
from fastapi import Request
from Redis import add_queue
router = APIRouter(prefix="/task", tags=["任务管理"])

class TaskCreate(BaseModel):
    userid: str = "0"
    type: str
    input: dict

@router.post("/", response_model=dict)
async def create_task(task: TaskCreate=Body(...)):
    # 创建任务到数据库
    task_obj = await Task.create(**task)

    # 将任务ID添加到input中
    task_input = task_obj.input
    task_input["taskid"] = task_obj.id

    # 将任务添加到Redis队列
    await add_queue(task_obj.type, json.dumps(task_input))

    return {"message": "任务创建成功", "data": {"id": task_obj.id}}

@router.get("/", response_model=List[dict])
async def get_tasks(id: Optional[str] = None, state: Optional[str] = None):
    if id:
        task = await Task.get_or_none(id=id)
        if not task:
            raise HTTPException(status_code=404, detail="任务不存在")
        return [dict(task)]

    query = Task.all()
    if state:
        query = query.filter(state=state)

    tasks = await query
    return [dict(task) for task in tasks]

@router.get("/ing")
async def update_task_to_running(id: int):
    task = await Task.get_or_none(id=id)
    if not task:
        raise HTTPException(status_code=404, detail="未找到指定ID的任务")
    
    await task.update_from_dict({"state": "running"}).save()
    return {"message": "任务状态已更新为进行中"}

# 完成任务
class TaskUpdate(BaseModel):
    id: int
    succeed: bool = False
    msg: str = ""
    data: dict = {}

@router.put("/done")
async def update_task_done(task_update: TaskUpdate=Body(...)):
    task = await Task.get_or_none(id=task_update.id)
    if not task:
        raise HTTPException(status_code=404, detail="未找到指定ID的任务")
    
    state = "success" if task_update.succeed else "error"
    
    await task.update_from_dict({
        "output": task_update.data,
        "state": state,
        "message": task_update.msg
    }).save()
    
    return {"message": "任务输出已成功更新"}

@router.delete("/{id}")
async def delete_task(id: int):
    task = await Task.get_or_none(id=id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    await task.delete()
    return {"message": "删除成功"}

@router.get("/count")
async def count_tasks():
    total_count = await Task.all().count()
    waiting_count = await Task.filter(state="waiting").count()
    running_count = await Task.filter(state="running").count()
    success_count = await Task.filter(state="success").count()
    error_count = await Task.filter(state="error").count()

    return {
        "message": "任务统计数据",
        "data": {
            "all": total_count,
            "waiting": waiting_count,
            "running": running_count,
            "success": success_count,
            "error": error_count
        }
    }