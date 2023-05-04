#!/usr/bin/python3

import argparse
import os
import json

#################### LAGO ROOT address ######################################
def LAGO_USR_INFO(fname):
	global LAGO_DIR;
	file_path = os.path.expanduser("~/.LAGO_USR_INFO")
	with open(file_path, "a+") as f:
		f.write(f"\nTOP_FILE={fname}") #--> write current toplevel file name
		f.seek(0)
		LAGO_DIR=f.readline().replace("LAGO_DIR=","")+"/files/";
		f.close()
		LAGO_DIR=LAGO_DIR.replace("\n","")
##############################################################################
from colorama import Fore
LAGO_DIR=''
f_name = "Baseboard.sv"
folder_name = 'Baseboard'
######################## setting name of instance & body  ############################
def set_instance_name(f_name, inputs, outputs, input_ranges, output_ranges):
    m_name = f_name.replace(".sv", "")
    if inputs or outputs:
        Body = f"module {m_name} (\ninput\t   \t\tclk,\ninput\t   \t\treset,"
        if inputs:
            i = ""
            for inp, inp_ranges in zip(inputs, input_ranges):
                if inp_ranges == 'None' or inp_ranges == 'none':
                    inpu = f"\ninput\t  \t\t{(i.join(inp))},"
                    Body = Body + inpu
                else:
                    inpu = f"\ninput\t  \t{inp_ranges}\t{(i.join(inp))},"
                    Body = Body + inpu
        if outputs:
            o = ""
            for out, opt_ranges in zip(outputs, output_ranges):
                if opt_ranges == 'None' or opt_ranges == 'none':
                    outu = f"\noutput\twire\t\t{o.join(out)},"
                    Body = Body + outu
                else:
                    outu = f"\noutput\twire\t{opt_ranges}\t{o.join(out)},"
                    Body = Body + outu
        Body = Body.rstrip(",")
        end = "\n\n);\nendmodule"
        Body = Body + end
        print(Body)
    else:
        Body = f'''module {m_name} (\ninput\tlogic\t\tclk,\ninput\tlogic\t\treset\n\n);\nendmodule'''
        print(Body)
    return Body

#########################################################
def name():
    global inputs, outputs, input_ranges,f_name, output_ranges;
    with open(f_name, 'w+') as file:
        file.write(set_instance_name(f_name, inputs,outputs, input_ranges, output_ranges))
        print(Fore.GREEN + f"{f_name} created" + Fore.RESET)
#########################################################
def storing_data_in_Json(f_name, inputs, input_ranges, outputs, output_ranges):

    ports = {}
    ports["clk"] = {"type": "input", "range": "None"}
    ports["reset"] = {"type": "input", "range": "None"}

    if inputs:
        for i, inp in enumerate(inputs):
            if type(inp) == list:
                inp = inp[0]
            ports[inp] = {"type": "input", "range": input_ranges[i]}
    if outputs:
        for j, out in enumerate(outputs):
            if type(out) == list:
                out = out[0]
            ports[out] = {"type": "output", "range": output_ranges[j]}

    return ports


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        default="Baseboard.sv", help='Name of the  top level file')
    parser.add_argument('-i', '--inputs', type=str,
                        nargs='+', help='Input port name')
    parser.add_argument('-ir', '--input_ranges', type=str,
                        nargs='+', help='Input port range')
    parser.add_argument('-o', '--outputs', type=str,
                        nargs='+', help='Output port name')
    parser.add_argument('-or', '--output_ranges',
                        nargs='+', help='Output port range')
    args = parser.parse_args()

    f_name = args.filename
    inputs = args.inputs
    input_ranges = args.input_ranges
    outputs = args.outputs
    output_ranges = args.output_ranges

    LAGO_USR_INFO(f_name)
    name() #->> name function called
    os.chdir(LAGO_DIR)
    try:
        os.chdir(folder_name)
    except:
        os.mkdir(folder_name)
        os.chdir(folder_name)
    ports = storing_data_in_Json(f_name, inputs, input_ranges, outputs, output_ranges)

    jname=f_name.replace(".sv","")
    with open(f"{jname}.json", "w") as jsonfile:
        json_data = {"toplevelfile": f"{f_name}"}
        inpouts={"ports":ports}
        json_data.update(inpouts)
        jsonfile.write(json.dumps(json_data,indent=4))
        
