# A Simple Processor

This is verilog code of a simple processor that supports four ALU operations i.e. ADD, SUB, MULT and NAND. And supports two memory instructions load (LW) and Store (SW). Below is instruction format and hardware design on the processor.

Program memory is initialized with program.hex file and data memory is intialized with data_file.txt. Currently these files implement a simple operation of


A = B + C*D


where A, B, C and D are stored in data memory locations 0 to 3. B, C and D have values 200, 10 and 2 respectively. Hence at the last SW instruction 220 is written at memory address 0.
