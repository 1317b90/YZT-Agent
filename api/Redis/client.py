import aioredis
from contextlib import asynccontextmanager
from fastapi import FastAPI
import Config

redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = aioredis.from_url(Config.REDIS_URL, decode_responses=True)
    print("🔌 Redis 连接已建立")
    yield
    await redis_client.close()
    print("❌ Redis 连接已关闭")

# 依赖项：获取 Redis 连接
async def get_redis():
    return redis_client
