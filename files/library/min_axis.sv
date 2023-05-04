module min_axis
#(
	parameter WIDTH = 32
)
(
	input 					clk,
	input 					reset,
	input				    valid,
	input					ready,
	input	signed 		[WIDTH-1:0]	data,
	output	reg	signed	[WIDTH-1:0]	min	
);
reg en;
always@(posedge clk)
	if(reset)		min <= {1'b0,{WIDTH-1{1'b1}}};
	else if(en) 	min <= data;

always@* en = valid & ready & (data < min);
endmodule