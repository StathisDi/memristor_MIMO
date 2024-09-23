import os
import sys
import pickle
import vhdl_codegen as hdl

def main():
    hdl.example()
    # total_no => states
    # voltage => write voltage 
    # cycle => dt (pulse/clock cycle)
    # duty ratio => duty cycle
    # V_reset => reset voltage
    # conductance => LUT from minimum conductance to max conductance 
    #with open('../../../modules/MemMIMO/memristor_lut.pkl', 'rb') as f:
    #    data = pickle.load(f)

    #print(data)

if __name__ == "__main__":
    main()