#!/usr/bin/python3
import argparse
import os
import json

from colorama import Fore
import connection

LEGO_DIR=''
Top_level_file=''
found = False     

#################### LAGO ROOT address #######################################
def LEGO_USR_INFO():
        global LEGO_DIR,Top_level_file
        Linux_file_path = os.path.expanduser("~/.LEGO_USR_INFO")
        with open(Linux_file_path, "r") as Shell_file:
            sh_file=Shell_file.readlines()
            LEGO_DIR=sh_file[0].replace("LEGO_DIR=","")+"/files/"
            if Top_level_file:
             if f"TOP_FILE={Top_level_file}\n" in sh_file:
                pass
             else:
                print(f"{Top_level_file} is not present")
                exit()
            else:
                Top_level_file=sh_file[-1]
        LEGO_DIR=LEGO_DIR.replace("\n","")
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
    parser.add_argument('-lp','--local_param',nargs='+',type=str,help='local parameter')
    parser.add_argument('-P', '--parameter',nargs='+',type=str, help='Name of the port')
    
    parser.add_argument('-o', '--instance2',type=str, help='Name of the second instance')
    
    parser.add_argument('-ip', '--input_ports', nargs='+',type=str,help='Input ports of the first instance')
    
    parser.add_argument('-op', '--output_ports', nargs='+', type=str,help='Output ports of the second instance')
    parser.add_argument("-v","--value",type=str,help="value to be assigned to port",nargs='+')
    parser.add_argument('-f', '--filename', help='other top level file',type=str)
    # Parse the arguments
    args = parser.parse_args()
    Top_level_file = args.filename

    LEGO_USR_INFO()
    Baseboard_path = os.path.join(LEGO_DIR,'Baseboard')
    json_file=Top_level_file.replace(".sv",'.json')
    
    with open(f'{Baseboard_path}/{json_file}', 'r') as f:
       data = json.load(f)

    if args.instance1 and args.input_ports and args.value: # connect to value
        for args.input_ports,args.value in zip(args.input_ports,args.value):
            connection.check_json_inst_ports(Top_level_file,args.instance1,args.input_ports,Baseboard_path)
            connection.connect_to_value(Top_level_file,args.instance1,args.input_ports,args.value)
    
    if args.local_param and args.instance1 and args.input_ports:
        for args.local_param ,args.input_ports in zip(args.local_param,args.input_ports):
            connection.check_json(Top_level_file,args.local_param,args.instance1,args.input_ports,Baseboard_path)
            connection.connect_localparam(Top_level_file,args.local_param,args.instance1,args.input_ports)
        exit()

    if args.parameter and args.instance1 and args.input_ports:  # connect to parameter
        for args.parameter,args.input_ports in zip(args.parameter,args.input_ports):
           connection.connect_param(Top_level_file,args.parameter,args.instance1,args.input_ports,Baseboard_path,data)
        exit()
    if args.reg and args.instance1 and args.input_ports: # connect to reg
        for args.reg,args.input_ports in zip(args.reg,args.input_ports):
            connection.connect_to_reg(Top_level_file,args.reg,args.instance1,args.input_ports,Baseboard_path)
        exit()
    if args.wire and args.instance1 and args.input_ports: # connect to wire
        for args.wire,args.input_ports in zip(args.wire,args.input_ports):
            connection.connect_to_wire(Top_level_file,args.wire,args.instance1,args.input_ports,Baseboard_path)
        exit()
    if args.instance1 and args.input_ports and args.instance2 and args.output_ports: # connect to instance
        for args.input_ports, args.output_ports in zip(args.input_ports, args.output_ports):
            connection.connect_instances(Top_level_file,args.instance1,args.input_ports,args.instance2,args.output_ports,Baseboard_path)
        exit() 
    if args.input_ports and args.output_ports and args.instance1: # connect to I/O
        found = connection.check_range_equality(found,Top_level_file,args.instance1, args.input_ports, args.output_ports,data)
        connection.connect_to_IO(found,Top_level_file, args.instance1,args.input_ports, args.output_ports)
        exit()