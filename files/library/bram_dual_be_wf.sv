module bram_dual_be_wf			
#(
	parameter NB_COL = 4,                       		
	parameter COL_WIDTH = 8,                  			
	parameter RAM_DEPTH = 512,                  		
	parameter RAM_PERFORMANCE = "HIGH_PERFORMANCE", 	
	parameter INIT_FILE = "",                       	
	parameter INIT_START_ADDR 	= 0,
	parameter INIT_END_ADDR		= RAM_DEPTH-1
)
(
  input		[clogb2(RAM_DEPTH-1)-1:0] addra, 
  input		[clogb2(RAM_DEPTH-1)-1:0] addrb, 
  input		[(NB_COL*COL_WIDTH)-1:0] dina,   
  input		[(NB_COL*COL_WIDTH)-1:0] dinb,   
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
  output 	[(NB_COL*COL_WIDTH)-1:0] douta, 
  output 	[(NB_COL*COL_WIDTH)-1:0] doutb 
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

  generate
  genvar i;
     for (i = 0; i < NB_COL; i = i+1) begin: byte_write
       always @(posedge clka)
         if (ena)
           if (wea[i]) begin
             ram_name[addra][(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= dina[(i+1)*COL_WIDTH-1:i*COL_WIDTH];
             ram_data_a[(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= dina[(i+1)*COL_WIDTH-1:i*COL_WIDTH];
           end else begin
             ram_data_a[(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= ram_name[addra][(i+1)*COL_WIDTH-1:i*COL_WIDTH];
           end

       always @(posedge clkb)
         if (enb)
           if (web[i]) begin
             ram_name[addrb][(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= dinb[(i+1)*COL_WIDTH-1:i*COL_WIDTH];
             ram_data_b[(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= dinb[(i+1)*COL_WIDTH-1:i*COL_WIDTH];
           end else begin
             ram_data_b[(i+1)*COL_WIDTH-1:i*COL_WIDTH] <= ram_name[addrb][(i+1)*COL_WIDTH-1:i*COL_WIDTH];
           end
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

  
  function integer clogb2;
    input integer depth;
      for (clogb2=0; depth>0; clogb2=clogb2+1)
        depth = depth >> 1;
  endfunction
endmodule							