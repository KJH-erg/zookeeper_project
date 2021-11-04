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

Disaster planing and plan to recovery




