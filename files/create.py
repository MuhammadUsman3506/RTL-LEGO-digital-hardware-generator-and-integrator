#!/usr/bin/python3
import argparse
import os
import json

#################### LAGO ROOT address ######################################
def LEGO_USR_INFO(fname):
	global LEGO_DIR
	file_path = os.path.expanduser("~/.LEGO_USR_INFO")
	with open(file_path, "a+") as f:
		f.write(f"\nTOP_FILE={fname}")
		f.seek(0)
		LEGO_DIR=f.readline().replace("LEGO_DIR=","")+"/files/"
		f.close()
		LEGO_DIR=LEGO_DIR.replace("\n","")
##############################################################################
from colorama import Fore
LEGO_DIR=''
f_name = "Baseboard.sv"
folder_name = 'Baseboard'
######################## setting name of instance & body  ############################
def set_instance_name(f_name, inputs, outputs, input_ranges, output_ranges):
    m_name = f_name.replace(".sv", "")
    if inputs or outputs:
        Body = f"module {m_name} (\ninput\t   \t\tclk,\ninput\t   \t\treset,"
        if inputs != "None":
            print("inputs",inputs)
            i = ""
            if input_ranges in ['None', 'none']:
                for inp in inputs:
                    inpu = f"\ninput\t  \t\t{(i.join(inp))},"
                    Body = Body + inpu
            else:
                for inp, inp_ranges in zip(inputs, input_ranges):
                    inpu = f"\ninput\t  \t{inp_ranges}\t{(i.join(inp))},"
                    Body = Body + inpu
        if outputs != "None":
            o = ""
            if output_ranges in ['None', 'none']:
                for out in outputs:
                    outu = f"\noutput\twire\t\t{o.join(out)},"
                    Body = Body + outu
            else:
                for out, opt_ranges in zip(outputs, output_ranges):
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
    
    if input_ranges == 'None' and inputs != "None":
        input_ranges = ['None' for i in range(len(inputs))]

    if output_ranges == 'None' and outputs != "None":
        output_ranges = ['None' for i in range(len(outputs))]


    if inputs != "None":
        for i, inp in enumerate(inputs):
            if type(inp) == list:
                inp = inp[0]
            ports[inp] = {"type": "input", "range": input_ranges[i]}
    if outputs != "None":
        for j, out in enumerate(outputs):
            if type(out) == list:
                out = out[0]
            ports[out] = {"type": "output", "range": output_ranges[j]}

    return ports


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',default="Baseboard.sv", help='Name of the  top level file')
    parser.add_argument('-i', '--inputs', type=str,nargs='+', help='Input port name',default='None')
    parser.add_argument('-ir', '--input_ranges', type=str, nargs='+', help='Input port range',default='None')
    parser.add_argument('-o', '--outputs', type=str,nargs='+', help='Output port name',default='None')
    parser.add_argument('-or', '--output_ranges',nargs='+', help='Output port range',default='None')
    args = parser.parse_args()

    f_name = args.filename
    inputs = args.inputs
    input_ranges = args.input_ranges
    outputs = args.outputs
    output_ranges = args.output_ranges

    LEGO_USR_INFO(f_name)
    name()
    os.chdir(LEGO_DIR)
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
        
