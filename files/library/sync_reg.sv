module sync_reg
(
   output reg sync, 
   input clk, 
   input async
   );


reg	async_r;


always @(posedge clk)
 begin
   async_r 	<= async;
   sync 	<= async_r;
 end

endmodule
