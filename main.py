from multiprocessing.dummy import Pool, Process
from device import DeviceList
from getpass import getpass
from generateLog import GenerateLog

import time

 ### Menerima input username dan password
username = input("Masukan username...?")
password = getpass("Masukan Password...?")
secrets = getpass("Masukan enable secret...?")

### Membaca list IP dan List Command dari file txt
device_ip  = DeviceList()
device_cmd = DeviceList()
device_ip_ = device_ip.read_List("list_ip_")
device_cmd_ = device_cmd.read_List("list_command_")

### inisiasi login perangkat dan command
get = GenerateLog(username,password,secrets)

def task(ipAdd,cmd):
    start_time = time.time()
    get._getLog(ipAdd,cmd)
    end_time = time.time() - start_time
    print(f"processing {ipAdd} logs, took {end_time}")
        
if __name__ == '__main__':
    # create all tasks
    processes = [Process(target=task, args=(ip,device_cmd_,)) for ip in device_ip_]
    # start all processes
    for process in processes:
        process.start()
    # wait for all processes to complete
    for process in processes:
        process.join()
    # report that all tasks are completed
    print('Done', flush=True)
