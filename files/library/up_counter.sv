module up_counter 
#(
	parameter WIDTH = 6
)
(
	input 					clk,
	input 					reset,
	input				    en,
	input 	    [WIDTH-1:0]	count_max,
	output reg 				clr,
	output reg	[WIDTH-1:0]	count
);

	always@(posedge clk)
		if(reset || clr)	count <= 0;
		else if(en) 		count <= count + 1;
	
	always@* clr = en & (count == count_max);
	
endmodule