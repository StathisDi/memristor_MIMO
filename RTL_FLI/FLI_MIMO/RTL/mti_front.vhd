ENTITY mti_front IS
END mti_front;

ARCHITECTURE arch_c OF mti_front IS
  ATTRIBUTE foreign OF arch_c : ARCHITECTURE IS "initForeign MTI_frontend.dll;";
BEGIN
END arch_c;