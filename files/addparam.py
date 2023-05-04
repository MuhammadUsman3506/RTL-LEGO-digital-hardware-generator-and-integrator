#!/usr/bin/python3
import json
from colorama import Fore
success = False
def adding_parameters(filename, param, value):
    global success
    if success is False:
        exit()
    with open (filename,'r') as topfile:
        data=topfile.readlines()
        if data[0].endswith("#(\n"):
            existing_param = data[1].replace("\n",",\n")
            existing_param = existing_param+f"\tparameter {param}  \t = {value}\n"

            data.remove(data[1])
            data.insert(1,existing_param)
            print(Fore.BLUE + f"{param} added in {filename}" + Fore.RESET)
        else:
            first_line = data[0].replace("(\n","#(\n")
            data.remove(data[0])
            data.insert(0,first_line)
            data.insert(1,f"\tparameter {param}  \t = {value}\n)\n\n(\n")
            print(Fore.BLUE + f"{param} added in {filename}" + Fore.RESET)
        with open (filename,'w') as topfile:
            topfile.writelines(data)
            
def parameter_json(filename,param,ranges,Baseboard_path):
    global success
    filename=filename.replace(".sv",".json")
    with open (f"{Baseboard_path}/{filename}",'r') as j:
        data=json.load(j)
        try:
            if param in data['parameter']:
                print(Fore.RED + f"{param} already exists in {filename}" + Fore.RESET)
                print(Fore.RED + f"Please change the parameter name" + Fore.RESET)
                return
            elif data.get('parameter'):
                 data['parameter'][param]=ranges
                 with open (f"{Baseboard_path}/{filename}",'w') as n:
                    new = json.dumps(data,indent=4)
                    n.write(new)
                    success = True
        except:      
            data.update({"parameter":{param:ranges}})
            with open (f"{Baseboard_path}/{filename}",'w') as n:
                new = json.dumps(data,indent=4)
                n.write(new)
                success = True