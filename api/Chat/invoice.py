import AI
from . import models
import json
from Manage import task
from Redis import set_value_func

# 创建开票任务
async def create_task(arguments:models.Invoice,M:models.Message):
    arguments.userid=M.userid
    arguments.serviceid=M.serviceid

    # 如果不预览发票,将发票代码置为空
    if not arguments.is_preview:
        arguments.invoice_code=""

    # 如果是群聊，则不需要预览
    if arguments.is_group:
        arguments.is_preview=False

    # 如果邮箱不为空，去除<a>
    if arguments.buy_email:
        arguments.buy_email=arguments.buy_email.replace("<a>", "").replace("</a>", "")
    task_data={
        "userid":M.userid,
        "type":"make_invoice",
        "input":arguments.model_dump()
    }

    # 创建开票任务
    await task.create_task(task_data)



