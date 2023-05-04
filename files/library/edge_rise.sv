module edge_rise 
(
	input 		clk,
	input 		reset,
	input 		in,
	output reg	out
);

reg in_r;
always@(posedge clk)
	if(reset)  in_r <= 0;
	else   	   in_r <= in;

always@* out = in & ~in_r;

endmodule