module bram_dual_wf
#(
	parameter RAM_WIDTH 		= 32,					
	parameter RAM_DEPTH 		= 512,                  
	parameter RAM_PERFORMANCE 	= "HIGH_PERFORMANCE",   
	parameter INIT_FILE 		= "",					
	parameter INIT_START_ADDR 	= 0,
	parameter INIT_END_ADDR		= RAM_DEPTH-1
	)
	(
	input	[clogb2(RAM_DEPTH-1)-1:0] addra,  	
	input	[clogb2(RAM_DEPTH-1)-1:0] addrb,  	
	input	[RAM_WIDTH-1:0] dina,           	
	input	[RAM_WIDTH-1:0] dinb,           	
	input	clka,                           	
	input	clkb,                           	
	input	wea,                            	
	input	web,                            	
	input	ena,                            	
	input	enb,                            	
	input	rsta,                           	
	input	rstb,                           	
	input	regcea,                         	
	input	regceb,                         	
	output	[RAM_WIDTH-1:0] douta,          	
	output	[RAM_WIDTH-1:0] doutb	          	
	);

  reg [RAM_WIDTH-1:0] ram_name [RAM_DEPTH-1:0];
  reg [RAM_WIDTH-1:0] ram_data_a = {RAM_WIDTH{1'b0}};
  reg [RAM_WIDTH-1:0] ram_data_b = {RAM_WIDTH{1'b0}};
  generate
    if (INIT_FILE != "") begin: use_init_file
      initial
        $readmemh(INIT_FILE, ram_name, INIT_START_ADDR, INIT_END_ADDR);
    end else begin: init_bram_to_zero
      integer ram_index;
      initial
        for (ram_index = 0; ram_index < RAM_DEPTH; ram_index = ram_index + 1)
          ram_name[ram_index] = {RAM_WIDTH{1'b0}};
    end
  endgenerate

  always @(posedge clka)
    if (ena)
      if (wea) begin
        ram_name[addra] <= dina;
        ram_data_a <= dina;
      end else
        ram_data_a <= ram_name[addra];
	   

  always @(posedge clkb)
    if (enb)
      if (web) begin
        ram_name[addrb] <= dinb;
        ram_data_b <= dinb;
      end else
        ram_data_b <= ram_name[addrb];

  
  generate
    if (RAM_PERFORMANCE == "LOW_LATENCY") begin: no_output_register

  
       assign douta = ram_data_a;
       assign doutb = ram_data_b;

    end else begin: output_register

      reg [RAM_WIDTH-1:0] douta_reg = {RAM_WIDTH{1'b0}};
      reg [RAM_WIDTH-1:0] doutb_reg = {RAM_WIDTH{1'b0}};

      always @(posedge clka)
        if (rsta)
          douta_reg <= {RAM_WIDTH{1'b0}};
        else if (regcea)
          douta_reg <= ram_data_a;

      always @(posedge clkb)
        if (rstb)
          doutb_reg <= {RAM_WIDTH{1'b0}};
        else if (regceb)
          doutb_reg <= ram_data_b;

      assign douta = douta_reg;
      assign doutb = doutb_reg;

    end
  endgenerate

  function integer clogb2;
    input integer depth;
      for (clogb2=0; depth>0; clogb2=clogb2+1)
        depth = depth >> 1;
  endfunction

endmodule	