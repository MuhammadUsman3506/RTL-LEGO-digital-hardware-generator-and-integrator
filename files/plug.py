#!/usr/bin/python3
import os
import argparse
import json
import Extracting_data
import shutil
import math
import re
from colorama import Fore
from create import tabsize
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

def copy_file(file):
    global CURRENT_DIR, library_file
    if not os.path.exists(f"{CURRENT_DIR}/{file}"):
        shutil.copy(library_file, CURRENT_DIR)

def extract_data(file,instance):               
    global Top_level_file, CURRENT_DIR ,tabsize,library
    #list only files in library not there extension
    files = [os.path.splitext(f)[0] for f in os.listdir(library) if os.path.isfile(os.path.join(library, f))]
    with open(f"{file}", 'r') as f:
        lines = f.readlines()
        for line in lines:
            for file in files:
                if file in line.split() :
                    if '.'  in lines[lines.index(line)+1]: 
                        file=os.path.join(library,f'{file}.sv')
                        if not os.path.exists(f"{CURRENT_DIR}/{file}"):
                            shutil.copy(file, CURRENT_DIR)

    in_module = False
    input_or_output_count = 0
    output_string = ""
    for line in lines:
        if 'module' in line and not in_module:
            in_module = True
            module_name = line.split()[1]
            output_string += module_name + ' ' + f'{instance}' + '\n'
            output_string += "(\n"
        if 'input' in line or 'output' in line:
            input_or_output_count += 1
            words = line.strip().split()
            x = words[-1]
            if "," in x:
                x = x.split(",")[0]
            if input_or_output_count == sum(('input' in line) or ('output' in line) for line in lines):
                output_string += '.' + x.ljust(tabsize) + '()\n'
            else:
                output_string += '.' + x.ljust(tabsize) +  '(),\n'

    with open(f"{CURRENT_DIR}/{Top_level_file}", "r") as f:
        content = f.read()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if instance in line and ('input' or 'output') not in line:
                print(Fore.RED +
                      f'Error: instance {instance} already exists at line {i+1}. Please Enter different name!' + Fore.RESET)
                exit()
        with open(f"{CURRENT_DIR}/{Top_level_file}", "a+") as f:  
            if 'endmodule' in content:
                r_end = (f.tell())-9
                x = f.truncate(r_end)
                f.write('\n\n' + output_string)
                f.write(');')
                f.write('\n\nendmodule')
            print(
                Fore.GREEN + f'instance {instance} is successfully pluged in {Top_level_file}.' + Fore.RESET)

def io_outside(ios):
    global Top_level_file, CURRENT_DIR
    m_name = f"{Top_level_file}".replace(".sv", "")
    with open(f"{CURRENT_DIR}/{Top_level_file}", 'r') as f:
        file_contents = f.read()
    pattern = rf".*?(module\s+{m_name}\s*((?:[\s\S]*?);))"
    match = re.search(pattern, file_contents)
    if match:
        block = match.group(1)
        new_data = block + f"\n{ios}"
        file_contents = re.sub(pattern, new_data, file_contents)
        with open(f"{CURRENT_DIR}/{Top_level_file}", 'w') as f:
            f.write(file_contents)

def generating_mux(input_signals, output_signal, sl):
    leng = len(input_signals)
    rounding_threshold = 0.1
    val = math.log2(leng)
    if leng == 2:
        selct_lin = f'reg\t\t{sl};'
        io_outside(selct_lin)
        code = "always@*\n"
        code += f"\tcase({sl})\n"
        for i, signal in enumerate(input_signals):
            code += f"\t1'd{i}: {str(output_signal)} = {signal};\n"
        code += "\tendcase\n"
        mux_code = code
    else:
        if val - math.floor(val) > rounding_threshold:
            rounded_value = math.ceil(val)
        else:
            rounded_value = math.floor(val)

        selct_lin = f'reg [{rounded_value-1}:0] {sl};'
        io_outside(selct_lin)

        for i_sig in input_signals:
            ranges = f"[{rounded_value-1}:0]"
            signlas = f'reg {ranges} {i_sig};'
            io_outside(signlas)

            code = "always@*\n"
            code += f"\tcase({sl})\n"
            for i, signal in enumerate(input_signals):
                code += f"\t{rounded_value}'d{i}: {str(output_signal)} = {signal};\n"
            code += "\tendcase\n"
            mux_code = code

    # open top file in append mode
    with open(f"{CURRENT_DIR}/{Top_level_file}", "r") as f:
        content = f.read()
    with open(f"{CURRENT_DIR}/{Top_level_file}", "a+") as f:
        if 'endmodule' in content:
            r_end = (f.tell())-9
            x = f.truncate(r_end)
            f.write('\n' + mux_code)
            f.write('\nendmodule')
    return mux_code

