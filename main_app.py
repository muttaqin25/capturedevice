import device_data as device_data
import capture_device as capture_device
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import threading

##Define proses capture device secara pararel
processes_connect = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for ip in device_data.list_ip:
        processes_connect.append(executor.submit(capture_device.connect_device,ip))
        print(f"Connecting to {ip}")
        sleep(0.1)
##Melakukan summary dari log inventory di folder OutputFileProsesInventory
capture_device.summary_inventory()