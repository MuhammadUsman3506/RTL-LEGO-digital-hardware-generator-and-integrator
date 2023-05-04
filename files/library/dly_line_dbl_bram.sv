`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    18:37:54 09/25/2012 
// Design Name: 
// Module Name:    dly_line_dbl_bram 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module dly_line_dbl_bram
	#(	  
		parameter	WIDTH 		= 32,	// Not configurable
		parameter	DEPTH1		= 16,
		parameter	DEPTH2		= 64,
		parameter 	RST_DEPTH_A = 16,
		parameter 	RST_DEPTH_B = 64
	)
	(  
	input								clk,
	input								reset,
	input		signed	[WIDTH-1:0]		data_in1,
	input								valid_in1,
	input		signed	[WIDTH-1:0]		data_in2,
	input								valid_in2,
		
	output		signed	[WIDTH-1:0]		data_out1,
	output		signed	[WIDTH-1:0]		data_out2
    );
	
reg	[7:0]	addr1;
reg	[7:0]	addr2;
reg clr_addr1;
reg clr_addr2;
always@(posedge clk)
	if(reset || clr_addr1)	addr1 <= #1 0;
	else if(valid_in1)		addr1 <= #1 addr1+1;
	
always@* clr_addr1 = (addr1 == (DEPTH1-1)) & valid_in1;	

always@(posedge clk)
	if(reset || clr_addr2)	addr2 <= #1 0;
	else if(valid_in2)		addr2 <= #1 addr2+1;

always@* clr_addr2 = (addr2 == (DEPTH2-1)) & valid_in2;	

bram_resetable 
		#(
		.RST_DEPTH_A	(RST_DEPTH_A),
		.RST_DEPTH_B	(RST_DEPTH_B),
		.B_ADDR_OFFSET	(256)
		)

dual_port_bram(

	.rsta		(reset),
	.rstb		(reset),
	
	.clka		(clk),
	.wea		(valid_in1),
	.addra		({1'b0,addr1}),
	.dina		(data_in1),
	.douta		(data_out1),
	
	.clkb		(clk),
	.web		(valid_in2),
	.addrb		({1'b1,addr2}),
	.dinb		(data_in2),
	.doutb		(data_out2)
	);

endmodule
