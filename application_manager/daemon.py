import asyncio
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
    zk = KazooClient(hosts=ip)
    zk.add_listener(my_listener)
    zk.start()
    #initial nodes
    zk.ensure_path("/inputs")
    zk.ensure_path("/result")
    zk.ensure_path("/members")
    #znode lock for inputs
    input_barrier = zk.Barrier("/inputs/")
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
        original_mem = len(member)
        
        changed_mem = len(children)
        #if node is deleted execute restart logic
        if changed_mem < original_mem:
            changed = set(members).difference(children)
            changed = ''.join(changed)
            logics.restart_VM(changed)
            membership('delete',str(changed))
        #node is added add new node to members
        elif changed_mem > original_mem:
            changed = set(children).difference(members)
            membership('add',str(changed))
            print('new member is added {mem}'.format(mem = str(changed)))

        
    # @zk.ChildrenWatch("/result")
    # def watch_result(children):
    #     print("Children are now: %s" % children)
    #     logics.remove_completed_input()
    
    while True:
        flag = asyncio.Event()
        asyncio.create_task(shell_input(flag,zk,input_barrier))
        await flag.wait()







