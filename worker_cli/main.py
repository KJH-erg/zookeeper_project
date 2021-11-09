
import time
import asyncio
import daemon
import os

if __name__ == "__main__":
	os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../donot/quick-replica-330115-aa2bd2f50a7c.json"
	print('worker server starts '+time.strftime('%X'))
	asyncio.run(daemon.main('localhost'))
# 10.178.0.9,10.178.0.10,10.178.0.11

# def my_listener(state):
# 	if state == KazooState.LOST:
# 		print('lost')
#         # Register somewhere that the session was lost
# 	elif state == KazooState.SUSPENDED:
# 		print('suspended')
#         # Handle being disconnected from Zookeeper
# 	else:
# 		print('okay')
#         # Handle being connected/reconnected to Zookeeper


# print('start')
# zk = zkcli('localhost:2181')
# zk.start()
# zk.create("/my/favorite/node", b"a value")
# # 
# # time.sleep(110)
# # zk.stop()

# # time.sleep(1000000)
# print('end')
