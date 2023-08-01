#!/usr/bin/python3
import json
from colorama import Fore
import re
from create import tabsize
success = False
def adding_parameters(filename, param, value):
    inst_name = filename.replace(".sv","")
    global success
    if success is False:
        exit()
    with open(filename, "r") as f:
        data = f.read()
        instance_regex = re.compile(rf'module {inst_name}\s*#\(')
        result = re.search(instance_regex, data)
        if result:
            new_param = f"\t parameter {param} = {value},\n"
            new = data[:result.end()+1] + new_param + data[result.end()+1:] 
            with open(filename, "w") as n:
                n.write(new)
                success = True
        else:
            instance_regex = re.compile(rf'module {inst_name}')
            result = re.search(instance_regex, data)
            if result:
                new_param = f"\n#(\n \t parameter {param} = {value}\n)\n"
                new = data[:result.end()] + new_param + data[result.end():] 
                with open(filename, "w") as n:
                    n.write(new)
                    success = True
            else:
                print(Fore.RED + f"Error: {inst_name} not found in {filename}" + Fore.RESET)
                success = False
        
            
def parameter_json(filename,param,ranges,Baseboard_path):
    global success
    filename=filename.replace(".sv",".json")
    with open (f"{Baseboard_path}/{filename}",'r') as j:
        data=json.load(j)
        for key, value in data['ports'].items():
            if param in value['range']:
                new_range = value['range'].replace(param, ranges)
                start,end = new_range.split(':')
                start=start.replace("[","")
                end=end.replace("]","")
                start=int(start.split("-")[0]) - int(start.split("-")[1])
                new_range = f'[{start}:{end}]'
                data['ports'][key] = {'type': value['type'], 'range': new_range}
        try:
            if param in data['parameter']:
                filename=filename.replace(".json",".sv")
                print(Fore.LIGHTRED_EX + f"{param} already exists in {filename}" + Fore.RESET)
                print(Fore.LIGHTRED_EX + f"Please change the parameter name" + Fore.RESET)
                success = False
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
    
def ovride_prms(filename,nw_w,prv_w,inst):
    module_name = str(filename).replace('.sv','')
    with open(filename, 'r') as file:
        content = file.read()
        match1 = re.search(rf'.*#\(\s*(.*?)\s*\)\s\S\s{inst}', content, re.DOTALL)
        match2 = re.search(rf'{module_name}\s*#\(\s*([^)]*)\s*\)', content, re.DOTALL)
        if match2:
            mod_parm = match2.group(1).rstrip()
            prm_dec = [True for prm in nw_w if prm in mod_parm ]
        match = re.search(rf'#\(\s*(.*?)\s*\)\s\S\s{inst}', content, re.DOTALL)
        if match1:
            ext_pram = match1.group(1).split()
        if match:
            existing_prm = match.group(1)
            existing_prm += "" if existing_prm else ""
            if prm_dec:
                Body = "".join([f'\n.{prm}'.ljust(tabsize)+f'({("".join(rng))},'for prm, rng in zip(prv_w, nw_w) if f".{prm}" not in ext_pram])
                if Body:
                    for prv_w in prv_w:
                        print(Fore.GREEN + f"{prv_w} added to {inst}" + Fore.RESET)
                else:
                    for prv_w in prv_w:
                        print(Fore.RED + f"{prv_w} already exists in {inst}" + Fore.RESET)
                    exit()
                new_text = f"{existing_prm}),{Body.rstrip(',')}"
                content = content.replace(match.group(1), new_text)
            else:
                print(Fore.RED + f"Please declare {nw_w} in parameters." + Fore.RESET)
        else:
            if prm_dec:
                Body = "".join([f'\n.{prm}'.ljust(tabsize)+f'({("".join(rng))}),' for prm, rng in zip(prv_w, nw_w)])
                if Body:
                    for prv_w in prv_w:
                        print(Fore.GREEN + f"{prv_w} added to {inst}" + Fore.RESET)
                    pattern_text = f"\n#(\n\t{Body.rstrip(',')}\n)\n{inst}"
                    content = content.replace(f"{inst}", pattern_text)
            else:
                print(Fore.RED + f"Please declare {nw_w} in parameters." + Fore.RESET)
            
        with open(filename, 'w') as f:
            f.write(content)

def adding_localparam(fileName,prms,wid):
        param = "".join([f'parameter\t{prms}\t= {wid};'])
        io_outside(fileName,param)
        
def io_outside(fileName,ios):
    m_name = fileName.replace(".sv", "")
    with open(fileName, 'r') as f:
        file_contents = f.read()
    pattern = rf".*?(module\s+{m_name}\s*((?:[\s\S]*?);))"
    match = re.search(pattern, file_contents)
    if match:
        block = match.group(1)
        new_data = block + f"\n{ios}"
        file_contents = re.sub(pattern, new_data, file_contents)
        with open(fileName, 'w') as f:
            f.write(file_contents)
    else:
        print(Fore.RED + f"Module {m_name} not found" + Fore.RESET)
        exit()