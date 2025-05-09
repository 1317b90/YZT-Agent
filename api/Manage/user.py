from fastapi import APIRouter, HTTPException,Body,Query
from typing import List, Optional
from Table import User
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

router = APIRouter(prefix="/user", tags=["用户管理"])

User_Pydantic = pydantic_model_creator(User, name="UserSchema")
User_Pydantic_Input = pydantic_model_creator(User, name="UserInputSchema", exclude_readonly=True)


@router.get("/", response_model=dict)
async def get_users(
    page: int = Query(1, description="页码", gt=0),
    page_size: int = Query(10, description="每页数量", gt=0),
    userid: str = Query(None, description="用户ID"),
    is_admin: str = Query(None, description="是否管理员"),
    company_name: str = Query(None, description="公司名称"),
    uscid: str = Query(None, description="统一社会信用代码"),
    dsj_username: str= Query(None, description="第三方用户名"),
    dsj_password: str = Query(None, description="第三方密码"),
    bank_name: str = Query(None, description="银行名称"),
    bank_id: str = Query(None, description="银行账号"),
    enable: str = Query(None, description="是否启用"),
    is_zero:str= Query(None, description="是否零申报"),
    is_bill: str= Query(None, description="是否开票")
):
    # 初始化查询
    query = User.all()

    # 根据传入的参数动态构建查询条件
    if userid:
        query = query.filter(userid=userid)
    if is_admin is not None:
        query = query.filter(is_admin=is_admin)
    if company_name:
        query = query.filter(company_name__icontains=company_name)
    if uscid:
        query = query.filter(uscid=uscid)
    if dsj_username:
        query = query.filter(dsj_username=dsj_username)
    if dsj_password:
        query = query.filter(dsj_password=dsj_password)
    if bank_name:
        query = query.filter(bank_name=bank_name)
    if bank_id:
        query = query.filter(bank_id=bank_id)
    if enable is not None:
        query = query.filter(enable=enable)
    if is_zero is not None:
        query = query.filter(is_zero=is_zero)
    if is_bill is not None:
        query = query.filter(is_bill=is_bill)
    
    # 计算总记录数
    total = await query.count()
    
    # 计算分页偏移量
    offset = (page - 1) * page_size
    
    # 执行分页查询
    users = await User_Pydantic.from_queryset(query.offset(offset).limit(page_size))
    
    # 构造分页响应数据
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": users
    }

@router.get("/{userid}", response_model=User_Pydantic)
async def get_user_by_id(userid: str):
    user = await User.get_or_none(userid=userid)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.post("/")
async def create_user(user: User_Pydantic=Body(...)):
    # 检查用户ID是否已存在
    existing_user = await User.get_or_none(userid=user.userid)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户ID已存在")
    
    # 创建新用户
    user_obj = await User.create(**user.dict(exclude_unset=True))
    
    # 返回创建的用户信息
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.put("/")
async def set_user(user: User_Pydantic=Body(...)):
    print(type(user))
    # if isinstance(user, dict):
    #     user = User_Pydantic(**user)
    # 检查用户是否存在
    existing_user = await User.get_or_none(userid=user.userid)
    if not existing_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户信息
    await existing_user.update_from_dict(user.dict(exclude_unset=True))
    await existing_user.save()
    
    # 返回更新后的用户信息
    return await User_Pydantic.from_tortoise_orm(existing_user)

# 修改用户的puppet_id
async def set_puppet(userid,puppet_id):
    # 检查用户是否存在
    existing_user = await User.get_or_none(userid=userid)
    if not existing_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 更新用户信息
    await existing_user.update_from_dict({"puppet_id":puppet_id})
    await existing_user.save()
    
@router.delete("/{userid}")
async def delete_user(userid: str):
    user = await User.get_or_none(userid=userid)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    await user.delete()
    return {"message": "用户删除成功"}