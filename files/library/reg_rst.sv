module reg_rst 
#(
	parameter WIDTH = 32
)
(
	input 				clk,
	input 				reset,
	input 	   [WIDTH-1:0] data_in,
	output reg [WIDTH-1:0] data_out
);

always@(posedge clk)begin

	if(reset)begin
	data_out <= 0;
	end
	else begin
	data_out <= data_in;
	end
end

endmodule