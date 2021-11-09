from kazoo.client import KazooClient
from google.cloud import storage
import googleAPI as google

def restart_VM(mem):
    print('restart'+str(mem))
    #restart api for vm

def add_input_logic(path,zk,input_barrier):
    # self.client.download_blob(path)
    client = google.googleAPI()
    try:
        # with open('./csv_tmp/'+path) as f:
        #     data = f.read()
        data = 'apple,banana,orange,berry,whisky'
        data = data.split(',')
        print(data)

        counter = 0
        
        # with input_lock:
        #     print('asd')
        input_barrier.create()
        print('enter')
        for item in data:
            zk.create("/inputs/",item.encode(encoding='utf-8'),sequence=True)
        input_barrier.remove()
    except:
        pass


def main(i,zk,input_barrier):
    if i == "status":
        print(zk.client_state)

    elif i == "add":
        print('please type URI of bucket for csv input')
        path = input()
        add_input_logic(path,zk,input_barrier)     
    else:
        print('invalid input')


        
