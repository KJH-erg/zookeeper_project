from kazoo.client import KazooState
from kazoo.client import KazooClient

def create_zkcli(ip):
    zk = KazooClient(hosts=ip)
    zk.add_listener(my_listener)
    zk.start()
    #initial nodes
    createInitNodes(zk)
    return zk

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

def createInitNodes(zk):
    zk.ensure_path("/inputs")
    zk.ensure_path("/result")
    zk.ensure_path("/members")
    zk.ensure_path("/process")


def createInitLocks(zk):
    #znode lock for inputs
    
    #znode lock for processing inputs
    result_lock= zk.Lock('/process')
    #znode lock for ended inputs
    result_lock= zk.Lock('/result')
    #znode lock for membership
    membership_lock= zk.Lock('/members')
    
        
        
    
    
    
    