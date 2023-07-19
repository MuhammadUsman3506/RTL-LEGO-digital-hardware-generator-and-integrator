module ALU 
#(
	parameter WIDTH 	= 32,
	parameter OPCODE_WIDTH 		= 2
	
)
(
	input                               clk,
	input        [OPCODE_WIDTH-1:0]			opcode,
	input        [WIDTH-1:0]		op1,
	input        [WIDTH-1:0]		op2,
	output  reg  [WIDTH-1:0]		result
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