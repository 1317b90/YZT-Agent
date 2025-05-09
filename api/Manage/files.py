from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import shutil

import uuid
import Config

router = APIRouter(prefix="/file", tags=["文件管理"])

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 保存文件路径
        file_path = Config.FILE_DIR+"/" +file.filename

        # 保存上传的文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": "ok", "fileName": file.filename}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")