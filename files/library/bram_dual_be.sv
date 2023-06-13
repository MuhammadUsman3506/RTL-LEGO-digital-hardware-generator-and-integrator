module bram_dual_be			
#(
	parameter NB_COL = 4,                       		
	parameter COL_WIDTH = 8,                  			
	parameter RAM_DEPTH = 512,                  		
	parameter RAM_PERFORMANCE = "HIGH_PERFORMANCE", 	
	parameter INIT_FILE = "",                       	
	parameter INIT_START_ADDR 	= 0,
	parameter INIT_END_ADDR		= 1
)
(
  input		[RAM_DEPTH-1:0] addra,
  input		[RAM_DEPTH-1:0] addrb,
  input		[COL_WIDTH-1:0] dina,  
  input		[NB_COL-1:0] dinb,  
  input		clka,                           
  input		clkb,                           
  input		[NB_COL-1:0] wea,               
  input		[NB_COL-1:0] web,               
  input		ena,                            
  input		enb,                            
  input		rsta,				 
  input		rstb,                           
  input		regcea,                         
  input		regceb,                         
  output reg	[COL_WIDTH-1:0] douta, 
  output reg	[COL_WIDTH-1:0] doutb 
);
  reg [(NB_COL*COL_WIDTH)-1:0] ram_name [RAM_DEPTH-1:0];
  reg [(NB_COL*COL_WIDTH)-1:0] ram_data_a = {(NB_COL*COL_WIDTH){1'b0}};
  reg [(NB_COL*COL_WIDTH)-1:0] ram_data_b = {(NB_COL*COL_WIDTH){1'b0}};
  
  generate
    if (INIT_FILE != "") begin: use_init_file
      initial
        $readmemh(INIT_FILE, ram_name, INIT_START_ADDR, INIT_END_ADDR);
    end else begin: init_bram_to_zero
      integer ram_index;
      initial
        for (ram_index = 0; ram_index < RAM_DEPTH; ram_index = ram_index + 1)
          ram_name[ram_index] = {(NB_COL*COL_WIDTH){1'b0}};
    end
  endgenerate
  
  always @(posedge clka)
    if (ena) begin
      ram_data_a <= ram_name[addra];
    end

  always @(posedge clkb)
    if (enb) begin
      ram_data_b <= ram_name[addrb];
    end
	
	generate
  genvar i;
     for (i = 0; i < NB_COL; i = i+1) begin: byte_write
       always @(posedge clka)
         if (ena)
           if (wea[i])
             ram_name[addra][(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= dina[(i+1)*COL_WIDTH-1:i*COL_WIDTH];
       always @(posedge clkb)
         if (enb)
           if (web[i])
             ram_name[addrb][(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= dinb[(i+1)*COL_WIDTH-1:i*COL_WIDTH];
  end
  endgenerate
  
  generate
    if (RAM_PERFORMANCE == "LOW_LATENCY") begin: no_output_register

  
       assign douta = ram_data_a;
       assign doutb = ram_data_b;

    end else begin: output_register

      reg [(NB_COL*COL_WIDTH)-1:0] douta_reg = {(NB_COL*COL_WIDTH){1'b0}};
      reg [(NB_COL*COL_WIDTH)-1:0] doutb_reg = {(NB_COL*COL_WIDTH){1'b0}};

      always @(posedge clka)
        if (rsta)
          douta_reg <= {(NB_COL*COL_WIDTH){1'b0}};
        else if (regcea)
          douta_reg <= ram_data_a;

      always @(posedge clkb)
        if (rstb)
          doutb_reg <= {(NB_COL*COL_WIDTH){1'b0}};
        else if (regceb)
          doutb_reg <= ram_data_b;

      assign douta = douta_reg;
      assign doutb = doutb_reg;

    end
  endgenerate
endmodule								