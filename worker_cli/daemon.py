# import asyncio
# import random
# import time
# from kazoo.client import KazooState
# from kazoo.client import KazooClient
# import sys
# import logics
# import socket
# from kazoo.retry import KazooRetry
# from kazoo.recipe.watchers import PatientChildrenWatch
# import time
# from googleAPI import googleAPI
# import kazoo.exceptions
# import run

# async def execute_run(zk,worker,children):
#     while True:
#         if len(children) == 0:
#             print('no inputs anymore wait for inputs')
#             watcher = PatientChildrenWatch(zk, '/inputs',
#                                time_boundary=10)
#             async_object = watcher.start()
#             children, child_async = async_object.get()
#         else:
#             #get one input
#             i = random.choice(children)
#             path = "/inputs/"+str(i)
#             #if locked wait for 5 seconds
#             try:
#                 lock = zk.Lock(path, worker)
#                 lock.acquire(timeout=5)
#                 print(lock)
#             #if lock is acquired move to another input
#             except kazoo.exceptions.LockTimeout:
#                 print(str(i)+' is passed')
#                 children.remove(i)
#                 continue
#             #after lock
#             data, stat = zk.get("/inputs/"+str(i))
#             print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
#             #async job for main_run
#             main_run_flag = asyncio.Event()
#             asyncio.create_task(run.main(main_run_flag,data))
#             await main_run_flag.wait()
            
#             #delete input 
#             lock_till_delete = asyncio.Event()
#             asyncio.create_task(logics.delete_node(lock_till_delete,zk,path,lock))
#             await lock_till_delete.wait()
#             #create result with worker_id
#             try:
#                 zk.ensure_path("/result/"+str(i))
#             except:
#                 zk.set("/result/"+str(i),worker_id.encode(encoding='utf-8'))
#             #refresh input list
#             children = zk.get_children('/inputs')
            
            
            
        
            


        


# async def main(ip):
#     '''
#     Daemon for application manager
#     '''
    
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     current_ip = s.getsockname()[0]
#     global worker_id
#     worker_id = ip_table[str(current_ip)]
#     zk = KazooClient(hosts=ip)
    
#     zk.start()
#     #znode lock for membership
#     membership_lock= zk.Lock('/members')
#     #get initial members in zkserver

    
#     zk.create('/members/'+worker_id,ephemeral=True)
    

    
    
#     @zk.DataWatch("/exec")
#     def watch_node(data, stat):
#         client = googleAPI()
#         client.download_blob(data)
#         print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    
#     while True:
#         children = zk.get_children('/inputs')
#         flag = asyncio.Event()
#         asyncio.create_task(execute_run(zk,worker_id,children))
#         await flag.wait()

    

        






