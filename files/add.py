#!/usr/bin/python3
import re
import os
import argparse,json
from colorama import Fore
import addparam
import changeIOandRange
import add_reg_wire
LEGO_DIR = ''
Top_level_file = ''
CURRENT_DIR = os.getcwd()
#################### LAGO ROOT address #######################################


def LEGO_USR_INFO():
    global LEGO_DIR, Top_level_file
    Linux_file_path = os.path.expanduser("~/.LEGO_USR_INFO")
    with open(Linux_file_path, "r") as Shell_file:
        sh_file = Shell_file.readlines()
        LEGO_DIR = sh_file[0].replace("LEGO_DIR=", "")+"/files/"
        if Top_level_file:
            if f"TOP_FILE={Top_level_file}\n" in sh_file:
                pass
            else:
                print(f"{Top_level_file} is not present")
                exit()
        else:
            Top_level_file = sh_file[-1]
    LEGO_DIR = LEGO_DIR.replace("\n", "")
    Top_level_file = Top_level_file.replace("TOP_FILE=", '')

##############################################################################

def update_json(json_data):
        try:
            param=json_data['parameter']
            for key, value in json_data['ports'].items():
                if str(list(param.keys())[0]) in value['range']:
                    new_range = value['range'].replace(str(list(param.keys())[0]), str(list(param.values())[0]))
                    start,end = new_range.split(':')
                    start=start.replace("[","")
                    end=end.replace("]","")
                    start=int(start.split("-")[0]) - int(start.split("-")[1])
                    new_range = f'[{start}:{end}]'
                    json_data['ports'][key] = {'type': value['type'], 'range': new_range}
            return json_data
        except:
            return json_data


def add_inputs_outputs(fileName, inputs, input_ranges, outputs, output_ranges):
    instance_name = fileName.replace('.sv', '')
    with open(fileName, 'r') as f:
        content = f.read()
    pattern1 = rf'module\s+{instance_name}\s*#\(\s*([^)]*)\s*\)\s*([^)]*)\s*\s*.;'
    pattern2 = rf".*?(module\s+{instance_name}\s*((?:[\s\S]*?);))"
    match1 = re.search(pattern1, content, re.DOTALL)
    match2 = re.search(pattern2, content, re.DOTALL)

    if match1:
        existing_ports1 = match1.group(1)
        existing_ports = match1.group(2)
        existing_ports = existing_ports.rstrip()
        if existing_ports != '':
            existing_ports += ','
        else:
            existing_ports += ' '
        body = ''
        if inputs:
            i = ''
            for inp, inp_ranges in zip(inputs, input_ranges):
                if inp in existing_ports:
                    print(Fore.RED + f"{inp} already exists in {fileName}" + Fore.RESET)
                    exit()
                else:
                    if inp_ranges == 'None' or inp_ranges == 'none':
                        inpu = f"\ninput\tlogic\t\t{(i.join(inp))},"
                        print(Fore.GREEN + f"{inp} is added in {fileName}" + Fore.RESET)
                        body = body + inpu
                    else:
                        inpu = f"\ninput\tlogic\t{inp_ranges}\t{(i.join(inp))},"
                        print(Fore.GREEN + f"{inp} is added in {fileName}" + Fore.RESET)
                        body = body + inpu
               
        if outputs:
            o = ''
            for out, opt_ranges in zip(outputs, output_ranges):
                if out in existing_ports:
                    print(Fore.RED + f"{out} already exists in {fileName}" + Fore.RESET)
                    exit()
                else:
                    if opt_ranges == 'None' or opt_ranges == 'none':
                        outu = f"\noutput\tlogic\t\t{o.join(out)},"
                        print(Fore.GREEN + f"{out} is added in {fileName}" + Fore.RESET)
                        body = body + outu
                    else:
                        outu = f"\noutput\tlogic\t{opt_ranges}\t{o.join(out)},"
                        print(Fore.GREEN + f"{out} is added in {fileName}" + Fore.RESET)
                        body = body + outu
            
        body = body.rstrip(",")
        new_instance_text = f'module {instance_name}\n#(\n\t{existing_ports1})\n{existing_ports}{body}\n);'
        new_content = content.replace(match1.group(0), new_instance_text)
        with open(fileName, "w") as f:
            f.write(new_content)
    elif match2:
        existing_ports = re.search(rf'module\s+{instance_name}\s*\((.*?)\);', match2.group(0), re.DOTALL)
        existing_ports = existing_ports.group(1)
        existing_ports = existing_ports.rstrip()
        if existing_ports != '':
            existing_ports += ','
        else:
            existing_ports += ' '
        body = ''
        if inputs:
            i = ''
            for inp, inp_ranges in zip(inputs, input_ranges):
                if inp in existing_ports:
                    print(Fore.RED + f"{inp} already exists in {fileName}" + Fore.RESET)
                    exit()
                else:
                    if inp_ranges == 'None' or inp_ranges == 'none':
                        inpu = f"\ninput\tlogic\t\t{(i.join(inp))},"
                        print(Fore.GREEN + f"{inp} is added in {fileName}" + Fore.RESET)
                        body = body + inpu
                    else:
                        inpu = f"\ninput\tlogic\t{inp_ranges}\t{(i.join(inp))},"
                        print(Fore.GREEN + f"{inp} is added in {fileName}" + Fore.RESET)
                        body = body + inpu
                 
        if outputs:
            o = ''
            for out, opt_ranges in zip(outputs, output_ranges):
                if out in existing_ports:
                    print(Fore.RED + f"{out} already exists in {fileName}" + Fore.RESET)
                    exit()
                else:
                    if opt_ranges == 'None' or opt_ranges == 'none':
                        outu = f"\noutput\tlogic\t\t{o.join(out)},"
                        print(Fore.GREEN + f"{out} is added in {fileName}" + Fore.RESET)
                        body = body + outu
                    else:
                        outu = f"\noutput\tlogic\t{opt_ranges}\t{o.join(out)},"
                        print(Fore.GREEN + f"{out} is added in {fileName}" + Fore.RESET)
                        body = body + outu
                 
        body = body.rstrip(",")
        new_instance_text = f'({existing_ports}{body}\n);'
        new_content = content.replace(match2.group(2), new_instance_text)
        with open(fileName, "w") as f:
            f.write(new_content)
