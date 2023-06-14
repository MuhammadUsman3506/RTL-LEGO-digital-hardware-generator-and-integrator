#!/bin/bash
create -f processor.sv	#create file
add -P WIDTH RAM_WIDTH RAM_ADDR_BITS PROG_FILE PROG_START_ADDR PROG_END_ADDR DATA_FILE DATA_START_ADDR DATA_END_ADDR -v "9" "32" "9" \"'program.hex'\" "0" "8" \"'data_file.txt'\" "0" "5" #adding parameters
add -w opcode -rn "[4:0]" # add reg 
add -w instr reg_data_in alu_out dram_data_out op2 op1 prog_cnt ctl3 ctl2 ctl1 -rn "[RAM_WIDTH-1:0]" "[RAM_WIDTH-1:0]" "[RAM_WIDTH-1:0]" "[RAM_WIDTH-1:0]" "[RAM_WIDTH-1:0]" "[RAM_WIDTH-1:0]" "[WIDTH-1:0]" "None" "None" "None"  #adding wire 1-bit 
add -lp LW SW  -v "5'd4" "5'd5"  # LOCAL PARAM
###################### up_counter ########################
plug -inst up_counter.sv -n up_counter_inst	#plug instance up_counter.sv
connect -i up_counter_inst -ip clk reset -op clk reset # Top_level_file inputs/outputs to instance ports
connect -w prog_cnt -i up_counter_inst -ip count # connect : wire to instance ports
add -nw WIDTH -ow WIDTH -inst up_counter_inst #FDJF
connect -w prog_cnt -i up_counter_inst -ip count # connect wire into instance port
####################### Prog_mem #########################
plug -inst prg_mem.sv -n prg_mem_inst	#plug instance prg_mem_inst
add -ow RAM_WIDTH RAM_ADDR_BITS PROG_FILE PROG_START_ADDR PROG_END_ADDR -nw RAM_WIDTH RAM_ADDR_BITS PROG_FILE PROG_START_ADDR PROG_END_ADDR -inst prg_mem_inst
connect -i prg_mem_inst -ip clock -op clk # Top_level_file inputs/outputs to instance ports
connect -w prog_cnt -i prg_mem_inst -ip address # connect : wire to instance ports
connect -w instr -i prg_mem_inst -ip out_data # connect : wire to instance ports
#connect -lp single_bit1 single_bit0 zero -i prg_mem_inst -ip ram_enable write_enable in_data # local parameter to instance
connect -v "1'b1" "1'b0" "0" -i prg_mem_inst -ip ram_enable write_enable in_data   # value connect to the instance prg_mem_inst 
###################### reg_file ###########################
plug -inst regfile.sv -n regfile_inst       #plug instance regfile_inst
add -ow WIDTH_ADDR WIDTH_DATA -nw DATA_END_ADDR RAM_WIDTH -inst regfile_inst # add parameter of instance 
connect -i regfile_inst -ip clk -op clk # Top_level_file inputs/outputs to instance ports
connect -w op1 op2 ctl1 reg_data_in -i regfile_inst -ip rd_data1 rd_data2 wr_en wr_data # connect : wire to instance ports
#connect -lp instr_addr1 instr_addr2 wr_addr_instr -i regfile_inst -ip rd_addr1 rd_addr2 wr_addr # local parameter to instance
connect -v "instr[21:17]" "instr[16:12]" "instr[26:22]" -i regfile_inst -ip rd_addr1 rd_addr2 wr_addr # constant value connect to the instance 
######################### comb block    ####################################################
###plug -i "instr[31:27]" -o "opcode" ## plug combination block
######################### ALU #####################################
plug -inst ALU.sv -n ALU_inst                 #plug instance  ALU_inst
add -nw RAM_WIDTH -ow RAM_WIDTH -inst ALU_inst #
connect -i ALU_inst -ip clk -op clk # Top_level_file inputs/outputs to instance ports
connect -w op1 op2 alu_out -i ALU_inst -ip op1 op2 result # connect : wire to instance ports
#connect -lp opcode_2bit -i ALU_inst -ip opcode #
connect -v "opcode[1:0]" -i ALU_inst -ip opcode # constant value connect to the instance
######################## Mux #################################
plug -inst Mux.sv -n Mux_inst                #plug instance Mux_inst
add -nw RAM_WIDTH -ow RAM_WIDTH -inst Mux_inst #
connect -w ctl2 alu_out dram_data_out reg_data_in -i Mux_inst -ip s_l in0 in1 out  # connect : wire to instance ports
####################### data_mem  #############################
plug -inst data_mem.sv -n data_mem_inst	#plug instance data_mem_inst
add -ow RAM_WIDTH RAM_ADDR_BITS DATA_FILE INIT_START_ADDR  INIT_END_ADDR -nw RAM_WIDTH RAM_ADDR_BITS DATA_FILE DATA_START_ADDR DATA_END_ADDR -inst data_mem_inst
connect -i data_mem_inst -ip clock -op clk # Top_level_file inputs/outputs to instance ports
connect -w ctl3 -i data_mem_inst -ip write_enable # gdsfg
connect -w op1 -i data_mem_inst -ip in_data # jghjj
connect -w dram_data_out -i data_mem_inst -ip out_data # jgjhg
#connect -w ctl3 op1 dram_data_out -i data_mem_inst -ip write_enable in_data out_data #--> this is commented b/c this is already done by previos CMDS # connect : wire to instance ports
#connect -lp single_bit1 datamem_addr_instr -i data_mem_inst -ip ram_enable address #
connect -v "1'b1" "instr[8:0]" -i data_mem_inst -ip ram_enable address # constant value connect to the instance
########################### not_gate ############################
plug -inst not_gate.sv -n inst_not_gate	#plug instance inst_not_gate
connect -w ctl3 ctl1 -i inst_not_gate -ip in out # wire to instance 
############################ comparator_inst  ################
plug -inst comparator.sv -n inst_comparator	#plug instance inst_comparator
add -nw DATA_END_ADDR  -ow WIDTH -inst inst_comparator #
connect -w opcode -i inst_comparator -ip in0 # register to instance 
connect -w ctl2 -i inst_comparator -ip out # wire to isnstance
connect -lp LW -i inst_comparator -ip in1 # local parameter to instance
################################## comparator_inst1  ################
plug -inst comparator.sv -n inst1_comparator	#plug inst1_comparator
add -nw DATA_END_ADDR -ow  WIDTH -inst inst1_comparator # 
connect -w opcode -i inst1_comparator -ip in0 #  register to instance 
connect -w ctl3 -i inst1_comparator -ip out # wire to isnstance
connect -lp SW -i inst1_comparator -ip in1 # local parameter to instance
########################  comb_block ####################### comb_block.sv
plug -inst comb_block.sv -n inst_comb_block	#plug inst_comb_block
add -nw DATA_END_ADDR -ow  WIDTH -inst inst_comb_block # gdfd
##connect -r opcode -i inst_comb_block -ip out # wire to isnstance
connect -v "instr[31:27]" "opcode" -i inst_comb_block -ip in out # constant value connect to the instance


