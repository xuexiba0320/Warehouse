# 异步redis

import asyncio
import aioredis


async def execute(address, password):
    print('开始执行', address)
    # 网络IO操作：创建redis连接
    redis = await aioredis.create_redis(address, password=password)

    # 网络IO操作：在redis中设置哈希值car, 内部再设三个键值对：即redis={car:{key1:1,key2:2,key3:3}}
    result = await redis.hmset_dict('car', encoding='utf-8')
    # 网络IO操作：去redis中获取值
    print(result)

    redis.close()
    # 网络IO操作：关闭redis连接
    await redis.wait_close()

    print('结束', address)

asyncio.run(execute('redis://127.0.0.1:6379', 'root'))