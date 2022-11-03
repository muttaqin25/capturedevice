import device_data as device_data
import os.path
from netmiko import ConnectHandler , NetmikoTimeoutException, NetmikoAuthenticationException
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


##Perintah dibawah untuk mendefinisikan fungsi connect devie dan Capture Device
def connect_device(ip):
        ### Proses Connect ke Device
    try:
        ##Define Date
        date_now = datetime.now()
        time_stamp = date_now.strftime("%d-%m-%y_%H_%M_%S")
        ##parameter untuk Connect Device
        device = {
            'device_type': 'cisco_ios',
            'host': '',
            'username': '',
            'password': '',
            'secret': '',
        }
        device['host'] = ip
        device['username'] = device_data.username
        device['password'] = device_data.password
        device['secret'] = device_data.secret
        print(device)
        ##initiate connect to device
        connect_to_device = ConnectHandler(**device)
        connect_to_device.enable()
        ### Define hostname
        req_hostname = connect_to_device.send_command('show running-config | in hostname')
        split_hostname = req_hostname.split()
        ### Define file name dari hostname dan tanggal untuk menyimpan output
        file_path = "OutputFileCapture/"
        hostname_date = split_hostname[1] + '-' + time_stamp + '.log'
        file_name = os.path.join(file_path, hostname_date)
        ##Proses Capture Command yang dibutuhkan
        for command in device_data.list_command:
            # print(command) Optional untuk checking
            output_command = connect_to_device.send_command(f"{command}")
            print(command)
            print(output_command)
            with open(file_name, 'a') as file:
                file.write(f'''\n{command}\n{output_command}\n\n''')
    except NetmikoTimeoutException:
        print(f"Gagal mencapture Device {ip} in {time_stamp} Karena Connection Timeout ")
        with open("list_failed_capture.txt",'a') as file_list_failed_capture:
            file_list_failed_capture.write(f'''\nGagal mencapture Device {ip} in {time_stamp} Karena Connection Timeout\n''')
    except NetmikoAuthenticationException:
        print(f"Gagal mencapture Device {ip} in {time_stamp} Karena Gagal Authentikasi ")
        with open("list_failed_capture.txt",'a') as file_list_failed_capture:
            file_list_failed_capture.write(f'''\nGagal mencapture Device {ip} in {time_stamp} Karena Gagal Authentikasi\n''')

