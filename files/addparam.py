#!/usr/bin/python3
import json
from colorama import Fore
import re
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
        try:
            if param in data['parameter']:
                filename=filename.replace(".json",".sv")
                print(Fore.LIGHTRED_EX + f"{param} already exists in {filename}" + Fore.RESET)
                print(Fore.LIGHTRED_EX + f"Please change the parameter name" + Fore.RESET)
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
    
#############################################################################################################
def ovride_prms(filename,prv_w, nw_w,inst):
    module_name = str(filename).replace('.sv','')
    with open(filename, 'r') as file:
        content = file.read()
        match1 = re.search(rf'{inst}\s*#\(\s*([\s\S]*?)\s*\)\s*;', content,re.DOTALL)
        match2 = re.search(rf'{module_name}\s*#\(\s*([^)]*)\s*\)', content, re.DOTALL)
        if match2:
            mod_parm = match2.group(1).rstrip()
            prm_dec = [True for prm in nw_w if prm in mod_parm ]
        match = re.search(rf'{inst}\s*#\(\s*([^)]*)\s*\)', content, re.DOTALL)
        if match1:
            ext_pram = match1.group(1).split()
        if match:
            existing_prm = match.group(1)
            existing_prm += "" if existing_prm else ""
            if prm_dec:
                Body = "".join([f'\n\t.{prm}\t\t({("".join(rng))}),'for prm, rng in zip(prv_w, nw_w) if f".{prm}" not in ext_pram])
                if Body:
                    print(Fore.GREEN + f"{prv_w} added to {inst}" + Fore.RESET)
                else:
                    print(
                        Fore.RED + f"{prv_w} already exists in {inst}" + Fore.RESET)
                    exit()
                new_text = f"{inst}\n#(\n\t{existing_prm}),{Body.rstrip(',')}"
                content = content.replace(match.group(0), new_text)
            else:
                print(Fore.RED + f"Please declare {nw_w} in parameters." + Fore.RESET)
        else:
            if prm_dec:
                Body = "".join([f'\n\t.{prm}\t\t({("".join(rng))}),' for prm, rng in zip(prv_w, nw_w)])
                if Body:
                    print(Fore.GREEN + f"{prv_w} added to {inst}" + Fore.RESET)
                    pattern_text = f"{inst}\n#(\n\t{Body.rstrip(',')}\n)"
                    content = content.replace(f'{inst}', pattern_text)
            else:
                print(Fore.RED + f"Please declare {nw_w} in parameters." + Fore.RESET)
            
        with open(filename, 'w') as f:
            f.write(content)

def adding_localparam(fileName,prms,wid,inst=None):
    if inst is None:
        param = "".join([f'parameter\t{p}\t= {w};\n' for p,w in zip(prms,wid)])
        import plug
        plug.io_outside(param)
    else:
        with open(fileName,"r+") as f:
            content = f.readlines()
            for string in content:
                if f"{inst}" in string:
                    index = content.index(string)
                    break
            param = "".join([f'parameter\t{p}\t= {w};\n' for p,w in zip(prms,wid)])
            content.insert(index,param)
        with open(fileName,'w') as write_file:
                write_file.writelines(content)

# local_param("clock.sv","SEC","wids",'32')

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description='Add parameters to a Verilog module')
#     parser.add_argument('-f', '--filename', type=str,
#                         help='the name of the Verilog file to modify')
#     parser.add_argument('-nw', '--new_width', type=str, nargs='+',
#                         help='the name of the parameter(s) to add')
#     parser.add_argument('-ow', '--old_width', type=str, nargs='+',
#                         help='the name of the parameter(s) to add')
#     parser.add_argument('-n', '--instance', type=str,
#                         help='the name of instance in which parameter need to be override')
#     args = parser.parse_args()

#     ovride_prms(args.filename, args.instance,args.old_width,args.new_width)