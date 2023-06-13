module counter 
#(
	parameter WIDTH = 16
)
(
	input 					clk,
	input 					reset,
	input				    en,
	input					clr,
	output reg [WIDTH-1:0]	count
);

	always@(posedge clk)
		if(reset || clr)	count <= 0;
		else if(en) 		count <= count + 1;
	
endmodule