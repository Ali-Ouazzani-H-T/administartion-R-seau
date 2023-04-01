import os
import psutil
import subprocess

def get_remote_mac_address(ip_address):
    try:
        response = os.system("ping -n 1 " + ip_address)
        if response == 0:
            output = subprocess.check_output(["arp", "-a", ip_address])
            output = output.decode("utf-8")
            lines = output.split("\n")
            for line in lines:
                if ip_address in line:
                    mac_address = line.split()[1]
                    return mac_address
        else:
            return None
    except:
        return None

def get_remote_ram_status(ip_address):
    try:
        response = os.system("ping -n 1 " + ip_address)
        if response == 0:
            memory = psutil.virtual_memory()
            total_memory = round(memory.total/(1024*1024*1024), 2)
            used_memory = round(memory.used/(1024*1024*1024), 2)
            ram_status = f"{used_memory} Go / {total_memory} Go"
            return ram_status
        else:
            return None
    except:
        return None

def get_remote_cpu_temp(ip_address):
    try:
        response = os.system("ping -n 1 " + ip_address)
        if response == 0:
            output = subprocess.check_output(["ssh", ip_address, "vcgencmd", "measure_temp"])
            output = output.decode("utf-8")
            temp = output.split("=")[1].strip()[:-2]
            return temp
        else:
            return None
    except:
        return None

ip_address = "192.168.182.136"
mac_address = get_remote_mac_address(ip_address)
ram_status = get_remote_ram_status(ip_address)
temp = get_remote_cpu_temp(ip_address)

if mac_address:
    print("Adresse MAC:", mac_address)
else:
    print("Impossible de récupérer l'adresse MAC de l'ordinateur distant.")

if ram_status:
    print("Etat de la RAM:", ram_status)
else:
    print("Impossible de récupérer l'état de la RAM de l'ordinateur distant.")

if temp:
    print("Température du processeur:", temp)
else:
    print("Impossible de récupérer la température du processeur de l'ordinateur distant.")

    
from jinja2 import Template

with open('index.html') as file:
    template = Template(file.read())


html = template.render(mac_address=mac_address, ram_status=ram_status, temp=temp)

with open('index.html', 'w') as file:
    file.write(html)
