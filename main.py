from zkcli import zkcli
import time
import asyncio
import callback

if __name__ == "__main__":
	print('start time of zkcli '+time.strftime('%X'))
	print('ver')
	asyncio.run(callback.callback(123))


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
