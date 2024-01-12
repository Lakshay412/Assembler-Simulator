The newly added instructions have following 5 new instructions

**inc**: (inc reg1) it increments the register value by one. It belongs to type G which I have later defined

**dec**: (dec reg1)it decrements the register value by one. It belongs to type G.

**lea**: (lea reg1 mem_adrs) it stores the memory adress in the register . It belongs to type D

**ldr:** (ldr reg1 reg2) It loads the the data stored in the Memory stored at the memory address stored in reg2 into reg1. It belongs to type 

**strr**: (str reg1 reg2) It stores the data of reg1 into memory at memory address stored in reg2

The Type G follows the following syntax: Opcode(5bits) register(3bits) (8 unused bits)

**instruction     opcode**
inc             10110
dec             10111
lea             10011
ldr             10100
str             10101
  
