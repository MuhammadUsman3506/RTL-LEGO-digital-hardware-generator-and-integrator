module axis_mux_4to1
#(	  
	parameter	WIDTH 		= 16,
	parameter	depth		= 2
)
(  
	input		[depth-1:0]			sel,
	input		[WIDTH-1:0]		data_0,
	input						valid_0,
	output	reg					ready_0,
	
	input		[WIDTH-1:0]		data_1,
	input						valid_1,
	output	reg					ready_1,
	
	input		[WIDTH-1:0]		data_2,
	input						valid_2,
	output	reg					ready_2,
	
	input		[WIDTH-1:0]		data_3,
	input						valid_3,
	output	reg					ready_3,
	
	output	reg	[WIDTH-1:0]		data,
	output	reg					valid,
	input						ready

   );

always@*
begin
	case(sel)
	2'b0:
	begin
		data		= data_0;
		valid       = valid_0;
		
		ready_0     = ready;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = 0;
	end
	2'b1:
	begin
		data		= data_1;
		valid       = valid_1;
		
		ready_0     = 0;
		ready_1     = ready;
		ready_2     = 0;
		ready_3     = 0;
	end
	2'b2:
	begin
		data		= data_2;
		valid       = valid_2;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = ready;
		ready_3     = 0;
	end
	2'b3:
	begin
		data		= data_3;
		valid       = valid_3;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = ready;
	end
	endcase
end
endmodule