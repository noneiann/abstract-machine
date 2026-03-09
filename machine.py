
# Machine instructions
def push(n, stack):
  stack.append(n)

def pop(stack):
  stack.pop()

def dup(stack):
  stack.append(stack[-1])

def swap(stack):
  stack[-1], stack[-2] = stack[-2], stack[-1]

def over(stack):
  stack.append(stack[-2])

def add(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(op1 + op2)
    
def sub(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(op1 - op2)
    
def mul(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(op1 * op2)
def div(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append( 0 if op2== 0 or op1 == 0 else op1 // op2)  # Integer division

def bnot(stack):
  op = stack.pop()
  stack.append(0 if op else 1)

def bor(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if op1 and op2 else 0)

def band(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if op1 & op2 else 0)

def nand(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(0 if op1 & op2 else 1)

def nor(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(0 if op1 | op2 else 1)

def xor(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(
    stack.append(1 if (op1 or op2) and not (op1 and op2) else 0)
  )

def xnor(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if (op1 and op2) or (not op1 and not op2) else 0)

def eq(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if op1 == op2 else 0)

def neq(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if op1 != op2 else 0)

def gt(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if op1 > op2 else 0)

def lt(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if op1 < op2 else 0)

def le(stack):
  op2 = stack.pop()
  op1 = stack.pop()
  stack.append(1 if op1 <= op2 else 0)

def hlt(stack):
  return "HALT"


# Control flow instructions
def lab(name, labels_dict, idx):
  labels_dict[name] = idx

def jmp(target_idx, stack):
  return target_idx  # Signal meval to jump

def jz(target_idx, stack):
  cond = stack.pop()
  return target_idx if cond == 0 else None

def jnz(target_idx, stack):
  cond = stack.pop()
  return target_idx if cond != 0 else None

# Instructions as string to instructions as functions
instr = {
  "PUSH" : push, 
  "POP"  : pop,
  "ADD"  : add, 
  "SUB"  : sub,
  "MUL"  : mul,
  "DIV"  : div,
  "NOT"  : bnot,
  "OR"   : bor,
  "AND"  : band,
  "NAND" : nand,
  "NOR"  : nor,
  "XOR"  : xor,
  "XNOR" : xnor,
  "EQ"   : eq,
  "NEQ"  : neq,
  "DUP"  : dup,
  "SWAP" : swap,
  "OVER" : over,
  "GT"   : gt,
  "LT"   : lt,
  "LE"   : le,
  "LAB"  : lab,
  "JMP"    : jmp,
  "J"      : jmp,
  "JZ"   : jz,
  "JNZ"  : jnz,
  "HLT"  : hlt
}

# Read code from input file
def readcode():
  # Read a single program line from stdin.
  return input().strip()

def assemble(strCode):
  code_raw = []
  labels = {}
  
  for strIns in strCode.split(';'):
    tokens = strIns.strip().split()
    if tokens:
      code_raw.append(tokens)
  
  for idx, tokens in enumerate(code_raw):
    if tokens[0].upper() == "LAB":
      labels[tokens[1]] = idx
  
  code = []
  for tokens in code_raw:
    op = tokens[0].upper()
    if op not in instr:
      raise ValueError(f"Unknown instruction: {tokens[0]}")

    if op == "LAB":
      code.append((lab, None)) 
    elif op in ["J", "JMP", "JZ", "JNZ"]:
      label = tokens[1]
      if label not in labels:
        raise ValueError(f"Undefined label: {label}")
      code.append((instr[op], labels[label]))
    elif len(tokens) == 1:
      code.append((instr[op], None))
    else:
      operand = tokens[1]
      if operand.startswith("M[") and operand.endswith("]") and len(operand) > 3:
        code.append((instr[op], "M", operand[2:-1]))
      else:
        code.append((instr[op], int(operand)))
  return code

# Initialize the machine with code and empty stack
def initstate(code):
  return (code, [], {})  

def meval(state):
  code, stack, memory = state
  ip = 0
  
  while ip < len(code):
    instr_item = code[ip]
    fn = instr_item[0]
    result = None

    # Memory-operand form: (fn, "M", address)
    if len(instr_item) == 3 and instr_item[1] == "M":
      addr = instr_item[2]
      if fn is push:
        stack.append(memory.get(addr, 0))
      elif fn is pop:
        memory[addr] = stack.pop()
      else:
        raise ValueError("Only PUSH/POP accept memory operands M[x]")
      ip += 1
      continue

    _, param = instr_item
    
    if param is None:
      result = fn(stack) if fn is not lab else None
    else:
      result = fn(param, stack)

    if result == "HALT":
      break
    
    # If jump returns an address, use it; else step forward
    ip = result if isinstance(result, int) else ip + 1
  
  return state
