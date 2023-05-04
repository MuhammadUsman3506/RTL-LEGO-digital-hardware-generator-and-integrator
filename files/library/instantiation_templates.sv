//----------------------------------------------------------------------------------------------------------------------------
// AXI Streaming mux: can be used to multiplex between two AXI streaming interfaces using a select line
axis_mux
	#(	  
		.WIDTH	()
	)
axis_mux_inst	
	(  
	.sel			(),
	
	.data_0			(),
	.valid_0		(),	
	.ready_0		(),
	
	.data_1			(),
	.valid_1		(),
	.ready_1		(),
	
	.data			(),
	.valid			(),
	.ready          ()
    );

//----------------------------------------------------------------------------------------------------------------------------
// Counters
//----------------------------------------------------------------------------------------------------------------------------
// Up counter: Increments on every enable and clears when count reaches count_max AND enable is asserted.
up_counter 
	#(
		.WIDTH	()
	)
up_counter_inst
	(
	.clk		(),
	.reset		(),
	.en			(),
	.count_max	(),
	.clr		(),
	.count		()
	);

//----------------------------------------------------------------------------------------------------------------------------
// Up down counter: Increments on incr and decrements on decr signal. Does nothing if both are high in same cycle.
up_dn_counter
	#(	  
		.WIDTH			(),
		.RESET_VALUE	()
	)
up_dn_counter_inst
	(
	.clk		(),
	.reset		(),
	.incr		(),
	.decr		(),
	.count      ()
	);

//----------------------------------------------------------------------------------------------------------------------------
// BRAMs
//----------------------------------------------------------------------------------------------------------------------------
// True dual port BRAMs without byte enables with write first (bram_dual_wf) and read first (bram_dual) modes
//bram_dual			// Readfirst mode without byte enable
bram_dual_wf		// Write first mode without byte enable
	#(
		.RAM_WIDTH 			(RAM_WIDTH 			),	// Specify RAM data width
		.RAM_DEPTH 			(RAM_DEPTH 			),	// Specify RAM depth (number of entries)
		.RAM_PERFORMANCE 	(RAM_PERFORMANCE 	),	// Select "HIGH_PERFORMANCE" or "LOW_LATENCY"
		.INIT_FILE 			(INIT_FILE 			),	// Specify name/location of RAM initialization file in inverted commas if using one (leave blank if not)
		.INIT_START_ADDR 	(INIT_START_ADDR 	),	
		.INIT_END_ADDR		(INIT_END_ADDR		)	
	)
	bram_dual_inst
	(
	.addra		(addra	),  	// Port A address bus, width determined from RAM_DEPTH
	.addrb		(addrb	),  	// Port B address bus, width determined from RAM_DEPTH
	.dina		(dina	),      // Port A RAM Input data
	.dinb		(dinb	),      // Port B RAM Input data
	.clka		(clka	),      // Port A clock
	.clkb		(clkb	),      // Port B clock
	.wea		(wea	),      // Port A write enable
	.web		(web	),      // Port B write enable
	.ena		(ena	),      // Port A RAM Enable, for additional power savings, disable port when not in use
	.enb		(enb	),      // Port B RAM Enable, for additional power savings, disable port when not in use
	.rsta		(rsta	),      // Port A output reset (does not affect memory contents)
	.rstb		(rstb	),      // Port B output reset (does not affect memory contents)
	.regcea		(regcea	),      // Port A output register enable
	.regceb		(regceb	),      // Port B output register enable
	.douta		(douta	),      // Port A RAM output data
	.doutb		(doutb	)	    // Port B RAM output data
	);


//----------------------------------------------------------------------------------------------------------------------------
// True dual port BRAMs with byte enables with write first (bram_dual_be_wf) and read first (bram_dual_be) modes
//bram_dual_be			// Readfirst mode with byte enable
bram_dual_be_wf		// Write first mode with byte enable
	#(
		.NB_COL				(NB_COL),   
	    .COL_WIDTH 			(COL_WIDTH),
		.RAM_DEPTH 			(RAM_DEPTH 			),	// Specify RAM depth (number of entries)
		.RAM_PERFORMANCE 	(RAM_PERFORMANCE 	),	// Select "HIGH_PERFORMANCE" or "LOW_LATENCY"
		.INIT_FILE 			(INIT_FILE 			),	// Specify name/location of RAM initialization file if using one (leave blank if not)
		.INIT_START_ADDR 	(INIT_START_ADDR 	),	
		.INIT_END_ADDR		(INIT_END_ADDR		)	
	)
	bram_dual_inst
	(
	.addra		(addra	),  	// Port A address bus, width determined from RAM_DEPTH
	.addrb		(addrb	),  	// Port B address bus, width determined from RAM_DEPTH
	.dina		(dina	),      // Port A RAM Input data
	.dinb		(dinb	),      // Port B RAM Input data
	.clka		(clka	),      // Port A clock
	.clkb		(clkb	),      // Port B clock
	.wea		(wea	),      // Port A write enable
	.web		(web	),      // Port B write enable
	.ena		(ena	),      // Port A RAM Enable, for additional power savings, disable port when not in use
	.enb		(enb	),      // Port B RAM Enable, for additional power savings, disable port when not in use
	.rsta		(rsta	),      // Port A output reset (does not affect memory contents)
	.rstb		(rstb	),      // Port B output reset (does not affect memory contents)
	.regcea		(regcea	),      // Port A output register enable
	.regceb		(regceb	),      // Port B output register enable
	.douta		(douta	),      // Port A RAM output data
	.doutb		(doutb	)	    // Port B RAM output data
	);
//----------------------------------------------------------------------------------------------------------------------------
