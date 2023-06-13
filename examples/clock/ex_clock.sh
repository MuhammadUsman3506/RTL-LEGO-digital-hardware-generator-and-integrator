#!/bin/bash
create -f clock.sv -o count_sec count_min count_hrs -or [5:0] [5:0] [5:0] #creating TOP_file clock.sv
add -P TRUE count_max -v "1'b1" "6'd59"		#adding parameters
add -w clr_sec clr_min clr_hrs			#adding wire 1-bit

plug -inst up_counter.sv -n SEC MIN HRS			#plug instance up_counter.sv 

connect -i SEC -ip clk reset count -op clk reset count_sec 	#connect instance 'SEC' ports to Top_file (clock.sv) ports
connect -i MIN -ip clk reset count -op clk reset count_min	#//
connect -i HRS -ip clk reset count -op clk reset count_hrs	#//

connect -i SEC -ip en count_max -P TRUE count_max 		#connect to paramter
connect -i SEC -ip clr -w clr_sec       #connect [SEC][clr] -> wire[clr_sec] 

connect -i MIN -ip en clr -w clr_sec clr_min 
connect -i MIN -ip count_max -P count_max

connect -i HRS -ip en clr -w clr_min clr_hrs
connect -i HRS -ip count_max -P count_max

iverilog -o tb_clock *.sv
vvp tb_clock
gtkwave wave.vcd
