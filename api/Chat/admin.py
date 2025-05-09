from Manage import user

# 指代用户
async def puppet(userid:str,message:str):
    puppet_id=''.join(filter(str.isdigit, message))
    user_data=await user.get_user_by_id(puppet_id)
    if user_data:
        await user.set_puppet(userid,puppet_id)
        return f"""指代成功
🚹 {user_data.company_name}
🆔 {puppet_id}"""

    else:
        return "指代用户不存在"






