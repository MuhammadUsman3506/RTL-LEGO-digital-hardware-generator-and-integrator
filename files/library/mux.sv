module Mux
#(
	parameter RAM_WIDTH	= 32
)
(
  input   s_l,
  input   [RAM_WIDTH-1:0] in0,
  input   [RAM_WIDTH-1:0] in1,
  output  [RAM_WIDTH-1:0] out
);
  assign out = s_l ? in1 : in0;
endmodule