def add_inputs_outputs_JSON(fileName,inputs, input_ranges, ouputs,output_ranges,Baseboard_path):
    json_file=fileName.replace('.sv','.json')
    with open(f"{Baseboard_path}/{json_file}") as f:
        data = json.load(f)
        if inputs:
            for inputs, input_ranges in zip(inputs, input_ranges):
                if inputs in data['ports']:
                    print(Fore.RED + f"{inputs} already exists in {fileName}" + Fore.RESET)
                    exit()
                else:
                    s={'type':'input','range':input_ranges} 
                    data['ports'].update({inputs:s})

        if ouputs:
            for output,range in zip(ouputs,output_ranges):
                if output in data['ports']:
                    print(Fore.RED + f"{output} already exists in {fileName}" + Fore.RESET)
                    exit()
                else:
                    s={'type':'output','range':range} 
                    data['ports'].update({output:s})
    data=update_json(data)
    with open(f"{Baseboard_path}/{json_file}" , 'w') as f:
        json.dump(data, f, indent=4)
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw',"--new_width",type=str,nargs='+',help='the name of the parameter(s) to add')
    parser.add_argument('-ow',"--old_width",type=str,nargs='+',help='the name of the parameter(s) to add')       
    parser.add_argument('-c',"--change",type=str,help='change IO status or range')
    parser.add_argument('-P', '--parameter',nargs='+',help='the name of the parameter(s) to add')
    parser.add_argument('-lp','--localparam',nargs='+',help='the name of the localparam(s) to add')
    parser.add_argument('-v', '--value',nargs='+', help='the value of the parameter(s) to add')
    parser.add_argument('-inst','--instance',help='instance name')
    parser.add_argument('-r','--reg',help='reg',nargs='+', type=str)
    parser.add_argument('-w','--wire',help='wire', nargs='+',type=str)
    parser.add_argument('-rn','--range',help='range',nargs='+',type=str,default=['None'])
     
    
    parser.add_argument('-nr','--new_range', help='New range of input or output port')
    parser.add_argument('-pr','--port_name', help='Name of the port to update (for update_range, update_range_json, change_IO_status, and change_IO_status_json operations)')
    parser.add_argument('-ns','--new_status', choices=['input', 'output'], help='New status to update (for change_IO_status and change_IO_status_json operations)')

    
    parser.add_argument('-t,','--topfile',help='Top level file name', type=str)
    
    parser.add_argument('-i', '--inputs',nargs='+',help='Input port name')
    parser.add_argument('-ir', '--input_ranges',nargs='+',help='Input port range',default=['None'])
    parser.add_argument('-o', '--outputs',nargs='+',help='Output port name')
    parser.add_argument('-or', '--output_ranges',nargs='+',help='Output port range',default=['None'])
    args=parser.parse_args()
    
    Top_level_file = args.topfile  
    
    LEGO_USR_INFO()
    Baseboard_path = os.path.join(LEGO_DIR, 'Baseboard')

    if args.new_width and args.old_width and args.instance:
        addparam.ovride_prms(Top_level_file,args.new_width,args.old_width,args.instance)
        exit()
    
    if args.reg:
        if args.range:
            for args.reg,args.range in zip(args.reg,args.range):
                add_reg_wire.add_reg_to_json(Top_level_file,args.reg,args.range,Baseboard_path)
                add_reg_wire.add_reg(Top_level_file,args.reg,args.range)
            exit()
          
    if args.wire:
            for args.wire,args.range in zip(args.wire,args.range):
                add_reg_wire.add_wire_to_json(Top_level_file,args.wire,args.range,Baseboard_path)
                add_reg_wire.add_wire(Top_level_file,args.wire,args.range)
            exit()
    if args.inputs:
            add_inputs_outputs_JSON(Top_level_file,args.inputs,args.input_ranges,args.outputs,args.output_ranges,Baseboard_path)
            add_inputs_outputs(Top_level_file,args.inputs,args.input_ranges,args.outputs,args.output_ranges)
            exit()
    if args.outputs:
            add_inputs_outputs_JSON(Top_level_file,args.inputs,args.input_ranges,args.outputs,args.output_ranges,Baseboard_path)
            add_inputs_outputs(Top_level_file,args.inputs,args.input_ranges,args.outputs,args.output_ranges)
            exit()

    if args.parameter:
        if args.value:
            for args.parameter,args.value in zip(args.parameter,args.value):
                addparam.parameter_json(Top_level_file,args.parameter,args.value,Baseboard_path)
                addparam.adding_parameters(Top_level_file,args.parameter,args.value)
            exit()
        else:
            print("Please provide value for parameter(s) to add")
            print("Example:add -P <parameter> 'WIDTH' -v <value> '32' -t <topfile> 'top.sv")
            exit()
            
    if args.localparam:
        if args.value:
            for args.localparam,args.value in zip(args.localparam,args.value):
                addparam.parameter_json(Top_level_file,args.localparam,args.value,Baseboard_path)
                addparam.adding_localparam(Top_level_file,args.localparam,args.value)
            exit()
        else:
            print("Please provide value for localparam(s) to add")
            print("Example:add -lp <localparam> 'WIDTH' -v <value> '32' -t <topfile> 'top.sv")
            exit()
            
    if args.change:
        if args.change=='range':
            if args.port_name and args.new_range:
                changeIOandRange.update_ranges(Top_level_file,args.port_name,args.new_range)
                changeIOandRange.update_ranges_json(Top_level_file,args.port_name,args.new_range,Baseboard_path)
            else:
                print("Please provide port name and new range")
                print("Example:add -c <change> 'range' -pr <port_name> 'clk' -nr <new_range> '32' -t <topfile> 'top.sv")
                exit()
        elif args.change=='port':
            if args.port_name and args.new_status: 
                changeIOandRange.change_IO_status(Top_level_file,args.port_name,args.new_status)
                changeIOandRange.change_IO_status_json(Top_level_file,args.port_name,args.new_status,Baseboard_path)
            else:
                print("Please provide port name and new status")
                print("Example:add -c <change> 'port' -pr <port_name> 'clk' -ns <new_status> 'input' -t <topfile> 'top.sv")
                exit()
        else:
            print("Please provide valid change option")
            print("Example:add -c <change> 'range' -p <port_name> 'clk' -nr <new_range> '32' -t <topfile> 'top.sv")
            print("Example:add -c <change> 'port' -p <port_name> 'clk' -ns <new_status> 'input' -t <topfile> 'top.sv")
            exit()
    else:
        print("please provide valid option")
        exit()