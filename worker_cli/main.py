import asyncio
import time
import sys
from kazoo.client import KazooClient
import socket
import googleAPI as google
from kazoo.recipe.watchers import PatientChildrenWatch
import time
import asyncio
import os
import znode_modify
def get_workername():
	gce_name = socket.gethostname()
	return gce_name
if __name__ == "__main__":
	ip = ['10.178.0.9','10.178.0.10','10.178.0.11']
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../donot/quick-replica-330115-aa2bd2f50a7c.json"
	gcloud = google.googleAPI()
	zk = KazooClient(hosts='localhost')

	zk.start()
    #get initial members in zkserver
	@zk.DataWatch("/exec")
	def watch_node(data, stat):
		znode_modify.get_runfile(data,gcloud)
	worker_id = get_workername()
	znode_modify.attain_membership(zk,worker_id)
	# 
    # 
	
    # print('start time of zkcli '+time.strftime('%X'))
    # zk = zk_cli.create_zkcli('localhost')
    # mship = membership(zk.get_children('/members'))
    # @zk.ChildrenWatch("/members")
    # def watch_member(children):
    #     API.configureMembership(mship,children)
	
	while True:
		watcher = PatientChildrenWatch(zk, '/inputs',time_boundary=10)
		async_object = watcher.start()
		children, child_async = async_object.get()
		znode_modify.input_execution(zk,worker_id,children)

		# client = googleAPI()
		# client.download_blob(data)
		# print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
		# cmd = input()
		# API.shell_input(cmd,zk)