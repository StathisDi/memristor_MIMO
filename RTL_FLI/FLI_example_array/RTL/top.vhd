ENTITY for_model IS
END for_model;

ARCHITECTURE arch OF for_model IS
  ATTRIBUTE foreign OF aarch : ARCHITECTURE IS "initForeign for_model.sl;";
BEGIN
END arch;

LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

ENTITY top IS

  TYPE bitarray IS ARRAY(3 DOWNTO 0) OF BIT;
  TYPE intarray IS ARRAY(1 TO 3) OF INTEGER;
  TYPE realarray IS ARRAY(1 TO 2) OF real;
  TYPE timearray IS ARRAY(-1 TO 0) OF TIME;

  TYPE rectype IS RECORD
    a : BIT;
    b : INTEGER;
    c : real;
    d : STD_LOGIC;
    e : bitarray;
  END RECORD;

END top;

ARCHITECTURE a OF top IS

  COMPONENT for_model
  END COMPONENT;

  FOR ALL : for_model USE ENTITY work.for_model(arch);

BEGIN

  inst1                : for_model;

  p1 : PROCESS
    VARIABLE bitsig      : BIT                      := '1';
    VARIABLE intsig      : INTEGER                  := 21;
    VARIABLE realsig     : real                     := 16.35;
    VARIABLE timesig     : TIME                     := 5 ns;
    VARIABLE stdlogicsig : STD_LOGIC                := 'H';

    VARIABLE bitarr      : bitarray                 := "0110";
    VARIABLE stdlogicarr : STD_LOGIC_VECTOR(1 TO 4) := "01LH";
    VARIABLE intarr      : intarray                 := (10, 11, 12);
    VARIABLE realarr     : realarray                := (11.6, 101.22);
    VARIABLE timearr     : timearray                := (15 ns, 6 ns);

    VARIABLE rec         : rectype                  := ('0', 1, 3.7, 'H', "1001");

  BEGIN
    bitsig      := NOT bitsig;
    intsig      := intsig + 1;
    realsig     := realsig + 1.5;
    timesig     := timesig + 1 ns;
    stdlogicsig := NOT stdlogicsig;

    bitarr      := NOT bitarr;

    intarr(1)   := intarr(1) + 1;
    intarr(2)   := intarr(2) + 1;
    intarr(3)   := intarr(3) + 1;

    realarr(1)  := realarr(1) + 0.5;
    realarr(2)  := realarr(2) + 0.5;

    timearr(-1) := timearr(-1) + 1 ns;
    timearr(0)  := timearr(0) + 1 ns;

    stdlogicarr := NOT stdlogicarr;

    rec.a       := NOT rec.a;
    rec.b       := rec.b + 1;
    rec.c       := rec.c + 2.5;
    rec.d       := NOT rec.d;
    rec.e       := NOT rec.e;

    WAIT FOR 5 ns;

  END PROCESS;

END a;