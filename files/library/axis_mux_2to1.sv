module axis_mux_2to1
	#(	  
		parameter	WIDTH 		= 16
	)
	(  
	input						sel,
	input		[WIDTH-1:0]		data_0,
	input						valid_0,
	output						ready_0,
	
	input		[WIDTH-1:0]		data_1,
	input						valid_1,
	output						ready_1,
	
	output	reg	[WIDTH-1:0]		data,
	output	reg					valid,
	input						ready
	
    );

always@*
begin
	case(sel)
	1'b0:
	begin
		data		= data_0;
		valid       = valid_0;
		ready_0     = ready;
		ready_1     = 0;
	end
	1'b1:
	begin
		data		= data_1;
		valid       = valid_1;
		ready_0     = 0;
		ready_1     = ready;
	end
	endcase
end
endmodule