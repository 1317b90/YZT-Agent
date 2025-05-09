from fastapi import APIRouter, HTTPException, Request,Body
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends
import aioredis
from . import client

router = APIRouter(prefix="/redis", tags=["redis"])

# 通过key获取value
@router.get("/{key}")
async def get_redis_value(key: str, redis: aioredis.Redis = Depends(client.get_redis)):
    value = await redis.get(key)
    
    if value is None:
        raise HTTPException(status_code=500, detail="Redis值为空")
    
    return {"data": value}

# 设置key-value
@router.post("/")
async def set_redis_value(key:str=Body(...),value:str=Body(...), redis: aioredis.Redis = Depends(client.get_redis)):
    try:
        await redis.set(key, value)
        return {"message": "设置Redis值成功"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"设置Redis值失败: {str(e)}"
        )

# 获取所有redis数据
@router.get("/")
async def get_redis_all(redis: aioredis.Redis = Depends(client.get_redis)):
    try:
        # 获取所有键
        keys = await redis.keys("*")
        redis_data = []

        for key in keys:
            # 获取键的类型
            key_type = await redis.type(key)

            if key_type == "string":
                value = await redis.get(key)
                redis_data.append({"key": key, "value": value})
            elif key_type == "list":
                values = await redis.lrange(key, 0, -1)
                redis_data.append({"key": key, "value": values})
            else:
                redis_data.append({"key": key, "value": "不支持的类型"})

        return {"message": "获取Redis数据成功", "data": redis_data}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取Redis数据失败: {str(e)}"
        )

# 删除redis数据
@router.delete("/{key}")
async def del_redis(key: str, redis: aioredis.Redis = Depends(client.get_redis)):
    if not key:
        raise HTTPException(status_code=400, detail="缺少键参数")

    try:
        await redis.delete(key)
        return {"message": "删除Redis数据成功"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"删除Redis数据失败: {str(e)}"
        )

# 增加队列函数（非接口）
async def add_queue(key, value):
    redis = await client.get_redis()
    await redis.lpush(key, value)


# 通过key获取value（非接口）
async def get_value_func(key):
    redis = await client.get_redis()
    return await redis.get(key)

# 设置key value
async def set_value_func(key,value):
    redis = await client.get_redis()
    await redis.set(key, value)