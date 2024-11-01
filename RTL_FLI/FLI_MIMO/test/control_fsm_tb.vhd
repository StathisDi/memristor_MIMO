LIBRARY ieee, work;
USE ieee.std_logic_1164.ALL;
USE ieee.numeric_std.ALL;
USE work.data_types.ALL;
USE work.constants.ALL;

ENTITY control_fsm_tb IS
END ENTITY;

ARCHITECTURE behavior OF control_fsm_tb IS

  -- Component Declaration for the Unit Under Test (UUT)
  COMPONENT MIMO_Control_FSM
    PORT (
      clk                : IN STD_LOGIC;
      rst_n              : IN STD_LOGIC;
      instr              : IN INSTRUCTION;
      data_in_comp       : IN int_array_ty(crossbar_rows - 1 DOWNTO 0);
      data_in_prog       : IN int_array_ty(crossbar_cols - 1 DOWNTO 0);
      crossbar_rdy       : IN STD_LOGIC;
      cross_compute_data : OUT int_array_ty(crossbar_rows - 1 DOWNTO 0);
      cross_program_data : OUT int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0);
      reading_prog       : OUT STD_LOGIC;
      compute_cross      : OUT STD_LOGIC;
      valid              : OUT STD_LOGIC
    );
  END COMPONENT;

  -- Testbench signals
  SIGNAL clk                : STD_LOGIC                                := '0';
  SIGNAL rst_n              : STD_LOGIC                                := '0';
  SIGNAL instr              : INSTRUCTION                              := IDLE_INST;
  SIGNAL data_in_comp       : int_array_ty(crossbar_rows - 1 DOWNTO 0) := (OTHERS => 0);
  SIGNAL data_in_prog       : int_array_ty(crossbar_cols - 1 DOWNTO 0) := (OTHERS => 0);
  SIGNAL crossbar_rdy       : STD_LOGIC                                := '1';
  SIGNAL cross_compute_data : int_array_ty(crossbar_rows - 1 DOWNTO 0);
  SIGNAL cross_program_data : int_2d_array_ty(crossbar_rows - 1 DOWNTO 0, crossbar_cols - 1 DOWNTO 0);
  SIGNAL reading_prog       : STD_LOGIC;
  SIGNAL compute_cross      : STD_LOGIC;
  SIGNAL valid              : STD_LOGIC;

  -- Clock generation
  CONSTANT clk_period       : TIME := 10 ns;
BEGIN
  clk_process : PROCESS
  BEGIN
    clk <= '0';
    WAIT FOR clk_period/2;
    clk <= '1';
    WAIT FOR clk_period/2;
  END PROCESS;

  -- Instantiate the Unit Under Test (UUT)
  uut : MIMO_Control_FSM PORT MAP(
    clk                => clk,
    rst_n              => rst_n,
    instr              => instr,
    data_in_comp       => data_in_comp,
    data_in_prog       => data_in_prog,
    crossbar_rdy       => crossbar_rdy,
    cross_compute_data => cross_compute_data,
    cross_program_data => cross_program_data,
    reading_prog       => reading_prog,
    compute_cross      => compute_cross,
    valid              => valid
  );

  -- Stimulus process
  stim_proc : PROCESS
  BEGIN
    -- Reset the system
    rst_n <= '0';
    WAIT FOR 20 ns;
    rst_n <= '1';
    WAIT UNTIL rising_edge(clk);
    -- Test programming instruction
    instr <= PROGRAM_INST;
    WAIT UNTIL rising_edge(clk);
    instr <= IDLE_INST;
    FOR i IN 1 TO crossbar_rows LOOP
      data_in_prog <= ((OTHERS => i));
      WAIT UNTIL rising_edge(clk);
    END LOOP;
    WAIT UNTIL reading_prog = '0';
    WAIT UNTIL rising_edge(clk);
    -- Test computation instruction
    instr <= COMPUTE_INST;
    WAIT UNTIL rising_edge(clk);
    instr <= IDLE_INST;
    FOR i IN 1 TO crossbar_rows LOOP
      REPORT "Applying computation data: " & INTEGER'image(i);
      data_in_comp(i - 1) <= i;
    END LOOP;
    WAIT UNTIL valid = '1';
    WAIT UNTIL rising_edge(clk);
    WAIT UNTIL rising_edge(clk);
    -- End simulation
    WAIT;
  END PROCESS;

END ARCHITECTURE;