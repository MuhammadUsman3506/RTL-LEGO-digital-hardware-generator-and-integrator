module register #
(
	parameter WIDTH = 32
)
(
	input 				clk,
	input 				reset,
	input 				en,
	input 	[WIDTH-1:0] data_in,
	output 	[WIDTH-1:0] data_out
);

always@(posedge clk)
	if(reset)	data_out <= 0;
	else if(en)	data_out <= data_in;

endmodule