module bram_dual			
#(
	parameter RAM_WIDTH 		= 32,					
	parameter RAM_DEPTH 		= 512,                  
	parameter RAM_PERFORMANCE 	= "HIGH_PERFORMANCE",   
	parameter INIT_FILE 		= "",					
	parameter INIT_START_ADDR 	= 0,
	parameter INIT_END_ADDR		= RAM_DEPTH-1
)
(
input	[clogb2(RAM_DEPTH-1)-1:0] addra,  	
input	[clogb2(RAM_DEPTH-1)-1:0] addrb, 
input	[RAM_WIDTH-1:0] dina,           	
input	[RAM_WIDTH-1:0] dinb,           	
input	clka,                           	
input	clkb,                           	
input	wea,                            	
input	web,                            	
input	ena,                            	
input	enb,                            	
input	rsta,                           	
input	rstb,                           	
input	regcea,                         	
input	regceb,                         	
output reg	[RAM_WIDTH-1:0] douta,          	
output	reg [RAM_WIDTH-1:0] doutb	          	
);
  reg [RAM_WIDTH-1:0] ram_name [RAM_DEPTH-1:0];
  reg [RAM_WIDTH-1:0] ram_data_a = {RAM_WIDTH{1'b0}};
  reg [RAM_WIDTH-1:0] ram_data_b = {RAM_WIDTH{1'b0}};

  

endmodule							