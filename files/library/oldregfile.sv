module regesterfile
(
	input [4:0]	wraddr,
	input 		wrEn,
	input [31:0]wrData,
	input [4:0]	Rdaddr1,
	input [4:0]	Rdaddr2,
	output reg [31:0]	RdData1,
	output reg [31:0]	RdData2
);

reg [31:0] regs [31:0];
always@(posedge clk)
	if (wrEn) regs[wraddr] <= wrData;
	
assign RdData1 = regs[Rdaddr1];
assign Rdaddr2 = regs[Rdaddr2];
endmodule