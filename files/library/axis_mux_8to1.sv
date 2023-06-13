module axis_mux_2to1
#(	  
	parameter	WIDTH 		= 16,
	parameter	depth		= 2
)
(  
input		[depth-1:0]			sel,
input		[WIDTH-1:0]		data_0,
input						valid_0,
output	reg				ready_0,

input		[WIDTH-1:0]		data_1,
input						valid_1,
output	reg					ready_1,

input		[WIDTH-1:0]		data_2,
input						valid_2,
output	reg					ready_2,

input		[WIDTH-1:0]		data_3,
input						valid_3,
output	reg					ready_3,

input		[WIDTH-1:0]		data_4,
input						valid_4,
output	reg					ready_4,

input		[WIDTH-1:0]		data_5,
input						valid_5,
output	reg					ready_5,

input		[WIDTH-1:0]		data_6,
input						valid_6,
output	reg					ready_6,

input		[WIDTH-1:0]		data_7,
input						valid_7,
output	reg					ready_7,

output	reg	[WIDTH-1:0]		data,
output	reg					valid,
input						ready

   );

always@*
begin
	case(sel)
	3'b0:
	begin
		data		= data_0;
		valid       = valid_0;
		
		ready_0     = ready;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = 0;
		ready_4     = 0;
		ready_5     = 0;
		ready_6     = 0;
		ready_7     = 0;
	end
	3'b1:
	begin
		data		= data_1;
		valid       = valid_1;
		
		ready_0     = 0;
		ready_1     = ready;
		ready_2     = 0;
		ready_3     = 0;
		ready_4     = 0;
		ready_5     = 0;
		ready_6     = 0;
		ready_7     = 0;
	end
	3'b2:
	begin
		data		= data_2;
		valid       = valid_2;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = ready;
		ready_3     = 0;
		ready_4     = 0;
		ready_5     = 0;
		ready_6     = 0;
		ready_7     = 0;
	end
	3'b3:
	begin
		data		= data_3;
		valid       = valid_3;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = ready;
		ready_4     = 0;
		ready_5     = 0;
		ready_6     = 0;
		ready_7     = 0;
	end
	3'b4:
	begin
		data		= data_4;
		valid       = valid_4;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = 0;
		ready_4     = ready;
		ready_5     = 0;
		ready_6     = 0;
		ready_7     = 0;
	end
	3'b5:
	begin
		data		= data_5;
		valid       = valid_5;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = 0;
		ready_4     = 0;
		ready_5     = ready;
		ready_6     = 0;
		ready_7     = 0;
	end
	3'b6:
	begin
		data		= data_6;
		valid       = valid_6;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = 0;
		ready_4     = 0;
		ready_5     = 0;
		ready_6     = ready;
		ready_7     = 0;
	end
	3'b7:
	begin
		data		= data_7;
		valid       = valid_7;
		
		ready_0     = 0;
		ready_1     = 0;
		ready_2     = 0;
		ready_3     = 0;
		ready_4     = 0;
		ready_5     = 0;
		ready_6     = 0;
		ready_7     = ready;
	end
	endcase
end
endmodule