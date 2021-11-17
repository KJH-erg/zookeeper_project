from kazoo.client import KazooClient
from google.cloud import storage
import googleAPI as google
def my_callback(async_obj):
    print('enter')
    try:
        print(async_obj.get())
        # print('berror')
        # children = async_obj.get()
        # print(children)
        # print('after')
    except:
        print('error')
async def delete_node(flag,zk,path,lock):
    lock.release()
    async_obj = zk.delete_async(path)
    async_obj.rawlink(my_callback)
    flag.set()
