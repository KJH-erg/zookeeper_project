import asyncio
import random
import time
from kazoo.client import KazooState
from kazoo.client import KazooClient
import sys
import logics
import socket
from kazoo.retry import KazooRetry
from kazoo.recipe.watchers import PatientChildrenWatch
import time
import kazoo.exceptions
import run
members = []
ip_table ={
    '10.178.0.3':'1',
    '10.178.0.3':'2',
    '10.178.0.3':'3',
    '10.178.0.3':'4',
    '10.178.0.3':'5',
    '172.30.1.58':'local1'
}
def my_callback(async_obj):
    print('enter')
    try:
        children = async_obj.get()
        print(children)
    except:
        print('error')
def membership(flag, input):
    if flag =='add':
        members.append(input)
    elif flag == 'delete':
        members.remove(input)
    else:
        pass
    return members



async def execute_run(zk,worker,children):
    while True:
        children = zk.get_children('/inputs')
        if len(children) == 0:
            print('no inputs anymore wait for inputs')
            watcher = PatientChildrenWatch(zk, '/inputs',
                               time_boundary=20)
            async_object = watcher.start()
            children, child_async = async_object.get()
        else:
            i = random.choice(children)
            try:
                lock = zk.Lock("/inputs/"+str(i), worker)
                lock.acquire(timeout=5)
            except kazoo.exceptions.LockTimeout:
                print(str(i)+' is passed')
                continue
            data, stat = zk.get("/inputs/"+str(i))
            print('finished'+str(i))
            print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
            flag = asyncio.Event()
            asyncio.create_task(run.main(flag,data))
            await flag.wait()
            zk.create("/result/"+str(i))
            
            async_obj = zk.delete_async("/inputs/"+str(i))
            async_obj.rawlink(my_callback)
            lock.release()
            
            
            
        
            


        


async def main(ip):
    '''
    Daemon for application manager
    '''
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    current_ip = s.getsockname()[0]
    global worker_id
    worker_id = ip_table[str(current_ip)]
    zk = KazooClient(hosts=ip)
    
    zk.start()
    #znode lock for membership
    membership_lock= zk.Lock('/members')
    #get initial members in zkserver

    
    zk.create('/members/'+worker_id,ephemeral=True)
    

    
    
    #watch for membership
    # @zk.ChildrenWatch("/members")
    # def watch_member(children):
    #     member = membership('init','NAN')
    #     changed = set(members).difference(children)
    #     #if node is deleted execute restart logic
    #     if len(changed) != 0:
    #         changed = ''.join(changed)
    #         logics.restart_VM(changed)
    #         membership('delete',str(changed))
    
        
    # @zk.ChildrenWatch("/result")
    # def watch_result(children):
    #     print("Children are now: %s" % children)
    #     logics.remove_completed_input()
    
    while True:
        children = zk.get_children('/inputs')
        flag = asyncio.Event()
        asyncio.create_task(execute_run(zk,worker_id,children))
        await flag.wait()

    

        






