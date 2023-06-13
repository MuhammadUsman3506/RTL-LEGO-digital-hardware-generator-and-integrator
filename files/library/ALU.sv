module ALU 
#(
	parameter RAM_WIDTH 	= 32,
	parameter WIDTH 		= 2
	
)
(
	input                               clk,
	input        [WIDTH-1:0]			opcode,
	input        [RAM_WIDTH-1:0]		op1,
	input        [RAM_WIDTH-1:0]		op2,
	output  reg  [RAM_WIDTH-1:0]		result
);

parameter ADD  = 'd0;
parameter SUB  = 'd1;
parameter MUL  = 'd2;
parameter NAND = 'd3;

always@*
	case(opcode[1:0])
	ADD : result =   op1 + op2;
	SUB : result =   op1 - op2;
	MUL : result =   op1 * op2;
	NAND: result = ~(op1 & op2);
	endcase
	
endmodule