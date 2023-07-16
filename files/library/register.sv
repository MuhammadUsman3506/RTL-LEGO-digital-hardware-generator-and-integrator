module register 
#(
	parameter WIDTH = 4,
	parameter Height = 4
)
(
	input 				clk,
	input 				reset,
	input 			en,
	input 	    [Height-1:0] data_in,
	output reg	[WIDTH-1:0] data_out
);

always@(posedge clk)
	if(reset)	data_out <= 0;
	else if(en)	data_out <= data_in;

endmodule