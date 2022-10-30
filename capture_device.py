from netmiko import ConnectHandler
from datetime import datetime

##Perintah dibawah untuk import list IP device dari file
with open("list_ip.txt", "r") as file_list_ip:
    list_ip=file_list_ip.read().split("\n")
    print(list_ip)

##Perintah dibawah untuk import list command yang mau diambil per device dari file
with open("list_command.txt", "r") as file_list_command:
    list_command=file_list_command.read().split("\n")
    print(list_command)

##Perintah untuk mendifinisikan tanggal untuk nama file
date_now   = datetime.now()
time_stamp = date_now.strftime("%d-%m-%y_%H_%M_%S")

###Menerima input username dan password

username = input("Masukan username ? ")
password = input("Masukan Password ? ")
secrets = input("Masukan enable secret ? ")

##Perintah dibawah untuk mendefinisikan fungsi connect dan capture ke device
def connect_device(ip):
    ### Proses Connect ke Device
    device = {
        'device_type': 'cisco_ios',
        'host': '',
        'username': '',
        'password': '',
        'secret': '',
    }
    device['host'] = ip
    device['username'] = username
    device['password'] = password
    device['secret'] = secrets
    connect_device = ConnectHandler(**device)
    connect_device.enable()
    ### Mencari Hostname
    req_hostname = connect_device.send_command('show running-config | in hostname')
    split_hostname = req_hostname.split()
    ### Define file name dari hostname dan tanggal
    hostname_date = split_hostname[1] + '-' + time_stamp + '.log'
    ### Proses Capture untuk setiap command yang ada di list file
    for command in list_command:
        #print(command) Optional untuk checking
        output_command = connect_device.send_command(f"{command}")
        print(command)
        print(output_command)
        with open(hostname_date, 'a') as file:
            file.write(f'''\n{command}\n{output_command}\n\n''')

###Perintah dibawah untuk eksekusi command untuk setiap ip dalam list
for ip in list_ip:
  connect_device(ip)
