import asyncio
import zkcli
import time
from kazoo.client import KazooState
from kazoo.client import KazooClient
import sys
import logics
members = []
def membership(flag, input):
    if flag =='add':
        members.append(input)
    elif flag == 'delete':
        members.remove(input)
    else:
        pass
    return members

def my_listener(state):
    if state == KazooState.LOST:
        print('session is lost')
        # Register somewhere that the session was lost
    elif state == KazooState.SUSPENDED:
        print('session is suspended')
        # Handle being disconnected from Zookeeper
    else:
        print('session is connected to zk server')
            # Handle being connected/reconnected to Zookeeper    
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
    zk = KazooClient(hosts='localhost:2181')
    zk.add_listener(my_listener)
    zk.start()
    #znode lock for inputs
    input_lock = zk.Lock("/inputs")
    #znode lock for ended inputs
    result_lock= zk.Lock('/result')
    #znode lock for membership
    membership_lock= zk.Lock('/members')
    
    #get initial members in zkserver
    for member in zk.get_children('/members'):
        membership('add',member)
    
    #watch for membership
    @zk.ChildrenWatch("/members")
    def watch_member(children):
        member = membership('init','NAN')
        changed = set(members).difference(children)
        #if node is deleted execute restart logic
        if len(changed) != 0:
            changed = ''.join(changed)
            logics.restart_VM(changed)
            membership('delete',str(changed))
    
        
    # @zk.ChildrenWatch("/result")
    # def watch_result(children):
    #     print("Children are now: %s" % children)
    #     logics.remove_completed_input()
    
    while True:
        flag = asyncio.Event()
        asyncio.create_task(shell_input(flag,zk,input_lock))
        await flag.wait()







