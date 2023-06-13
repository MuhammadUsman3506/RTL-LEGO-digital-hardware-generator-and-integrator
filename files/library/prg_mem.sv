module prg_mem
#(
	parameter RAM_WIDTH 		= 32,
	parameter RAM_ADDR_BITS 	= 9,
	parameter PROG_FILE 		= "program.hex",
	parameter PROG_START_ADDR 	= 0,
	parameter PROG_END_ADDR		= 8
	
)
(
	input							clock,
	input							ram_enable,
	input							write_enable,
    input 		[RAM_ADDR_BITS-1:0]	address,
    input 		[RAM_WIDTH-1:0] 	in_data,
	output reg 	[RAM_WIDTH-1:0] 	out_data
);
	
   
   (* RAM_STYLE="BLOCK" *)
   reg [RAM_WIDTH-1:0] ram_name [(2**RAM_ADDR_BITS)-1:0];

   initial
    $readmemh(PROG_FILE, ram_name, PROG_START_ADDR, PROG_END_ADDR);

   always @(posedge clock)
    if (ram_enable) begin
       if (write_enable)
          ram_name[address] <= in_data;
       out_data <= ram_name[address];
    end

endmodule