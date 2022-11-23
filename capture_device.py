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
        #print(device) optional jika membutuhkan list device
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

## Fungsi untuk Membaca list file isi folder Outputfile Capture dan melakukn filterisasi
def summary_inventory():
    path = "OutputFileCapture"
    list_file_in_directory = os.listdir(path)

    ## Melakukan filrer Description PID Dan SN untuk setiap file pada hasil capture
    descr_pid_sn = []

    ## Membaca isi setiap file dari folder Outputfile untuk di filter SN PID dan Descriptionnya
    for file in list_file_in_directory:
        # print(read_file(f"{path}/{data}"))
        file_read = device_data.read_file(f"{path}/{file}")
        descr_pid_sn = []
        #melakukan filter description SN dan PID pada setiap file
        keyword_descr = "DESCR"
        descr_index = 0
        keyword_pid = "PID"
        pid_index = 1
        keyword_sn = "SN"
        sn_index = 2
        for data in file_read:
            start_index_descr = data.find(keyword_descr)
            if start_index_descr != -1:
                descr_pid_sn.insert(descr_index,data[start_index_descr:].strip('DESCR: '))
                descr_index += 3
            start_index_pid = data.find(keyword_pid)
            end_index_pid = data.find(" , ")
            if start_index_pid != -1:
                descr_pid_sn.insert(pid_index, data[start_index_pid:end_index_pid].strip("PID:"))
                pid_index += 3
            start_index_sn = data.find(keyword_sn)
            if start_index_sn != -1:
                descr_pid_sn.insert(sn_index,data[start_index_sn:].strip("SN:"))
                sn_index += 3
        ## Menulis hasil perapihan description SN dan PID ke file CSV
        index = 1
        path_inventory = "OutputFileProsesInventory/summary_inventory.csv"
        with open(path_inventory, 'a') as data_inventory:
            data_inventory.write(f'''{file},Description,Produnt ID,Serial Number\n''')
        for data in descr_pid_sn:
            if index % 3 == 0:
                with open(path_inventory, 'a') as data_inventory:
                        data_inventory.write(f''',{data}\n''')
            else:
                with open(path_inventory, 'a') as data_inventory:
                        data_inventory.write(f''',{data}''')
            index+=1