module comp_eq #
(
	parameter WIDTH = 32
)
(
	input 	[WIDTH-1:0] data1,
	output 	[WIDTH-1:0] data1,
	output				equal,
);

assign	equal = data1 == data2;

endmodule