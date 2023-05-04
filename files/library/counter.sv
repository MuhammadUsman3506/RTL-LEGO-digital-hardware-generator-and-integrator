module counter 
#(
	parameter WIDTH = 16
	parameter R_WIDTH = 17
	parameter X_WIDTH = 18
	parameter Y_WIDTH = 19
)
(
	input 					clk,
	input 		[WIDTH-1:1]	reset,
	input				    en,
	input		[R_WIDTH-1:0]			clr,
	output reg [X_WIDTH-1:0]	count
);

	always@(posedge clk)
		if(reset || clr)	count <= 0;
		else if(en) 		count <= count + 1;
	
endmodule