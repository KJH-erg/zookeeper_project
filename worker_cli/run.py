import asyncio
import time
async def main(flag,i):
    print('main function with '+str(i)+' is now executing')
    time.sleep(10)
    flag.set()