def generate_register(inp_sig=None,inp_ranges=None, out_sig=None ,out_ranges=None, enable_sig=None):
    if enable_sig is None:
        if inp_sig:
            if inp_ranges is None:
                inp_declaration = f'reg {inp_sig};'
                io_outside(inp_declaration)
            else:
                inp_declaration = f'reg {inp_ranges} {inp_sig};'
                io_outside(inp_declaration)
        if out_sig:
            if out_ranges is None:
                out_declaration = f'reg {out_sig};'
                io_outside(out_declaration)
            else:
                out_declaration = f'reg {out_ranges} {out_sig};'
                io_outside(out_declaration)
                    
        code = f"always @(posedge clk)\nbegin\n\tif(reset)\n\tbegin\n"
        code += f"\t\t{out_sig} <= 0;\n"
        code += f"\tend\n\telse\n\tbegin\n"
        code += f"\t\t{out_sig} <= {inp_sig};\n"
        code += f"\tend\nend\n"
    else:
        reg_sig = f'reg {enable_sig};'
        io_outside(reg_sig)
        if inp_sig:
            if inp_ranges is None:
                inp_declaration = f'reg {inp_sig};'
                io_outside(inp_declaration)
            else:
                inp_declaration = f'reg {inp_ranges} {inp_sig};'
                io_outside(inp_declaration)
        if out_sig:
            if out_ranges is None:
                out_declaration = f'reg {out_sig};'
                io_outside(out_declaration)
            else:
                out_declaration = f'reg {out_ranges} {out_sig};'
                io_outside(out_declaration)
                
        code = f"always @(posedge clk)\nbegin\n"
        code += f"\tif(reset)\n\tbegin\n"
        code += f"\t\t{out_sig} <= 0;\n"
        code += f"\tend\n\telse if({enable_sig})\n\tbegin\n"
        code += f"\t\t{out_sig} <= {inp_sig};\n"
        code += f"\tend\nend\n"

    with open(f"{CURRENT_DIR}/{Top_level_file}", "r") as f:
        content = f.read()
    with open(f"{CURRENT_DIR}/{Top_level_file}", "a+") as f:
        if 'endmodule' in content:
            r_end = (f.tell())-9
            x = f.truncate(r_end)
            f.write('\n' + code)
            f.write('\nendmodule')

    return code


def fileio(inputs, input_ranges, outputs, output_ranges):
    global Top_level_file, CURRENT_DIR
    m_name = f"{Top_level_file}".replace('.sv', "")
    with open(f"{CURRENT_DIR}/{Top_level_file}", "r") as f:
        file_contents = f.read()
    # pattern = r".*?(clock\s*((?:[\s\S]*?);))"
    pattern = rf".*?(module\s+{m_name}\s*((?:[\s\S]*?);))"
    match = re.search(pattern, file_contents)
    if match:
        block = match.group(1)
        Body = ""
        if inputs:
            for inp_range, input in zip(input_ranges, inputs):
                if inp_range == 'None':
                    input_str = f"reg \t\t{input};\n"
                    Body += input_str
                else:
                    input_str = f"reg\t {inp_range}\t{input};\n"
                    Body += input_str
        if outputs:
            for out_range, output in zip(output_ranges, outputs):
                if out_range == 'None':
                    output_str = f"wire\t\t{output};\n"
                    Body += output_str
                else:
                    output_str = f"wire {out_range}\t{output};\n"
                    Body += output_str

        new = block + f"\n{Body}"
        file_contents = re.sub(pattern, new, file_contents)
        with open(f"{CURRENT_DIR}/{Top_level_file}", "w") as f:
            f.write(file_contents)
def create_instance(file_name,inst_name):
    global LEGO_DIR, Baseboard_path,library_file

    if inst_name:
        instance = inst_name
    else:
        instance = file_name.replace(".sv", '')
    try:
        data = Extracting_data.get_ranges_from_file(library_file)
        json_file = Top_level_file.replace(".sv", '.json')
        new_inst={instance:data}
        with open (f"{Baseboard_path}/{json_file}",'r') as j:
            jfile=j.read()
            dict_j =json.loads(jfile) #str -> dict
            dict_j.update(new_inst)
            with open (f"{Baseboard_path}/{json_file}",'w') as f:
                new_data=json.dumps(dict_j,indent=4)  #dict -> str
                f.write(new_data)
                copy_file(library_file)
                extract_data(library_file,instance)
    except:
        print("error occured! ")

    #Function to declare a single input and single output combinational block
