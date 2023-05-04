#!/usr/bin/python3
import json
import re
from colorama import Fore
Success = False
def update_ranges(file_name,port_name,new_range): 
    with open(file_name, "r") as f:
        lines = f.readlines()
        found = False
        for i, line in enumerate(lines):
            if re.search(fr"\[(\d.*:\d.*)\].*\b{port_name}\b", line):
                found = True
                old_range = re.search(fr'\[(\d.*:\d.*)\]', line).group()
                if old_range == new_range:
                    print(Fore.RED + f"Error: Port status is already {new_range}" + Fore.RESET)
                    Success = False
                    return
                else:
                    updated_line = re.sub(fr"\[(\d.*:\d.*)\]", f"{new_range}", line)
                    lines[i] = updated_line
                    with open(file_name, "w") as f_out:
                        f_out.writelines(lines)
                    print(Fore.LIGHTGREEN_EX + f"Range for {port_name} port updated from {old_range} to {new_range}" + Fore.RESET)
                    Success = True
                    return Success
        if not found:
            print(Fore.RED + f"Error: {port_name} or range not found in {file_name}." + Fore.RESET)
            Success = False
            return Success


def update_ranges_json(file_name,port_name,new_range, Baseboard_path):
    Json_Top_file = file_name.replace(".sv", "")      
    with open(f'{Baseboard_path}/{Json_Top_file}.json', 'r') as f:
        data = json.load(f)
        data['ports'][port_name]['range'] = new_range
        with open(f"{Baseboard_path}/{Json_Top_file}.json", 'w') as outfile:
            json.dump(data, outfile, indent=4)


def change_IO_status(file_name,port_name, new_status):
    with open(file_name, "r") as f:
        lines = f.readlines()
        found = False
        for i, line in enumerate(lines):
            if re.search(fr'\b(input|output)\b.*\b{port_name}\b', line):
                found = True
                port_type = re.search(fr'\b(input|output)\b', line).group()
                if port_type == new_status:
                    print(Fore.RED + f"Error: Port status is already {new_status}" + Fore.RESET)
                    Success = False
                    return Success
                else:
                    lines[i] = re.sub(fr'\b{port_type}\b', new_status, line)
                    with open(file_name, "w") as f:
                        f.writelines(lines)
                    print(Fore.LIGHTGREEN_EX +
                          f"Port status of {port_name} changed from {port_type} to {new_status}." + Fore.RESET)
                    Success = True
                    return Success
        if not found:
            print(Fore.RED + f"Error: {port_name} not found in {file_name}." + Fore.RESET)


def change_IO_status_json(file_name,port_name, new_status,Baseboard_path):
    Json_Top_file = file_name.replace(".sv", "")
    with open(f'{Baseboard_path}/{Json_Top_file}.json', 'r') as f:
        data = json.load(f)
        data['ports'][port_name]['type'] = new_status
        with open(f"{Baseboard_path}/{Json_Top_file}.json", 'w') as outfile:
            json.dump(data, outfile, indent=4)