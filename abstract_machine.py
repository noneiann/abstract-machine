#!/usr/bin/env python3

import sys

from machine import readcode, assemble, initstate, meval


def read_program_source() -> str:
  """Read assembly program from file argument or stdin."""
  if len(sys.argv) > 1:
    asm_path = sys.argv[1]
    with open(asm_path, "r", encoding="utf-8") as f:
      return f.read().strip()
  return readcode()

# Main program
def runMachine():
  codestr      = read_program_source()  # read code from file arg or stdin
  code         = assemble(codestr)   # code is list of pair of instruction and parameter
  initialstate = initstate(code)     # return a state: (code, stack, memory)
  finalstate   = meval(initialstate)
  _, stack, memory = finalstate
  print(stack[0] if stack else memory) 
  
  #print(finalstate)
  #print(finalstate[1][0])               # The second part is stack

# (Code, Stack, Memory) = state
#    0     1      2

if __name__ == "__main__":
  runMachine()

