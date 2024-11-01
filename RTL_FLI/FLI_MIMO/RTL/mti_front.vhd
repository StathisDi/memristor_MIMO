--------------------------------------------------------------------------------
-- Inptus:
--    * inst->clk_id = mti_FindSignal("/../clk");
--    * inst->rst_id = mti_FindSignal("/../rst_n");
--    * inst->program_id = mti_FindSignal("/../program");
--    * inst->compute_id = mti_FindSignal("/../compute");
--    * inst->crossbar_input_prog_id = mti_FindSignal("/../crossbar_input_prog");
--    * inst->crossbar_input_comp_id = mti_FindSignal("/../crossbar_input_comp");
-- Outputs:
--    * inst->crossbar_rdy_id    = mti_FindSignal("/../crossbar_rdy");
--    * inst->crossbar_output_id = mti_FindSignal("/../crossbar_output");
--------------------------------------------------------------------------------
ENTITY mti_front IS
END mti_front;

ARCHITECTURE arch_c OF mti_front IS
  ATTRIBUTE foreign OF arch_c : ARCHITECTURE IS "initForeign MTI_frontend.dll;";
BEGIN
END arch_c;