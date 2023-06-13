#!/usr/bin/python3
from colorama import Fore
import re
import os
import argparse
import json
import fileinput

LEGO_DIR=''
Top_level_file=''
#################### LAGO ROOT address #######################################
def LEGO_USR_INFO():
        global LEGO_DIR,Top_level_file
        Linux_file_path = os.path.expanduser("~/.LEGO_USR_INFO")
        with open(Linux_file_path, "r") as Shell_file:
            sh_file=Shell_file.readlines()
            LEGO_DIR=sh_file[0].replace("LEGO_DIR=","")+"/files/";
            if Top_level_file:
             if f"TOP_FILE={Top_level_file}" in sh_file:
                pass
             else:
                print(f"{Top_level_file} is not present")
                exit()
            else:
                Top_level_file=sh_file[-1]
        LEGO_DIR=LEGO_DIR.replace("\n","")
        Top_level_file=Top_level_file.replace("TOP_FILE=",'')
##############################################################################
CURRENT_DIR=os.getcwd();

def json_delete_port(filename,port_name):
    module_name = filename.replace(".sv","")
    with open(f"{Baseboard_path}/{Json_Top_file}.json",'r') as f:
        data = json.load(f)

    # Delete the "clk" port from the "ports" object within the "Baseboard" object
    if module_name in data and "ports" in data[module_name] and f"{port_name}" in data[module_name]["ports"]:
        del data[module_name]["ports"][port_name]

    # Save the updated JSON file
    with open(f"{Baseboard_path}/{Json_Top_file}.json",'w') as f:
        json.dump(data, f, indent=4)


def delete_port(filename, port_name):
    # Remove the line containing the string and print the previous line
    new_lines = []
    prev_line = ""
    deleted = False  # flag to track if the port has been deleted

    for line in fileinput.input(filename, inplace=True):
        if port_name in line and not ',' in line:
            line = prev_line.rstrip(',\n') + "\n"
            new_lines[-1] = line
            deleted = True
        elif port_name in line and ",":
            line = prev_line.rstrip(',\n') + "\n"
            deleted = True
        else:
            new_lines.append(line)
            prev_line = line
    if deleted:  # print message only if port is deleted
        print(Fore.GREEN +
              f"Port {port_name} has been deleted successfully." + Fore.RESET)
    else:
        print(Fore.RED + "Port not found." + Fore.RESET)

    with open(filename, 'w') as file:
        file.writelines(new_lines)
    fileinput.close()


def json_delete_instance(instance):
    with open(f"{Baseboard_path}/{Json_Top_file}.json",'r') as f:
        data = json.load(f)
    # Check if the object with the specified name exists and delete it if it does
    if instance in data:
        del data[instance]

    # Save the updated JSON file
    with open(f"{Baseboard_path}/{Json_Top_file}.json", 'w') as f:
        json.dump(data, f, indent=4)


def delete_instance(fileName, instance):
    with open(f"{fileName}", 'r') as f:
        content = f.read()
    pattern = rf'.*{instance}\s*(([\s\S]*?));'
    match = re.search(pattern, content)
    if match:
        block = match.group()
        block = block.replace(block, '')
        content = re.sub(pattern, block, content)
        print(Fore.GREEN +
              f"instance {instance} has been deleted successfully." + Fore.RESET)
    else:
        print(Fore.RED + f"instance {instance} is not found." + Fore.RESET)
    with open(fileName, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', "--file_name", help="Name of file where port or instance has to be removed")
    parser.add_argument(
        '-p', "--port", help="Name of file of port which needs to be removed")

    parser.add_argument(
        '-i', "--instance", help="Name of instances which needs to be removed")

    arg = parser.parse_args()
    Top_level_file = arg.file_name

    LEGO_USR_INFO()
    Json_Top_file=Top_level_file.replace(".sv",'')
    Baseboard_path = os.path.join(LEGO_DIR,'Baseboard')

    if arg.port:
        port = arg.port
        json_delete_port(Top_level_file,port)
        delete_port(Top_level_file, port)
    if arg.instance:
        instance = arg.instance
        delete_instance(Top_level_file, instance)
        json_delete_instance(instance)
