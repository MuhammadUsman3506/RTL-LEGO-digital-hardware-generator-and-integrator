module comp 
#(
	parameter WIDTH = 32
	
)
(
	input 	[WIDTH-1:0] data1,
	output 	reg [WIDTH-1:0] data1,
	output	reg			equal
);

assign	equal = data1 == data2;

endmodule