from fastapi import FastAPI,Body,HTTPException,BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import traceback
import json
import Config
from Redis import client as redis_client,router as redis_router
from Chat import router as chat_router
from Manage import user,message,task,files
from tortoise.contrib.fastapi import register_tortoise
from pathlib import Path

# 创建 FastAPI 应用
app=FastAPI(title="优账通API",lifespan=redis_client.lifespan, include_in_schema=False)

# 确保文件目录存在
FILE_DIR = Path(Config.FILE_DIR)
FILE_DIR.mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory=FILE_DIR), name="file")

app.include_router(redis_router)
app.include_router(chat_router)
app.include_router(user.router)
app.include_router(message.router)
app.include_router(task.router)
app.include_router(files.router)

# 配置跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


# 设置报错信息（不设置该函数，程序报错会自动终止）
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    print(f"请求信息: {request}")
    print(f"错误信息: {str(exc)}")
    return {"code": 500, "message": str(exc)}

register_tortoise(
    app,
    config=Config.TORTOISE_ORM,
    generate_schemas=True, # 自动生成数据库表
    add_exception_handlers=False,# 数据库调试信息
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
