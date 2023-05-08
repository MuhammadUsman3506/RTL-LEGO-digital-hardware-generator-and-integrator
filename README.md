# RTL LAGO

## A Digital Hardware Generator and Integrator

The aim of this project is to create a framework that can be used to generate and intergrate RTL components. User should be able to connect components from a library of generic RTL components and existing IP blocks to create Digital Hardware.

Here is brief discription of files that how to proceed them

## [./install.sh](install.sh)

install will create commands (create/ plug/ connect) in your terminal. You can use these commands to create project, create instance and connect instances.

Here is the command to run install file

```bash
  ./install.sh
```

After running this file you can use following commands in your terminal

To create Top level file

```bash
create 
```

To veiw avalible files in library

```bash
list_lago 
```

To create instances of library files in your Toplevel file and plug registers,mux etc

```bash
plug 
```

Use add to add reg/wire/ranges etc

```bash
add 
```

Use connect to connect ports of instances

```bash
connect 
```

Here is the brief discription of commands

## create

This command will create a file with name given in argument. If you don't give any argument then it will create a file with name **Baseboard.sv** with defult **clk** and **reset** inputs.

```bash
create -f filename
```

if you want to add more inputs and outputs in the file use following commands

```bash
create -f filename -i inputs -o clear result -ir None [5:0] -or None [3:0]
```

## list_lago

This command will list all the files that are present in the library.

```bash
list_lago
```

To view the content of a file use following command

```bash
list_lago -f filename
```

To edit a file use following command

```bash
list_lago -e filename
```

## plug

plug command can create instance of a file. You can use this command to create instance of a file that you have created using create command or you can use this command to create instance of a file that is already present in the library.

By default it will create instance of a file with its own name you can use different name by ***-i*** argument. and will create instance in current or recesnt created .sv file (make sure you are in that .sv file Dir) To plug instance in older (other then previous) ure ***-t*** Topfile name

```bash
plug -inst file_name -n instance_name 
```

plug command can also add comments like ***register, mux*** to the Top file.

To add ***register***  use following command

```bash
plug -r <register> -i <inputs> -o <outputs> -en <enable>
```

To add ***mux*** use following command

```bash
plug -m <mux> -i <inputs> -o <outputs> -s <select>
```

## add

To add Extra input/output port ***port***,***parameter***,***wire***,***reg*** or ***change-range*** of input/output or chnage the status of input/output
use add command

To add ***port***  use following command

```bash
add -p <port> -i <inputs> -o <outputs>
```

To add ***Parameter*** use following command

```bash
add -P <Parameter> -v <value>
```

use '' to add string value

```bash
add -P <parameter> -v '"HIGH_PERFORMANCE"'
```

will add ***parameter  = "HIGH_PERFORMANCE"*** to the file

To add local ***parameter*** use following command

```bash
add -lp <localparam> -v <value> -inst <instance>
```

To add ***wire*** use following command

```bash
add -w <wire> -rn <range>
```

To add ***reg*** use following command

```bash
add -r <reg> -rn <range>
```

To change the ***range*** of input/output use following command

```bash
add -c <change> range -pr <port_name> -nr <new_range>
```

to change the ***status*** of input/output use following command

```bash
add -c <change> port -pr <port_name> -ns <new_status>
```

## connect

After creating instances you can connect them using connect command. You can connect instances of files that you have created using create command or you can connect instances of files that are already present in the library.

***connect two instances***

```bash
connect -i <instance1> -ip <input_ports> -o <instance2> -op <output_ports>
```

***connect port to parameters***

```bash
connect -P <parameters> -i <instance> -ip <input_port>
```

***connect port to wire***

```bash
connect -w <wire> -i <instance> -ip <input_port>
```

***connect port to reg***

```bash
connect -r <reg> -i <instance> -ip <input_port>
```

***connect port to input/output***

```bash
connect -i <instance1> -ip <input_port> -op <output_port>
```

## delete

you can delete instance or port or parameter or wire or reg using delete command

***delete instance***

```bash
delete -i <instance>
```

***delete port***

```bash
delete -p <port> -i <instance>
```

## [./uninstall.sh](uninstall.sh)

To uninstall the commands run ./uninstall.sh file

```bash
./uninstall.sh
```

## Usage/Examples

To run Examples, Please look into [examples](examples). eg To run ex_clock.sh file

```bash
./ex_clock.sh
```

## Documentation

To undestand complete and Usage Please look into [commands](commands)

## 🚀 About Me

I'm Student of Electrical Engineering...
