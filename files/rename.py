#!/usr/bin/python3
import os
import json
import argparse
from colorama import Fore

LAGO_DIR=''
Top_level_file=''
#################### LAGO ROOT address #######################################
def LAGO_USR_INFO():
        global LAGO_DIR,Top_level_file
        Linux_file_path = os.path.expanduser("~/.LAGO_USR_INFO")
        with open(Linux_file_path, "r") as Shell_file:
            sh_file=Shell_file.readlines()
            LAGO_DIR=sh_file[0].replace("LAGO_DIR=","")+"/files/";
            if Top_level_file:
             if f"TOP_FILE={Top_level_file}\n" in sh_file:
                pass
             else:
                print(f"{Top_level_file} is not present")
                exit()
            else:
                Top_level_file=sh_file[-1]
        LAGO_DIR=LAGO_DIR.replace("\n","")
        Top_level_file=Top_level_file.replace("TOP_FILE=",'')
##############################################################################
CURRENT_DIR=os.getcwd();

port = 'count_hrs'
# new_name = 'myclock'
def rename_module(fileName,old_name,new_name): 
    new_lines =[]
    with open(fileName,'r+') as f:
        content = f.readlines()
        for line in content:
            if f"{old_name}" in line:
                line = line.split()
                line[-1] = f"{new_name}"
                new_lines.append(' '.join(line) + '\n')
            else:
                new_lines.append(line)
        with open(fileName,'w+') as f:
            f.writelines(new_lines)


def update_module_name(old_module_name, new_module_name):
    with open(f'{Baseboard_path}/{Json_Top_file}.json', 'r') as json_file:
        data_dict = json.load(json_file)
    if old_module_name in data_dict:
        data_dict[new_module_name] = data_dict.pop(old_module_name)
        with open(f'{Baseboard_path}/{Json_Top_file}.json', 'w') as json_file:
            json.dump(data_dict, json_file, indent=4)
        print (Fore.LIGHTGREEN_EX + f"instance {old_module_name} renamed to {new_module_name}." + Fore.RESET)
    else:
        print (Fore.RED + f"instance {old_module_name} not found." + Fore.RESET)
    
def rename_port(fileName,old_port_name,new_port_name):
    new_lines = []
    with open(fileName,"r+") as f:
        content = f.readlines()
        for line in content:
            if f"{old_port_name}" in line and ("input" in line or "output" in line):
                line = line.split()
                if line[-1].endswith(','):
                    line[-1] = f"{new_port_name},"
                    new_lines.append(' '.join(line) + '\n')
                else:
                    line[-1] = f"{new_port_name}"
                    new_lines.append(' '.join(line) + '\n')
            else:
                new_lines.append(line)
        with open("clock.sv","w+") as f:
            f.writelines(new_lines)
            

def update_port_name(old_port_name, new_port_name):
    with open(f"{Baseboard_path}/{Json_Top_file}.json", 'r') as json_file:
        data_dict = json.load(json_file)
        if old_port_name in data_dict['clock']['ports']:
            data_dict['clock']['ports'][new_port_name] = data_dict['clock']['ports'].pop(old_port_name)
            with open(f"{Baseboard_path}/{Json_Top_file}.json", 'w') as outfile:
                json.dump(data_dict, outfile, indent=4)
            print(Fore.LIGHTGREEN_EX + f"Successfully updated port name from {old_port_name} to {new_port_name}" + Fore.RESET)
        else:
            print(Fore.LIGHTGREEN_EX + f"Port with name {old_port_name} not found in file" + Fore.RESET)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f','--file_name',type=str, help='name of file where instance or port need to be renamed')
    parser.add_argument('-e','--earlier',type=str, help='name of file where instance or port need to be renamed')
    parser.add_argument('-n','--new_name',type=str, help='name of file where instance or port need to be renamed')

    parser.add_argument('-p','--port',type=str, help='name of port need to be renamed')
    parser.add_argument('-i','--instance',type=str, help='name of instance need to be renamed')

    args = parser.parse_args()
    Top_level_file = args.file_name
    erlier_name = args.earlier
    new_name = args.new_name
    LAGO_USR_INFO()
    Json_Top_file=Top_level_file.replace(".sv",'')
    Baseboard_path = os.path.join(LAGO_DIR,'Baseboard')


    if args.port:
        rename_port(Top_level_file,erlier_name,new_name)
        update_port_name(erlier_name,new_name)
    if args.instance:
        update_module_name(erlier_name,new_name)
        rename_module(Top_level_file,erlier_name,new_name)
    else:
        print("Please provide the arguments")
        print("Use -h or --help for more information")
        exit()
