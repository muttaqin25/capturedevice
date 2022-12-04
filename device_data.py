#Perintah dibawah untuk import list command yang mau diambil per device dari file dan list ip
import os.path

##Perintah untuk mendapatkan input user dan password
username = input("Masukan Username ?")
password = input("Masukan password ?")
secret = input("Masukan secret ?")

## Membuat fungsi untuk membaca file
def read_file(nama_file):
    with open(nama_file, "r") as file:
        list_data = file.read().split("\n")
        return list_data

def write_file(nama_file,data_write):
    with open(nama_file, 'a') as file:
        file.write(f'{data_write}\n')

## Membaca file list command
list_command = read_file("_list_command.txt")
## Membaca file list command
list_ip = read_file("_list_ip.txt")