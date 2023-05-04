module max_axis
#(
	parameter WIDTH = 32
)
(
	input 					clk,
	input 					reset,
	input				    valid,
	input					ready,
	input	signed 		[WIDTH-1:0]	data,
	output	reg	signed	[WIDTH-1:0]	max	
);
reg en;
always@(posedge clk)
	if(reset)		max <= {1'b1,{WIDTH-1{1'b0}}};
	else if(en) 	max <= data;

always@* en = valid & ready & (data > max);
endmodule