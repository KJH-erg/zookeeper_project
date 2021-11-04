import asyncio
import zkcli
import time
from kazoo.client import KazooState
from kazoo.client import KazooClient

def my_listener(state):
    if state == KazooState.LOST:
        print('lost')
        # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        print('suspended')
        # Handle being disconnected from Zookeeper
    else:
        print('okay')
            # Handle being connected/reconnected to Zookeeper    
async def tasks(flag,zk):
    time.sleep(10)
    zk.stop()
    flag.set()
    

async def callback(ip):
    zk = KazooClient(hosts='localhost:2181')

    zk.add_listener(my_listener)
    while True:
        zk.start()
        flag = asyncio.Event()
        print('new')
        asyncio.create_task(tasks(flag,zk))
        await flag.wait()







