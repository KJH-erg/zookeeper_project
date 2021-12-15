from kazoo.client import KazooClient
from google.cloud import storage
import googleAPI as google
def restart_VM(mem,cnt):
    cnt +=1
    print('restart'+str(mem))
    client = google.googleAPI()
    client.create_instance(mem)
    #restart api for vm
def add_run_logic(path,zk,):
    print(path)
    zk.set('/exec',path.encode(encoding='utf-8'))

def add_input_logic(path,zk):
    
    client = google.googleAPI()
    client.download_blob(path)
    try:
        with open('./csv_tmp/'+path) as f:
            data = f.read()
        # data = 'apple,banana,orange,berry,whisky'
        data = data.split('\n')
        counter = 0
        input_lock = zk.Lock("/inputs")
        input_lock.acquire(timeout=100)
        for item in data:
            zk.create("/inputs/",item.encode(encoding='utf-8'),sequence=True)
        input_lock.release()
    except:
        pass
def configureMembership(mship,children):
        original_mem = len(mship.get())
        changed_mem = len(children)
        #if node is deleted execute restart logic
        if changed_mem < original_mem:
            changed = set(mship.get())-set(children)
            changed = ''.join(changed)
            # logics.restart_VM(changed)
            mship.delete(str(changed))
            print('member {mem} is lost'.format(mem = str(changed)))
            restart_VM(changed)
        #node is added add new node to members
        elif changed_mem > original_mem:
            changed = set(children)-set(mship.get())
            changed = ''.join(changed)
            mship.add(str(changed))
            print('new member is added {mem}'.format(mem = str(changed)))

def shell_input(cmd, zk):
    if cmd == "status":
        print(zk.client_state)

    elif cmd == "add":
        print('please type URI of bucket for csv input')
        path = input()
        add_input_logic(path,zk)     
    elif cmd == 'run':
        print('please type URI of bucket for run file')
        path = input()
        add_run_logic(path,zk)  
    elif cmd =='check':
        children = zk.get_children('/process')
        if len(children) == 0:
            print('no missing outputs')
        for i in children:
            try:
                data, stat = zk.get("/process/"+str(i))
                zk.create("/inputs/"+str(i), data)
                zk.delete("/process/"+str(i))
                print(str(i)+' is moved from process to input')
            except:
                print(str(i)+' is passed')
            continue
    else:
        print('invalid input')

        
