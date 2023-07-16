#!/usr/bin/python3
import json
from colorama import Fore
import re
from create import tabsize
success=False
def connect_to_reg(Top_level_file,reg_name,instance_name,port_name,Baseboard_path):
    json_file=Top_level_file.replace(".sv",".json")
    with open(f'{Baseboard_path}/{json_file}', 'r') as f:
        data = json.load(f)
        if reg_name in data['reg']:
           if  port_name in data[instance_name]['ports']:
               with open (f'{Top_level_file}','r') as f:
                    content=f.readlines()
                    index1=False;index2=False
                    for string in content:
                       if instance_name in string:
                            index2=index1=content.index(string)
                            for string in content[index1+1:]:
                                index2+=1
                                if f'.{port_name}' in string:
                                    if content[index2+1].startswith("."):
                                        content.pop(index2)
                                        content.insert(index2,f".{port_name}".ljust(tabsize)+f"({reg_name}),\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {reg_name}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)
                                    else:
                                        content.pop(index2)
                                        content.insert(index2,f".{port_name}".ljust(tabsize)+f"({reg_name})\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {reg_name}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)
           else:
               print(Fore.RED,f"{port_name} is not present in {instance_name}, please check the name"+Fore.RESET)
               exit()   
        else:
            print(Fore.RED,f"{reg_name} is not present in {Top_level_file}, please check the name"+Fore.RESET)
            exit()

def connect_to_wire(Top_level_file,wire_name,instance_name,port_name,Baseboard_path):
    json_file=Top_level_file.replace(".sv",".json")
    with open(f'{Baseboard_path}/{json_file}', 'r') as f:
        data = json.load(f)
        if wire_name in data['wire']:
            if  port_name in data[instance_name]['ports']:
               with open (f'{Top_level_file}','r') as f:
                    content=f.readlines()
                    index1=False;index2=False
                    for string in content:
                       if instance_name in string:
                            index2=index1=content.index(string)
                            for string in content[index1+1:]:
                                index2+=1
                                if f'.{port_name}' in string:
                                    if content[index2+1].startswith("."):
                                        content.pop(index2)
                                        content.insert(index2,f".{port_name}".ljust(tabsize)+f"({wire_name}),\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {wire_name}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)
                                    else:
                                        content.pop(index2)
                                        content.insert(index2,f".{port_name}".ljust(tabsize)+f"({wire_name})\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {wire_name}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)
            else:
                print(Fore.RED,f"{port_name} is not present in {instance_name}, please check the name"+Fore.RESET)
                exit()   
        else:
            print(Fore.RED,f"{wire_name} is not present in {Top_level_file}, please check the name"+Fore.RESET) 
            exit()    

def check_range_equality(found,Top_level_file,inst, input_port, output_port,data):
    try:
        for  input_port, output_port in zip(input_port, output_port):
            range1 = data[inst]['ports'][input_port]['range']
            range2 = data['ports'][output_port]['range']
            if range1 == range2:
                found = True
            else:
                print(
                    Fore.RED + f'Error: Range of {input_port} is {range1} and range of {output_port} is {range2} which is not equal!!' + Fore.RESET)
                exit()
        return found
    except KeyError:
        for  input_port, output_port in zip(input_port, output_port):
            if inst not in data:
                print(
                    Fore.RED + f'Error: Instance {inst} not found' + Fore.RESET)
            elif input_port not in data[inst]['ports']:
                print(
                    Fore.RED + f'Error: Port {input_port} not found of instance {inst}' + Fore.RESET)
            elif output_port not in data['ports']:
                print(
                    Fore.RED + f'Error: I/O Port {output_port} not found in {Top_level_file} ' + Fore.RESET)
            found = False
        return found

def connect_to_IO(found,Top_level_file, instance1, input_ports, output_ports):
    with open(f"{Top_level_file}", 'r') as f:
        content = f.read()
    pattern = rf'{instance1}\s*(([\s\S]*?));'
    match = re.search(pattern, content)
    if found and match:
        block = match.group()
        for input_port, output_port in zip(input_ports, output_ports):
            pattern = rf'\.{input_port}\s*\((?P<connected_port>.*)\)'
            existing_connections = re.findall(pattern, block)
            for connected_port in existing_connections:
                pattern = rf'\.{input_port}\s*\([\s\S]*?\)' 
                if connected_port:
                    connected_ports_list = [port.strip() for port in connected_port.strip('(){}').split(',')]
                    if output_port in connected_ports_list:
                        print(Fore.RED + f"Error: {output_port} already connected to {input_port}" + Fore.RESET)
                        exit()
                    else:
                        connected_ports_list.append(output_port)
                    connected_ports_str = '{{{}}}'.format(', '.join(connected_ports_list))
                    block = re.sub(pattern, fr'.{input_port}'.ljust(tabsize)+f'({connected_ports_str})', block)
                else:
                    block = re.sub(pattern, f'.{input_port}'.ljust(tabsize)+f'({output_port})', block)       
            pattern = rf'{instance1}\s*(([\s\S]*?));'
            content = re.sub(pattern, block, content)
            print(Fore.LIGHTGREEN_EX + f'Ports Connected to IO ' + Fore.RESET)
        
    # Write the modified content back to the file
    with open(f'{Top_level_file}', 'w') as f:
        f.write(content)  
        
def connect_param(Top_level_file,param,instance,ports,Baseboard_path,data):
        if param in data['parameter']: # check if parameter is in json file
            if  ports in data[instance]['ports']:
                with open(f"{Top_level_file}", 'r') as f:
                    content = f.readlines()
                    index1=False;index2=False
                    for string in content:
                       if instance in string:
                            index2=index1=content.index(string)
                            for string in content[index1+1:]:
                                index2+=1
                                if f'.{ports}' in string:
                                    if content[index2+1].startswith("."):
                                        content.pop(index2)
                                        content.insert(index2,f".{ports}".ljust(tabsize)+f"({param}),\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {param}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)
                                    else:
                                        content.pop(index2)
                                        content.insert(index2,f".{ports}".ljust(tabsize)+f"({param})\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {param}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)          
            else:
                print(Fore.RED + f'Error: Port {ports} not found in instance {instance}' + Fore.RESET)
                exit()
        else:           
            print(Fore.RED + f'Error: Parameter {param} not found' + Fore.RESET)
            choice=input("Do you want to create a new parameter? (y/n) : ")
            if choice =='y' or choice=='Y':
                val=input("Enter the value: ")
                from addparam import adding_parameters
                from addparam import parameter_json
                adding_parameters(Top_level_file,param,val)
                parameter_json(Top_level_file,param,val,Baseboard_path)
                instance=str(instance)
                if data[instance]['ports'][ports]:
                        with open(f"{Top_level_file}", 'r') as f:
                            content = f.readlines()
                        index1=False;index2=False
                        for string in content:
                            if instance in string:
                                    index1=content.index(string)
                                    for string in content[index1+1:]:
                                        if f'.{ports}' in string:
                                            index2=content.index(string)
                            if index1 < index2:
                                    break
                            if index2>index1:
                                if content[index2+1].startswith("."):
                                    content.pop(index2)
                                    content.insert(index2,f".{ports}".ljust(tabsize)+f"({param}),\n")
                                    print(Fore.LIGHTGREEN_EX + 'Port Connected to' + Fore.RESET)
                                    with open (f'{Top_level_file}','w') as f:
                                        f.writelines(content)
                                else:
                                    content.pop(index2)
                                    content.insert(index2,f".{ports}".ljust(tabsize)+f"({param})\n")
                                    print(Fore.LIGHTGREEN_EX + 'Port Connected to reg' + Fore.RESET)
                                    with open (f'{Top_level_file}','w') as f:
                                        f.writelines(content)
            else:
                print(Fore.RED,"Aborting...",Fore.RESET)
                exit() 

def connect_instances(fille_name,instance1,input_port,instance2,output_ports,Baseboard_path):
    json_file=fille_name.replace(".sv",'.json')
    with open(f"{Baseboard_path}/{json_file}") as j:
        data=json.load(j)
        
        if instance1 in data:
            if input_port in data[instance1]['ports']:

                if output_ports in data[instance2]['ports']:
                    with open (fille_name) as file:
                        content=file.readlines()

                    index1=False;index2=False
                    for string in content:
                       if instance1 in string:
                            index1=content.index(string)
                            for string in content[index1+1:]:
                                if f'.{input_port}' in string:
                                    index2=content.index(string)
                       if index1 < index2:
                            break
                    if index2>index1:
                        if content[index2+1].startswith("."):
                            content.pop(index2)
                            content.insert(index2,f".{input_port}".ljust(tabsize)+f" ({output_ports}),\n")
                            with open (f'{fille_name}','w') as f:
                                f.writelines(content)
                                print(Fore.LIGHTGREEN_EX + 'Port Connected to' + Fore.RESET)
                        else:
                            content.pop(index2)
                            content.insert(index2,f".{input_port}".ljust(tabsize)+f" ({output_ports}),\n")
                            with open (f'{fille_name}','w') as f:
                                f.writelines(content)
                                print(Fore.LIGHTGREEN_EX + 'Port Connected to reg' + Fore.RESET)    
            else:
                print( Fore.RED,f"{input_port} is not present in {instance1}!",Fore.RESET)
                exit()
        else:
            print(Fore.RED,f"{instance1} is not present in {fille_name} ",Fore.RESET) 
            exit()
def check_json(file_name,local_param,instance,port,Baseboard_path):
    global success
    json_file=file_name.replace(".sv",'.json')
    with open(f"{Baseboard_path}/{json_file}") as j:
        data=json.load(j)
        try:
            if port in data[instance]['ports']:
                if local_param in data["parameter"]:
                    success = True
                    return success
                else:
                    print(Fore.RED,f"{local_param} is not present in {file_name}!",Fore.RESET)
                    exit()
            else:
                print(Fore.RED,f"{port} is not present in {instance}!",Fore.RESET)
                exit()
        except:
            print(Fore.RED,f"{instance} is not present in {file_name}!",Fore.RESET)
            exit()

def connect_localparam(file_name,local_param,instance,port):
    global success
    if success:
        try:
            with open (file_name) as file:
                content=file.readlines()
                index1=False;index2=False
                for string in content:
                    if instance in string:
                        index1=content.index(string)
                        for string in content[index1+1:]:
                            if f'.{port}' in string:
                                index2=content.index(string)
                            if index1 < index2:
                                break
                if index2>index1:
                    if content[index2+1].startswith("."):
                        content.pop(index2)
                        content.insert(index2,f".{port}".ljust(tabsize)+f" ({local_param}),\n")
                        with open (f'{file_name}','w') as f:
                            f.writelines(content)
                            print(Fore.LIGHTGREEN_EX + f'Port Connected to {local_param}' + Fore.RESET)
                    else:
                        content.pop(index2)
                        content.insert(index2,f".{port}".ljust(tabsize)+f" ({local_param}),\n")
                        with open (f'{file_name}','w') as f:
                            f.writelines(content)
                            print(Fore.LIGHTGREEN_EX + f'Port Connected to {local_param}' + Fore.RESET)
        except: 
            print(Fore.RED,f"{instance} is not present in {file_name}!",Fore.RESET)
            exit()

def check_json_inst_ports(Top_level_file,instance,ports,Baseboard_path):
    json_file=Top_level_file.replace(".sv",'.json')
    with open(f"{Baseboard_path}/{json_file}") as j:
        data=json.load(j)
        try:
            if ports in data[instance]['ports']:
                return True
            else:
                print(Fore.RED,f"{ports} is not present in {instance}!",Fore.RESET)
                exit()
        except:
            print(Fore.RED,f"{instance} is not present in {Top_level_file}!",Fore.RESET)
            exit()

def connect_to_value(Top_level_file,instance,port,value):
     with open (f'{Top_level_file}','r') as f:
                    content=f.readlines()
                    index1=False;index2=False
                    for string in content:
                       if instance in string:
                            index2=index1=content.index(string)
                            for string in content[index1+1:]:
                                index2+=1
                                if f'.{port}' in string:
                                    if content[index2+1].startswith("."):
                                        content.pop(index2)
                                        content.insert(index2,f".{port}".ljust(tabsize) +f"({value}),\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {value}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)
                                            success=False
                                    else:
                                        content.pop(index2)
                                        content.insert(index2,f".{port}".ljust(tabsize)+f"({value})\n")
                                        print(Fore.LIGHTGREEN_EX + f'Port Connected to {value}' + Fore.RESET)
                                        with open (f'{Top_level_file}','w') as f:
                                            f.writelines(content)
                                            success=False