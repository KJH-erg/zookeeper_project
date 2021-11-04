from kazoo.client import KazooClient
from kazoo.client import KazooState

class zkcli(KazooClient):
    def __init__(self,ip):
        self.ip = ip
    def start(self):
        self.zk.start()
    def stop(self):
        self.zk.stop()
    
    

    