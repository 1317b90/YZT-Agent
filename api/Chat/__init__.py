from fastapi import APIRouter, HTTPException,Body,BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel
from . import admin,invoice,models
import AI
from Manage import user,message
from Redis import get_value_func,set_value_func
import json
import traceback
router = APIRouter(prefix="/chat", tags=["聊天"])


@router.post("/")
async def chat(M: models.ChatMessage = Body(...)):
    return AI.chat(M.messages,M.temperature)

@router.post("/receive")
async def receive_message(background_tasks: BackgroundTasks,M: models.Message = Body(...)):
    if "admin" in M.userid:
        new_message=M.messages[-1]["content"]
        if "指代" in new_message:
            return await admin.puppet(M.userid,new_message)

    # 获取记忆
    memory=await get_value_func("memory_"+M.userid)
    try:
        memory=json.loads(memory)
    except:
        memory={}

    # 调用AI，获取回答
    result=AI.receive(M.messages,memory=memory)
    print(result)
    M.answer=result.content
    # 调用工具
    if result.tool_calls:
        for tool_call in result.tool_calls:
            tool_content=""
            try:
                # 解析参数
                arguments=json.loads(tool_call.function.arguments)

                none_content=""
                # 如果是开票
                if tool_call.function.name=="make_invoice":
                    arguments = models.Invoice(**arguments)
                    await invoice.create_task(arguments,M)
                    # 假如AI没有生成回复，使用下面这句作为回复
                    none_content="正在执行开票中，请您稍等..."

                # 如果是取消开票
                elif tool_call.function.name=="cancel_invoice":
                    memory=await get_value_func("memory_"+M.userid)
                    tool_content="# 开票任务已经取消\n 取消的开票信息："+str(memory)+"\n# 如果有需要 请重新发起开票"
                    # 清空记忆
                    await set_value_func("memory_"+M.userid,"{}")

                # 如果AI回复漏了
                if not M.answer and not tool_content:
                    tool_content=none_content

            # 如果出错了
            except Exception as e:
                # 打印详细报错
                traceback.print_exc()
                tool_content=str(e)

            finally:
                # 如果工具有返回值
                if tool_content:
                    M.messages.append(
                        {
                            "role": "tool",
                            "content": tool_content,
                            "tool_call_id": tool_call.id
                        }
                    )
                    M.answer=AI.receive(M.messages).content

    # 将聊天记录存储到数据库中(后台执行)
    background_tasks.add_task(message.add_message,M.model_dump())
    return M.answer


@router.get("/polish")
def polish_message(message:str):
    # 将待润色结果传入
    messages=[{
                "role": "tool",
                "content": message,
                "tool_call_id": ""
                    }]
    return {"message":AI.polish(messages)}

@router.post("/group")
async def group_message(M: models.GroupMessage = Body(...)):
    try:
        # 补充习惯
        try:
            user_data=await user.get_user_by_id(M.userid)
            if "admin" in M.userid:
                userid=user_data.puppet_id
                user_data=await user.get_user_by_id(userid)

            M.message+=user_data.invoice_habit
        except Exception as e:
            print(f"习惯出错：{e}")

        result=AI.group(M.message)
        # 调用工具
        if result.tool_calls:
            for tool_call in result.tool_calls:
                none_content=""
                # 解析参数
                arguments=json.loads(tool_call.function.arguments)

                must_dict={
                    "buy_name": "发票抬头",
                    "invoice_type": "发票类型",
                    "invoice_name": "发票名称",
                    "invoice_amount": "发票金额"
                }

                # 检查必填项
                for key in must_dict.keys():
                    if arguments.get(key,"")=="":
                        none_content+=must_dict[key]+"，"

                if none_content:
                    return f"请将{none_content}补充完整"

                arguments = models.Invoice(**arguments)
                # 是群聊消息
                arguments.is_group=True
                arguments.adminid=M.adminid
                print(arguments)
                await invoice.create_task(arguments,M)

        return ""
    except Exception as e:
        # 打印详细报错
        traceback.print_exc()
        raise Exception(f"{str(e)}\n{str(M.model_dump())}")





# 一键提醒
@router.get("/remind")
async def remind():
    users=await user.get_users()
    for user in users:
        message.send_message("yzt_serviceid",user.get("UserID",""),"您好，麻烦导出上个月的银行回单和银行对账单，入账需要，谢谢配合")