def comb_block(fileName,output,input):
    code = f"always@* {output} = {input};\n"
    with open(f"{fileName}", "r") as f:
        content = f.read()
    with open(f"{fileName}", "a+") as f:
        if 'endmodule' in content:
            r_end = (f.tell())-9
            x = f.truncate(r_end)
            f.write('\n' + code)
            f.write('\nendmodule')
            print(Fore.GREEN,"combinational block declared successfully",Fore.RESET)

#Function to declare a memory in file
def mem_declaration(fileName,mem_name,wid,dep):
    code = f"reg\t{wid} {mem_name} {dep};"
    with open(f"{fileName}", "r") as f:
        content = f.read()
    with open(f"{fileName}", "a+") as f:
        if 'endmodule' in content:
            r_end = (f.tell())-9
            x = f.truncate(r_end)
            f.write('\n' + code)
            f.write('\nendmodule')
            print(Fore.GREEN,"memory declared successfully",Fore.RESET)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-inst',"--instance",help='Name of file from which instance is taken', type=str, nargs='+')
    parser.add_argument('-m',"--mux",action='store_true')
    parser.add_argument('-r',"--register",action='store_true')
    parser.add_argument('-t,','--topfile',help='Top level file name', type=str)
    parser.add_argument('-n', '--instance_name', help='Name of instance',nargs='+')
   
    parser.add_argument('-i', '--inputs',nargs='+',help='Input port name')
    parser.add_argument('-ir', '--input_ranges',help='Input port range')
    parser.add_argument('-o', '--outputs',help='Output port name',nargs='+')
    parser.add_argument('-or', '--output_ranges',help='Output port range')
      
    parser.add_argument('-sl', '--select_line', type=str, help='Select line')
    
    parser.add_argument('-re', '--reset_signal', type=str, help='Select line')
    parser.add_argument('-en', '--enable_signal', type=str, help='Select line')
    parser.add_argument("-w","--width_of_mem",type=str,help="width of memory",nargs='+')
    parser.add_argument("-dp","--depth_of_mem",type=str,help="depth of memory",nargs='+')
    parser.add_argument("-nm","--name_of_mem",type=str,help="name of memory",nargs='+')

    
    args = parser.parse_args()
    Top_level_file = args.topfile
    
    LEGO_USR_INFO()
    Baseboard_path = os.path.join(LEGO_DIR, 'Baseboard')
    library = os.path.join(LEGO_DIR, 'library')

   
    if args.outputs and args.inputs:
        for args.outputs, args.inputs in zip(args.outputs, args.inputs):
            comb_block(Top_level_file,args.outputs,args.inputs)
            exit()

    if args.name_of_mem and args.width_of_mem and args.depth_of_mem:
        for args.name_of_mem, args.width_of_mem, args.depth_of_mem in zip(args.name_of_mem, args.width_of_mem, args.depth_of_mem):
            mem_declaration(Top_level_file,args.name_of_mem,args.width_of_mem,args.depth_of_mem)
            exit()
    
    if args.instance:
        try:
            if  len(args.instance) == 1 and len(args.instance_name) > 1:  
                for i in args.instance_name:
                    library_file = os.path.join(library, f"{args.instance[0]}")
                    create_instance(args.instance[0],i)
            elif args.instance and args.instance_name:
                for file,name in zip(args.instance,args.instance_name):
                    library_file = os.path.join(library, file)
                    create_instance(file,name)
        except:
            if args.instance:
                for file in args.instance:
                    library_file = os.path.join(library, file)
                    create_instance(file,None)
        exit()
            
    if args.mux:
        if args.inputs and args.outputs and args.select_line:
            generating_mux(args.inputs, args.outputs,args.select_line)
            exit()
        else:
            print("Please provide all the required arguments\n")
            print("plug -m -i <inputs> -ir <input_ranges> -o <output> -or <output_ranges> -sl <select_line> \n")
            exit()
        
    if args.register:
        if args.inputs and args.outputs:
            generate_register(args.inputs, args.input_ranges, args.outputs, args.output_ranges ,args.enable_signal )              
            exit()
        else:
            print("Please provide all the required arguments\n")
            print("plug -r -i <input_signal> -o <output_signal> -en <enable_signal> -ir <input_range> -or <output_range> \n")
            exit()
   