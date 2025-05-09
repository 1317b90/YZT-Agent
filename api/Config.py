TORTOISE_ORM = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.mysql",    # 引擎是asyncpg
                "credentials": {
                   "host": "172.18.59.37",
                     #"host": "127.0.0.1",
                    "port": "3306",
                    "user": "olive",
                    "password": "wangrong@2024",
                    "database": "yzt",
                    "maxsize": 20,  # 最大连接数
                    # "minsize": 1, # 最小连接数
                    # 关闭池中非活动连接的秒数。通过 0 则禁用此机制。
                    # "max_inactive_connection_lifetime": 60 * 5,
                    "ssl": False
                },
            }
        },
        "apps": {                         # 后续迁移的时候调的是apps.keys（），不能写成app！
            "models": {
                "models": ['Table'],     # 是models，而不是apps.models!
                "default_connection": "default",
            }
        },
        "use_tz": False,
        "timezone":  "Asia/Shanghai",
}

REDIS_URL = "redis://8.137.105.108:6379"

# 不可以等于./file
FILE_DIR="./files"