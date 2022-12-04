import device_data as device_data
import os.path
from netmiko import ConnectHandler , NetmikoTimeoutException, NetmikoAuthenticationException
from netmiko.ssh_autodetect import SSHDetect
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from time import sleep

##Cek Date Time
date_now = datetime.now()
time_stamp = date_now.strftime("%d-%m-%y-%H-%M-%S")

##Define tipe perangkat
tipe_perangkat = ''

##defince file path output
file_path = "OutputFileCapture"
file_path_inventory = "OutputFileProsesInventory"

#Perintah dibawah untuk mendefinisikan fungsi connect devie dan Capture Device
## Fungsi untuk auto detect device type
def tipe_device(ip):
    hasil_connect = '1_connect_device_summary' + '_' + time_stamp + '.csv'
    file_hasil_connect = os.path.join(file_path, hasil_connect)
    try:
        device = {
            'device_type': 'autodetect',
            'host': '',
            'username': '',
            'password': '',
            'secret': '',
        }
        device['host'] = ip
        device['username'] = device_data.username
        device['password'] = device_data.password
        device['secret'] = device_data.secret
        guesser = SSHDetect(**device)
        best_match = guesser.autodetect()
        print(f"Berhasi Cek Device Type {ip}")
        return best_match
        guesser.disconnect()
    except NetmikoTimeoutException:
        print(f"Gagal Cek Device Type {ip} in {time_stamp} Karena Connection Timeout Saat Cek Device Type")
        device_data.write_file(file_hasil_connect,f'''\nGagal;mencapture Device {ip} pada {time_stamp} Karena Connection Timeout Saat Cek Device Type''')
        proses_error = True
    except NetmikoAuthenticationException:
        print(f"Gagal Cek Device Type {ip} in {time_stamp} Karena Gagal Authentikasi Saat Cek Device Type")
        device_data.write_file(file_hasil_connect,f'''\nGagal;mencapture Device {ip} pada {time_stamp} Karena Gagal Authentikasi Saat Cek Device Type''')
        proses_error = True

##Fungsi untuk connect ke device
def connect_device(ip):
    proses_error = False
    try:
        tipe_perangkat = tipe_device(ip)
        sleep(0.1)
    except:
        proses_error = True
        print("Function Cek Device Type Gagal")
    if proses_error == False :
        ### Proses Connect ke Device
        try:
            #parameter untuk Connect Device
            device = {
                'device_type': tipe_perangkat,
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
            try:
                connect_to_device.enable()
            except:
                print("Secret password salah")
                proses_error = True
            ### Define hostname
            req_hostname = connect_to_device.send_command('show running-config | in hostname')
            split_hostname = req_hostname.split()
            ### Define Check Inventory
            cek_inventory = connect_to_device.send_command("show inventory")
            ## define lokasi save
            file_inventory = split_hostname[1] + '_Inventory_' + time_stamp + '.log'
            file_name_inventory = os.path.join(file_path_inventory, file_inventory)
            ##tulis inventory ke file Inventory
            device_data.write_file(file_name_inventory, f"SHOW_INVENTORY\n{split_hostname[1]}")
            device_data.write_file(file_name_inventory, cek_inventory)
            ### Define file name dari hostname dan tanggal untuk menyimpan output dari list command
            hostname_date = split_hostname[1] + '_' + time_stamp + '.log'
            file_name = os.path.join(file_path, hostname_date)
            ### Define file name summary file
            hasil_connect = '1_connect_device_summary' + '_' + time_stamp + '.csv'
            file_hasil_connect = os.path.join(file_path, hasil_connect)
            ##Proses Capture Command yang dibutuhkan
            for command in device_data.list_command:
                # print(command) Optional untuk checking
                output_command = connect_to_device.send_command(f"{command}")
                print(command)
                print(output_command)
                with open(file_name, 'a') as file:
                    file.write(f'''\n{command}\n{output_command}\n\n''')
            device_data.write_file(file_hasil_connect,f'''\nBerhasil;mencapture Device {ip} pada {time_stamp}''')
            connect_to_device.disconnect()
        except NetmikoTimeoutException:
            print(f"Gagal mencapture Device {ip} in {time_stamp} Karena Connection Timeout ")
            device_data.write_file(file_hasil_connect,f'''\nGagal;mencapture Device {ip} pada {time_stamp} Karena Connection Timeout''')
        except NetmikoAuthenticationException:
            print(f"Gagal mencapture Device {ip} in {time_stamp} Karena Gagal Authentikasi ")
            device_data.write_file(file_hasil_connect,f'''\nGagal;mencapture Device {ip} in {time_stamp} Karena Gagal Authentikasi''')

## Fungsi untuk Membaca list file isi folder Outputfile Capture dan melakukn filterisasi
def summary_inventory():
    list_file_in_directory = os.listdir(file_path_inventory)
    ## Melakukan filrer Description PID Dan SN untuk setiap file pada hasil capture
    descr_pid_sn = []
    ## Membaca isi setiap file dari folder Outputfile untuk di filter SN PID dan Descriptionnya
    for file in list_file_in_directory:
        ##Membaca file 1 per 1
        file_read = device_data.read_file(f"{file_path_inventory}/{file}")
        # print(file_read)
        ##Membuat list kosong untuk menampung inventory
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
        path_inventory = "OutputFileProsesInventory/summary_inventory"+"_"+time_stamp+".csv"
        with open(path_inventory, 'a') as data_inventory:
            data_inventory.write(f'''Hostname;Description;Product ID;Serial Number\n{file_read[1]}''')
        for data in descr_pid_sn:
            if index % 3 == 0:
                with open(path_inventory, 'a') as data_inventory:
                        data_inventory.write(f''';{data}\n''')
            else:
                with open(path_inventory, 'a') as data_inventory:
                        data_inventory.write(f''';{data}''')
            index+=1