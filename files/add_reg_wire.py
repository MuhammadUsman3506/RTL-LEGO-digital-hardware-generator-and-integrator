#!/usr/bin/python3
import json
from colorama import Fore
succes=False
def add_wire(file_name,name,range):
    if range == "None":
        range=" "
    global succes
    if succes==True:
        with open (file_name) as f:
            content = f.readlines()
            for string in content:
                if ");" in string:
                    index = content.index(string)
                    break
            content.insert(index+1,f"wire  \t {range} \t {name};\n")
            print(Fore.GREEN,f"wire {name} added successfully",Fore.RESET)
            with open(file_name,'w') as write_file:
                write_file.writelines(content)
            
def add_wire_to_json(file_name,name,range,Baseboard_path):
    global succes
    json_file=file_name.replace(".sv",".json")
    with open(f"{Baseboard_path}/{json_file}", "r") as read_file:
        data = json.load(read_file)
        try:
            if name in data['wire']:
                print(Fore.RED,f"Error: {name} wire already exists",Fore.RESET)
                choice=input("Do you want to overwrite it? (y/n) : ")
                if choice=='y' or choice=='Y':
                    data['wire']={name:range}
                    succes=True
                else:
                    print(Fore.RED,"Aborting...",Fore.RESET)
                    return 0
            else: 
                if "[" in range:
                        range=range.replace("[","")
                        range=range.replace("]","")
                        var = range.split(":")
                        param = var[0].split("-")
                        if param[0].isdigit():
                            try:
                                range=f"[{range}]"
                                data['wire'].update({name:range})
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                            except:
                                data['wire']={name:range}
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                        else:
                            if param[0] in data['parameter']:
                                param_value=data['parameter'][param[0]]
                                param_value=int(param_value)-int(param[1])
                                new=f'[{param_value}:{var[1]}]'
                                data['wire'].update({name:new})
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                            else:
                                print(Fore.RED,"Error: This parameter doesn't exist",Fore.RESET)
                                exit()
                else:   
                    data['wire'].update({name:range})
                    with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                        json.dump(data, write_file, indent=4)
                        succes=True
   
        except:
            if succes is not True:
                if "[" in range:
                        range=range.replace("[","")
                        range=range.replace("]","")
                        var = range.split(":")
                        param = var[0].split("-")
                        if param[0].isdigit():
                            try:
                                range=f"[{range}]"
                                data['wire'].update({name:range})
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                            except:
                                data['wire']={name:range}
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                        else:
                            if param[0] in data['parameter']:
                                param_value=data['parameter'][param[0]]
                                param_value=int(param_value)-int(param[1])
                                new=f'[{param_value}:{var[1]}]'
                                data['wire']={name:new}
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True     
                            else:
                                print(Fore.RED,"Error: This parameter doesn't exist",Fore.RESET)
                                exit()
                else:   
                    data['wire']={name:range}
                    with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                        json.dump(data, write_file, indent=4)
                        succes=True
                            
    
def add_reg_to_json(file_name,name,range,Baseboard_path):
    global succes
    json_file=file_name.replace(".sv",".json")
    with open(f"{Baseboard_path}/{json_file}", "r") as read_file:
        data = json.load(read_file)
        try:
            if name in data['reg']:
                print(Fore.RED,"Error: This register already exists",Fore.RESET)
                choice=input("Do you want to update it? (y/n) : ")
                if choice=='y' or choice=='Y':
                    if "[" in range:
                        range=range.replace("[","")
                        range=range.replace("]","")
                        var = range.split(":")
                        param = var[0].split("-")
                        if param[0].isdigit():
                            try:
                                range=f"[{range}]"
                                data['reg'].update({name:range})
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                            except:
                                data['reg']={name:range}
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                        else:
                            if param[0] in data['parameter']:
                                param_value=data['parameter'][param[0]]
                                param_value=int(param_value)-int(param[1])
                                new=f'[{param_value}:{var[1]}]'
                                data['reg'].update({name:new})
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True     
                            else:
                                print(Fore.RED,"Error: This parameter doesn't exist",Fore.RESET)
                                exit()
                    else:   
                        data['reg'].update({name:range})
                        with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                            json.dump(data, write_file, indent=4)
                            succes=True
        
                    with open(file_name) as f:
                        content=f.readlines()
                        index1=0;index2=0
                        for string in content:
                            if ');' in string:
                                index1=content.index(string)
                            if name in string:
                                index2=content.index(string)
                            if index2>index1:
                                content.pop(index2)
                                content.insert(index2,f"reg  \t {range} \t {name};\n")
                                with open(file_name,'w') as write_file:
                                    write_file.writelines(content)
                                    break
                        return
                else:
                    print(Fore.RED,"Aborting...",Fore.RESET)
                    return 
            else:
                if "[" in range:
                    range=range.replace("[","")
                    range=range.replace("]","")
                    var = range.split(":")
                    param = var[0].split("-")
                    if param[0].isdigit():
                            try:
                                range=f"[{range}]"
                                data['reg'].update({name:range})
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                            except:
                                data['reg']={name:range}
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                    else:
                        if param[0] in data['parameter']:
                            param_value=data['parameter'][param[0]]
                            param_value=int(param_value)-int(param[1])
                            new=f'[{param_value}:{var[1]}]'
                            data['reg'].update({name:new})
                            with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                json.dump(data, write_file, indent=4)
                                succes=True     
                        else:
                            print(Fore.RED,"Error: This parameter doesn't exist",Fore.RESET)
                            exit()
                else: 
                    data['reg'].update({name:range})
                    with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                        json.dump(data, write_file, indent=4)
                        succes=True
        except:
            if succes is not True:
                if "[" in range:
                    range=range.replace("[","")
                    range=range.replace("]","")
                    var = range.split(":")
                    param = var[0].split("-")
                    if param[0].isdigit():
                            try:
                                range=f"[{range}]"
                                data['reg'].update({name:range})
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                            except:
                                data['reg']={name:range}
                                with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                    json.dump(data, write_file, indent=4)
                                    succes=True
                    else:
                        if param[0] in data['parameter']:
                            param_value=data['parameter'][param[0]]
                            param_value=int(param_value)-int(param[1])
                            new=f'[{param_value}:{var[1]}]'
                            data['reg']={name:new}
                            with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                                json.dump(data, write_file, indent=4)
                                succes=True     
                        else:
                            print(Fore.RED,"Error: This parameter doesn't exist",Fore.RESET)
                            exit()
                else:   
                    data['reg']={name:range}
                    with open(f"{Baseboard_path}/{json_file}", "w") as write_file:
                        json.dump(data, write_file, indent=4)
                        succes=True
        
        
def add_reg(file_name,name,range):
    if range == "None":
        range=" "
    if succes==True:
        with open (file_name) as f:
            content = f.readlines()
            for string in content:
                if ");" in string:
                    index = content.index(string)
                    break
            content.insert(index+1,f"reg  \t {range} \t {name};\n")
            with open(file_name,'w') as write_file:
                write_file.writelines(content)
            print(Fore.GREEN,f"Register {name} added successfully",Fore.RESET)