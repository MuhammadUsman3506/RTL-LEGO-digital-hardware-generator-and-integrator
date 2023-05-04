module up_dn_counter
	#(	  
		parameter	WIDTH 		= 32,
		parameter	WIDTH 		= 32,
		parameter	RESET_VALUE	= 0
	)
	(
	input       			clk,
	input       			reset,
	input       			incr,
	input       			decr,
	output reg [WIDTH-1:0]	count
	);

reg       		enable;
reg [WIDTH-1:0] mux_out;

always@(*)
   enable = incr ^ decr;

always@(*)
begin
   case(increment)
   1'b0: mux_out = count-1;
   1'b1: mux_out = count+1;
   endcase
end

always@(posedge clk)
	if(reset)   	count <= RESET_VALUE;
	else if(enable)	count <= mux_out;

endmodule
