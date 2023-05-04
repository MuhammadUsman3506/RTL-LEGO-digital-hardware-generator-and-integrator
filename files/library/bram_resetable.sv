`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    14:01:31 09/28/2013 
// Design Name: 
// Module Name:    bram_resetable 
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
module bram_resetable
	#(
		parameter RAM_WIDTH 	= 16,
		parameter RST_DEPTH_A 	= 16,
		parameter RST_DEPTH_B 	= 16,
		parameter B_ADDR_OFFSET = 256
	)
	(
		input 			clka,
		input 			rsta,
		input 			wea,
		input 	[8:0] 	addra,
		input 	[RAM_WIDTH - 1:0] 	dina,
		output 	[RAM_WIDTH - 1:0] 	douta,
		
		input 			clkb,
		input 			rstb,
		input 			web,
		input 	[8:0]	addrb,
		input 	[RAM_WIDTH - 1:0]	dinb,
		output 	[RAM_WIDTH - 1:0]	doutb
    );

reg			rsta_ram;
reg			rstb_ram;

always@(posedge clka)
	if(rsta)
		rsta_ram <= #1 1;
	else if((addra == RST_DEPTH_A-1) & wea)
		rsta_ram <= #1 0;
	
always@(posedge clkb)
	if(rstb)		 						
		rstb_ram <= #1 1;
	else if(addrb == (RST_DEPTH_B-1+B_ADDR_OFFSET) & web)
		rstb_ram <= #1 0;

bram bram_inst(
		.clka	(clka), 
		.wea	(wea), 
		.addra	(addra), 
		.dina	(dina), 
		.douta	(douta), 
		.clkb	(clkb), 
		.web	(web), 
		.addrb	(addrb), 
		.dinb	(dinb), 
		.doutb	(doutb),
		.rsta	(rsta_ram | rsta),
		.rstb	(rstb_ram | rstb)
	);
	
endmodule
