#!/usr/bin/python3
import argparse
import os
import json

from colorama import Fore
import connection

LAGO_DIR=''
Top_level_file=''
found = False     

#################### LAGO ROOT address #######################################
def LAGO_USR_INFO():
        global LAGO_DIR,Top_level_file
        Linux_file_path = os.path.expanduser("~/.LAGO_USR_INFO")
        with open(Linux_file_path, "r") as Shell_file:
            sh_file=Shell_file.readlines()
            LAGO_DIR=sh_file[0].replace("LAGO_DIR=","")+"/files/"
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


if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description='Change lines in instances in  file')
    # Add arguments for the instances and ports
    parser.add_argument('-i', '--instance1',type=str,help='Name of the first instance')
    parser.add_argument('-r', '--reg',nargs='+',type=str, help='Name of the reg')
    parser.add_argument('-w', '--wire',nargs='+',type=str, help='Name of the wire')
    
    parser.add_argument('-P', '--parameter',nargs='+',type=str, help='Name of the port')
    
    parser.add_argument('-o', '--instance2',type=str, help='Name of the second instance')
    
    parser.add_argument('-ip', '--input_ports', nargs='+',type=str,help='Input ports of the first instance')
    
    parser.add_argument('-op', '--output_ports', nargs='+', type=str,help='Output ports of the second instance')
    
    parser.add_argument('-f', '--filename', help='other top level file',type=str)
    # Parse the arguments
    args = parser.parse_args()
    Top_level_file = args.filename

    LAGO_USR_INFO()
    Baseboard_path = os.path.join(LAGO_DIR,'Baseboard')
    json_file=Top_level_file.replace(".sv",'.json')
    
    with open(f'{Baseboard_path}/{json_file}', 'r') as f:
       data = json.load(f)
    
    if args.parameter and args.instance1 and args.input_ports:
        for args.parameter,args.input_ports in zip(args.parameter,args.input_ports):
           connection.connect_param(Top_level_file,args.parameter,args.instance1,args.input_ports,Baseboard_path,data)
        exit()
    if args.reg and args.instance1 and args.input_ports:
        for args.reg,args.input_ports in zip(args.reg,args.input_ports):
            connection.connect_to_reg(Top_level_file,args.reg,args.instance1,args.input_ports,Baseboard_path)
        exit()
    if args.wire and args.instance1 and args.input_ports:
        for args.wire,args.input_ports in zip(args.wire,args.input_ports):
            connection.connect_to_wire(Top_level_file,args.wire,args.instance1,args.input_ports,Baseboard_path)
        exit()
    if args.instance1 and args.input_ports and args.instance2 and args.output_ports:
        for args.input_ports, args.output_ports in zip(args.input_ports, args.output_ports):
            connection.connect_instances(Top_level_file,args.instance1,args.input_ports,args.instance2,args.output_ports,Baseboard_path)
        exit() 
    if args.input_ports and args.output_ports and args.instance1: # connect to I/O
        found = connection.check_range_equality(found,Top_level_file,args.instance1, args.input_ports, args.output_ports,data)
        connection.connect_to_IO(found,Top_level_file, args.instance1,args.input_ports, args.output_ports)
        exit()
    else:
        print("Please enter the correct arguments")
        exit()