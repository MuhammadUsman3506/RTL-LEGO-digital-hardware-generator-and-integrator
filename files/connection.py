#!/usr/bin/python3
import json
from colorama import Fore
import re
def connect_to_reg(Top_level_file,reg_name,instance_name,port_name,Baseboard_path):
    json_file=Top_level_file.replace(".sv",".json")
    with open(f'{Baseboard_path}/{json_file}', 'r') as f:
        data = json.load(f)
        if reg_name in data:
           if  port_name in data[instance_name]['ports']:
               with open (f'{Top_level_file}','r') as f:
                    content=f.readlines()
                    for string in content:
                       if instance_name in string:
                            index2=content.index(string)
                       if f'.{port_name}' in string:
                            index1=content.index(string)
                            break
                    if index2>index1:
                        if content.index[index1+1].startswith("."):
                            content.pop(index1)
                            content.insert(index1,f".{port_name} \t\t ({reg_name}),\n")
                            print(Fore.LIGHTGREEN_EX + 'Port Connected to' + Fore.RESET)
                            with open (f'{Top_level_file}','w') as f:
                                f.writelines(content)
                        else:
                            content.pop(index1)
                            content.insert(index1,f".{port_name} \t\t ({reg_name})\n")
                            print(Fore.LIGHTGREEN_EX + 'Port Connected to reg' + Fore.RESET)
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
        if wire_name in data:
            if  port_name in data[instance_name]['ports']:
               with open (f'{Top_level_file}','r') as f:
                    content=f.readlines()
                    index=False;index2=False
                    for string in content:
                        if instance_name in string:
                            index=content.index(string)
                            break
                    for string in content:
                        if f'.{port_name}' in string:
                            index2=content.index(string)
                            if index2>index:
                                break
                    try: 
                        if content[index2+1].startswith("."): 
                            content.pop(index2)
                            content.insert(index2,f".{port_name} \t\t ({wire_name}),\n")
                            print(Fore.LIGHTGREEN_EX + f'Port Connected to wire' + Fore.RESET)
                            with open(f'{Top_level_file}','w') as f:
                                f.writelines(content)
                        else:
                            content.pop(index2)
                            content.insert(index2,f".{port_name} \t\t ({wire_name})\n")
                            print(Fore.LIGHTGREEN_EX + 'Port Connected to wire' + Fore.RESET)
                            with open (f'{Top_level_file}','w') as f:
                                f.writelines(content)
                    except IndexError:
                       print(Fore.RED,"IndexError",Fore.RESET)
                       return
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
                    block = re.sub(pattern, fr'.{input_port} \t\t\t\t({connected_ports_str})', block)
                else:
                    block = re.sub(pattern, f'.{input_port} \t\t\t\t({output_port})', block)       
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
                    index=False;index2=False
                    for string in content:
                        if instance in string:
                            index=content.index(string)
                            break
                    for string in content:
                        if ports in string:
                            index2=content.index(string)
                            if index2>index:
                                break
                            
                    if content[index2+1].startswith("."):
                        content.pop(index2)
                        content.insert(index2,f".{ports} \t\t ({param}),\n")
                        print(Fore.LIGHTGREEN_EX + 'Port Connected to parameter' + Fore.RESET)
                        with open(f'{Top_level_file}','w') as f:
                            f.writelines(content)
                    else:
                        content.pop(index2)
                        content.insert(index2,f".{ports} \t\t ({param})\n")
                        print(Fore.LIGHTGREEN_EX + 'Port Connected to parameter' + Fore.RESET)
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
                            for string in content:
                                if instance in string:
                                    index = content.index(string)
                                if ports in string:
                                    index1 = content.index(string)
                                    break
                            if index1 > index:
                                Modified_port = f".{ports} \t\t\t ({param})\n"
                                content.pop(index1)
                                content.insert(index1, Modified_port)
                                print(Fore.LIGHTGREEN_EX + 'Parameter Connected.' + Fore.RESET)
                                with open(f"{Top_level_file}", 'w') as f:
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
                        index=False;index2=False
                        for string in content:
                            if instance1 in string:
                                index=content.index(string)
                                break
                        for string in content:
                            if input_port in string:
                                index2=content.index(string)
                                if index2>index:
                                    break
                        content.pop(index2)
                        content.insert(index2,f".{input_port} \t\t\t ({output_ports}),\n")
                        with open (fille_name,'w') as wri:
                            wri.writelines(content)
                        print(Fore.GREEN,f"{input_port} is connected to {output_ports}")        
            else:
                print( Fore.RED,f"{input_port} is not present in {instance1}!",Fore.RESET)
                exit()
        else:
            print(Fore.RED,f"{instance1} is not present in {fille_name} ",Fore.RESET) 
            exit()