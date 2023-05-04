#!/usr/bin/python3
import json
from colorama import Fore
def add_wire(file_name,name,range):
    with open (file_name) as f:
        content = f.readlines()
        for string in content:
            if ");" in string:
                index = content.index(string)
                break
        content.insert(index+1,f"wire  \t {range} \t {name};\n")
        print(Fore.GREEN,f"wire {name} added successfully",Fore.RESET)
        # except:
        #     for string in content:
        #         if ");" in string:
        #             index = content.index(string)
        #             break
        #     content.insert(index+1,f"wire  \t {range} \t {name};\n")
        #     print(Fore.GREEN,f"wire {name} added successfully",Fore.RESET)
        with open(file_name,'w') as write_file:
            write_file.writelines(content)
            
def add_wire_to_json(file_name,name,range,Baseboard_path):
    json_file=file_name.replace(".sv",".json")
    with open(f"{Baseboard_path}/{json_file}", "r") as read_file:
        data = json.load(read_file)
        if name in data:
            print(Fore.RED,f"Error: {name} wire already exists",Fore.RESET)
            choice=input("Do you want to overwrite it? (y/n) : ")
            if choice=='y' or choice=='Y':
                data[name]={"range":range,"type":"wire"}
            else:
                print(Fore.RED,"Aborting...",Fore.RESET)
                exit()
        else:
            data[name]={"range":range,"type":"wire"}
            
        with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
            json.dump(data, write_file, indent=4)
    
def add_reg_to_json(file_name,name,range,Baseboard_path):
    json_file=file_name.replace(".sv",".json")
    with open(f"{Baseboard_path}/{json_file}", "r") as read_file:
        data = json.load(read_file)
        if name in data:
            print(Fore.RED,"Error: This register already exists",Fore.RESET)
            choice=input("Do you want to overwrite it? (y/n) : ")
            if choice=='y' or choice=='Y':
                data[name]={"range":range,"type":"reg"}
            else:
                print(Fore.RED,"Aborting...",Fore.RESET)
                exit()
        else:
            data[name]={"range":range,"type":"reg"}
            
        with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
            json.dump(data, write_file, indent=4)
        
def add_reg(file_name,name,range):
    with open (file_name) as f:
        content = f.readlines()
        try:
            for string in content:
                if "reg" in string:
                    index = content.index(string)
                    break
            content.insert(index+1,f"reg  \t {range} \t {name};\n")
            print(Fore.GREEN,f"Register {name} added successfully",Fore.RESET)
        except:
            for string in content:
                if ");" in string:
                    index = content.index(string)
                    break
            content.insert(index+1,f"reg  \t {range} \t {name};\n")
            print(Fore.GREEN,f"Register {name} added successfully",Fore.RESET)
        with open(file_name,'w') as write_file:
            write_file.writelines(content)