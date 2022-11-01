from datetime import datetime
from netmiko import ConnectHandler
import os.path

class GenerateLog:
    
    def __init__(self,username,password,secret):
        self.user = username
        self.password = password
        self.secret = secret
        self.i =0

    def _getLog(self,ip,cmd):
        print(f"Connecting to {ip}")

        ### Proses Connect ke Device
        device = {
            'device_type': 'cisco_ios',
            'host': '',
            'username': '',
            'password': '',
            'secret': '',
        }
        device['host'] = ip
        device['username'] = self.user
        device['password'] = self.password
        device['secret'] = self.secret
        connect_device = ConnectHandler(**device)
        connect_device.enable()

        ### Mencari Hostname
        req_hostname = connect_device.send_command('show running-config | in hostname')
        split_hostname = req_hostname.split()

        date_now   = datetime.now()
        time_stamp = date_now.strftime("%d-%m-%y_%H_%M")

        ### Define file & Path name dari hostname dan tanggal
        file_path = "GenerateLog/"
        file_name = split_hostname[1]+'-'+str(self.i)+ '-' + time_stamp
        hostname = os.path.join(file_path, file_name+".log")

        ### Proses Capture untuk setiap command yang ada di list file
        for cmd_list in cmd :
            output_command = connect_device.send_command(f"{cmd_list}")
            ##print(output_command)
            try:
                with open(hostname, 'a') as file:
                    file.write(f'''\n{cmd_list}\n{output_command}\n\n''')
            except Exception as error:
                    file.write(error)
                    pass
        print(f"log {split_hostname[1]} has been create successfully")
        self.i +=1
        
        