import asyncio
import time
import sys
import API


  

import time
import asyncio
import zk_cli
import os
from membership import membership
from kazoo.recipe.watchers import PatientChildrenWatch

if __name__ == "__main__":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../donot/quick-replica-330115-aa2bd2f50a7c.json"
    print('start time of zkcli '+time.strftime('%X'))
    zk = zk_cli.create_zkcli('localhost')
    mship = membership(zk.get_children('/members'))
    @zk.ChildrenWatch("/members")
    def watch_member(children):
        API.configureMembership(mship,children)
    @zk.ChildrenWatch("/result")
    def watchResults(children):
        print('ended are ')
        for i in children:
            print(i)
    
    while True:
        cmd = input()
        API.shell_input(cmd,zk)







