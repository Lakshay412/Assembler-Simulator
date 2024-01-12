# CO_Project_A33
In The code first I create a list of opcodes, register exluding Flags, and list of all the types of instructions, that is typA typB, ... , typF and instruction list , line list which has list of all the lines of the assembly code.

Then I initialize three dictionaries for variable with the stucture { name:{adrs:int, data:int}, ...} , 
and for labels with the structure {name:adrs, ...} 

i have writeend some helper functions namely intbin() that  converts an integer(n) to binary with x bits

reg_adrs() converts register name to its address.

is_valid_var_instn(s): which checks whether a line starting with var has the correct syntax for variable declaration

Then I define fucnctions which checks the errors for instructions of a specfic opcode types that is 
check_typA, check_typ_B, ....., check_typE. 

Then I define functions which translated instructions of a specific type to its corresponding binary form
namely, trnslt_A(), trnslt_B(), ....., trnsltE() and also separeately  for mov since there are two types of mov opcode.

Then the main code starts which starts processing the line list , which has list of all the lines in assembly code.

the first loop checks for all the variable declarations and saves and also checks for errors

once it reaches a line which is not a variable declaration line thenn it start the second loop which starts processing the instructions after the variable declaration. 

Ther is line_cnt variable whcih keeps track of line number, instrn_cnt variable which keeps track of instruction number, hlt_reached flag variable which is set to True if a hlt instuction is reached .

Then eveytime in the second loop it reads a line it check whether the first word is a valid opcode or not , if not it throws and error, and also it checks whther a new being define or not, if yes then it throws the error. , 

if the opcode is valid then it checks for error with its respective error checker function once that is passed it translates it to its binary form 
for opcode of typd D it stores its line number in update_dic dicitonary to translate it later to binary after assigning memmory adreses to all the variables and all the translated instructions till that point is stored in gapped_string string list. to 

similary for typE also it marks its line number to check translate it later after checking for valid label definitions. 

if hlt is reached then it checks for further instruction if there is then it throws error else it continues 

then it goes in the list where all the typD and typE cann finally be checked for error and be translated and then it is joined appropriatedly with the stings in the gaped string list and the final output string is outputed. 

