import asyncio
import time
from kazoo.client import KazooState
from kazoo.client import KazooClient
import sys
import logics
import socket
members = []
ip_table ={
    '10.178.0.3':'1',
    '10.178.0.3':'2',
    '10.178.0.3':'3',
    '10.178.0.3':'4',
    '10.178.0.3':'5',
    '172.30.1.58':'local'
}
def membership(flag, input):
    if flag =='add':
        members.append(input)
    elif flag == 'delete':
        members.remove(input)
    else:
        pass
    return members

  
async def shell_input(flag,zk,input_lock):
    
    while True:
        var =input()
        if var:
            logics.main(var,zk,input_lock)
            break
    flag.set()


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

    membership_lock.acquire(timeout=100000)
    zk.create('/members/'+worker_id,ephemeral=True)
    membership_lock.release()

    @zk.ChildrenWatch("/inputs/")
    def input_watch(children):
        print(children)
    
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
        flag = asyncio.Event()
        asyncio.create_task(shell_input(flag,zk,membership_lock))
        await flag.wait()






