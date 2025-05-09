import service from "@/request/index";


// --------- 任务 --------- 任务 --------- 任务 --------- 任务 --------- 任务 --------- 任务 --------- 任务


// 从数据库获取任务
export async function getTasks(state: string) {
    if (state == "all") {
        return service({
            url: "task/",
            method: "GET",
        })
    } else {
        return service({
            url: "task/?state=" + state,
            method: "GET",
        })
    }

}

// 创建任务
export async function createTask(Type: string, Input: object) {
    return service({
        url: "task/",
        method: "POST",
        data: {
            "type": Type,
            "input": Input
        }
    })
}

// 统计任务数据
export async function countTask() {
    return service({
        url: "task/count",
        method: "GET",
    })
}

// --------- redis --------- redis --------- redis --------- redis --------- redis --------- redis --------- redis --------- redis --------- redis

// 获取所有redis数据
export async function getRedis() {
    return service({
        url: "redis/",
        method: "GET",
    })
}


// 删除redis数据
export async function delRedis(key: string) {
    return service({
        url: "redis/" + key,
        method: "DELETE",
    })
}


// --------- 用户 --------- 用户 --------- 用户 --------- 用户 --------- 用户 --------- 用户 --------- 用户 --------- 用户
// 动态查询用户
export async function getUser(params: object) {
    const queryString = Object.entries(params)
        .filter(([_, value]) => value !== undefined)
        .map(([key, value]) => `${key}=${value}`)
        .join('&');
    return service({
        url: `user/?${queryString}`,
        method: "GET",
    });
}

// 根据id查询用户
export async function getUserByUserID(userid: string) {
    return service({
        url: "user/" + userid,
        method: "GET",
    })
}

// 创建用户
export async function createUser(data: object) {
    return service({
        url: "user/",
        method: "POST",
        data: data
    })
}

// 修改用户
export async function setUser(data: object) {
    return service({
        url: "user/",
        method: "PUT",
        data: data
    })
}

// 删除用户
export async function delUser(userid: string) {
    return service({
        url: "user/" + userid,
        method: "DELETE",
    })
}



// --------- 日志 --------- 日志 --------- 日志 --------- 日志 --------- 日志 --------- 日志 --------- 日志

// 获取日志
export async function getLog(params: object) {
    return service({
        url: "log/",
        method: "GET",
        params: params
    })
}


// --------- 企业微信 --------- 企业微信 --------- 企业微信 --------- 企业微信 --------- 企业微信 --------- 企业微信 --------- 企业微信

export async function getMessages(params: {
    page?: number,
    pageSize?: number,
    serviceid?: string,
    userid?: string,
    startDate?: string,  // 开始日期
    endDate?: string     // 结束日期
}) {
    return service({
        url: "message/",
        method: "GET",
        params: params
    })
}