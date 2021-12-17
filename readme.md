Zookeeper project
Objective
create distributed system using zookeeper
How does it work (User action)
1. user uploads run file to server and inputs
2. multiple worker server downloads run file and runs file with each input as a parameter
3. result data is stored in each server first and user can check the result eventually

Details of the project
1. project is implemented on google cloud for cloud service
2. 5 working servers are always in work, if there is remaining inputs
3. auto recovery incase of working server failover
4. three servers of zookeeper for server failovers

Major components 
1. user
sends inputs and run file to application manager
2. application manager
- recieves inputs and run file from user and send those aspects to zookeeper server
- check the status of each worker server and zookeeper server
- in case of worker server failover, execute recovery
3. zookeeper server
- stores run file and inputs from application manager
- orchestrate inputs and distribute them to worker servers
- check for error while handing errors
4. worker server
- execute run file and store the data

/applcation_manager
main.py
daemon for maintaining connection with zookeeper server
watches are set,too
API.py
all logics like membership and add inputs
googleAPI
all googleAPIs for GCP like download blob and restart VM
zk_cli.py
initial setups for zookeeper server
membership.py
control inner membership

/worker_cli
main.py
daemon for maintaining connection with zookeeper server
watches are set,too
googleAPI
all googleAPIs for GCP like download blob and restart VM
run.py
ayncio method to wait for the end of run.main file
run_main.py
main logic downloaded from user
znode_modify.py
all logics like get inputs move to process node
lock setting move to result node and nodes deletion





