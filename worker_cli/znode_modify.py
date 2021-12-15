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
from googleAPI import googleAPI
import kazoo.exceptions
import run

def attain_membership(zk, worker_id):
    membership_lock= zk.Lock('/members')
    while True:
        try:
            zk.create('/members/'+worker_id,ephemeral=True)
            break
        except:
            pass

def get_runfile(runFile_name,gcloud):
    gcloud.download_blob(runFile_name)

def input_execution(zk,worker,children):
    while True:
        children = zk.get_children('/inputs')
        if len(children) == 0:
            print('No inputs yet')
            return
        children = zk.get_children('/inputs')
        #get one input
        i = random.choice(children)
        input_path = "/inputs"
        process_path = "/process/"+str(i)
        #if locked wait for 5 seconds
        try:
            input_lock = zk.Lock(input_path, worker)
            input_lock.acquire(timeout=5)
            data, stat = zk.get("/inputs/"+str(i))
            process_lock = zk.Lock(process_path, worker)
            zk.create("/process/"+str(i), data)
            process_lock.acquire(timeout=5)
            zk.delete("/inputs/"+str(i))
            input_lock.release()
        #if lock is acquired move to another input
        except kazoo.exceptions.LockTimeout:
            print(str(i)+' is passed')
            children.remove(i)
            continue
        run.main(data)
        zk.ensure_path("/result/"+str(i))
        process_lock.release()
        zk.delete("/process/"+str(i))
    
