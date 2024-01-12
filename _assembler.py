import sys
fl = "assembly_code1.txt"  # assembly code file name
#file = open(fl, "r")
line_list = sys.stdin.readlines()
#file.close()

reg_dic = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0,"FLAGS": ['0', '0', '0', '0']}  # this is dictionary of valid register names with the data they contain.
opcode_list = ["add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]
reg_list = ["R0", "R1", "R2", "R3", "R4", "R5", "R6"]

typA = ["add", "sub", "mul", "xor", "or", "and"]
typB = ["mov", "rs", "ls"]
typC = ["mov", "div", "not", "cmp"]
typD = ["ld", "st"]
typE = ["jmp", "jlt", "jgt", "je"]
typF = ["hlt"]
gn_err = ": General Syntax Error"

instn_lst = []  # list of all intstructions mostly won't be needed
var_dic = {}  # { name:{adrs:int, data:int}, ...} dictionary of variables
label_dic = {}  # {name:adrs, ...} dictionary of labels

# converts an integer(n) to binary with x bits
def intbin(n, x):
    s = format(n, f"0{x}b")
    return s

# converts register name to its address.
def reg_adr(s):
    if (s == "FLAGS"):
        return "111"
    n = int(s[1])
    return intbin(n, 3)

# converts flag to binary/mostly won't be needed
def flag_to_binary():
    return "000000000000" + "".join(reg_dic["FLAGS"])

def is_valid_var_instn(s):

    if len(s.split()) != 2 or s.split()[0] != "var" or s.split()[1] in var_dic:

        return False

    return True

#*************************************************
# ERROR CHECKER FUNCTIONS
def check_typA(instrn, ln_nmber):
    list = instrn.split()

    if len(list) != 4:
        print("line", ln_nmber, "General Syntax Error")
        return False
    if "FLAGS" in list[1:]:
        print("line", ln_nmber, ": Illegal use of FLAGS register!")
        return False
    for i in range(1, 4):
        if list[i] not in reg_list:
            print("line", ln_nmber, "Typos in Register name")
            return False

    # if len(list) != len(set(list)): edit this after doubt clearance
    #     return False
    return True
def check_typB(instrn, ln_nmber):
    list = instrn.split()
    if len(list)!=3:
        print("line", ln_nmber, gn_err)
        return False
    if "FLAGS" == list[1]:
        print("line", ln_nmber, ": Illegal use of FLAGS register!")
        return False
    if list[1] not in reg_list:
        print("line", ln_nmber, "Typos in Register name")
        return False
    if list[2][0] != "$":
        print("line", ln_nmber, gn_err)
        return False
    if not list[2][1:].isdigit():
        if list[2][2:].isdigit() and list[2][1]=="-":
            print("line", ln_nmber, ": Illegal immediate values")
        else:
            print("line", ln_nmber, gn_err)
        return False
    if int(list[2][1:]) > 127: #negative values are checked by the if condtion above only, be detecting "-" sign
        print("line", ln_nmber, ": Illegal immediate values")
        return False
    return True
def check_typC(instrn, ln_nmber):
    list = instrn.split()
    if len(list)!=3:
        print("line", ln_nmber, gn_err)
        return False
    if "FLAGS" == list[1]:
        print("line", ln_nmber, ": Illegal use of FLAGS register!")
        return False
    if list[1] not in reg_list:
        print("line", ln_nmber, "Typos in Register name")
        return False
    if list[2] not in reg_list and list[2]!="FLAGS":
        print("line", ln_nmber, "Typos in Register name")
        return False
    return True
def check_mov(instrn, ln_nmber):
    list = instrn.split()
    if len(list)!=3:
        return False
    if list[2][0]=="$":
        return check_typB(instrn, ln_nmber)
    else:
        return check_typC(instrn, ln_nmber)

def check_typD(instrn, ln_nmber):
    list = instrn.split()
    if len(list)!=3:
        print("line", ln_nmber, gn_err)
        return False
    if "FLAGS" == list[1]:
        print("line", ln_nmber, ": Illegal use of FLAGS register!")
        return False
    if list[1] not in reg_list:
        print("line", ln_nmber, "Typos in Register name")
        return False
    if list[2] in label_dic:
        print("line", ln_nmber, "Use of undefined variable and Misuse of label as variable")
        return False
    if list[2] not in var_dic:
        print("line", ln_nmber, "Use of Undefined variables!")
        return False
    return True

def check_typE(instrn, ln_nmber):
    list = instrn.split()
    if len(list)!=2:
        print("line", ln_nmber, gn_err)
        return False
    if list[1] in var_dic:
        print("line", ln_nmber, "Misuse of variable as label")
        return False
    if list[1] not in label_dic:
        print("line", ln_nmber, "Use of undefined label")
        return False
    return True

#****************************************************************
# TRANSLATOR FUNCTIONS
def trnslt_A(instrn):
    n = instrn.split()
    reg1 = intbin(int(n[1][1]), 3)
    reg2 = intbin(int(n[2][1]), 3)
    reg3 = intbin(int(n[3][1]), 3)
    if n[0] == "add":
        s = "0000000" + str(reg1) + str(reg2) + str(reg3)
    if n[0] == "sub":
        s = "0000100" + str(reg1) + str(reg2) + str(reg3)
    if n[0] == "mul":
        s = "0011000" + str(reg1) + str(reg2) + str(reg3)
    if n[0] == "xor":
        s = "0101000" + str(reg1) + str(reg2) + str(reg3)
    if n[0] == "or":
        s = "0101100" + str(reg1) + str(reg2) + str(reg3)
    if n[0] == "and":
        s = "0110000" + str(reg1) + str(reg2) + str(reg3)

    return s
def trnslt_B(instrn):
    n = instrn.split()
    reg1 = intbin(int(n[1][1]), 3)
    imd_val = str(intbin(int(n[2][1:]), 7))
    if n[0] == "mov":
        s = "000100" + str(reg1) + imd_val
    if n[0] == "ls":
        s = "010010" + str(reg1) + imd_val
    if n[0] == "rs":
        s = "010000" + str(reg1) + imd_val

    return s

def trnslt_C(instrn):
    n = instrn.split()
    reg1 = intbin(int(n[1][-1]), 3)
    if n[2] == "FLAGS":
        reg2 = 111
    else:
        reg2 = intbin(int(n[2][-1]), 3)

    if n[0] == "mov":
        s = "0001100000" + str(reg1) + str(reg2)
    elif n[0] == "div":
        s = "0011100000" + str(reg1) + str(reg2)
    elif n[0] == "not":
        s = "0110100000" + str(reg1) + str(reg2)
    elif n[0] == "cmp":
        s = "0111000000" + str(reg1) + str(reg2)

    return s

def trnslt_D(instrn, tot_lines):
    n = instrn.split()
    reg1 = intbin(int(n[1][-1]), 3)
    var_indx = list(var_dic.keys()).index(n[2])
    var_bin = str(intbin(tot_lines + var_indx, 7))
    # print(var_bin)
    if n[0] == "ld":
        s = "001000" + str(reg1) + var_bin
    if n[0] == "st":
        s = "001010" + str(reg1) + var_bin
    return s

def trnslt_E(instrn):
    n = instrn.split()
    lbl = str(intbin(label_dic[n[1]]-1, 7))
    if n[0] == "jmp":
        s = "011110000" + lbl
    elif n[0] == "jlt":
        s = "111000000" + lbl
    elif n[0] == "jgt":
        s = "111010000" + lbl
    elif n[0] == "je":
        s = "111110000" + lbl
    return s
#********************************************************************


# main code
# this loop checks for all initial variable declarations and adds it to the dictionary of variables.


line_cnt = 1
for line in line_list:
    line = line.strip()
    if line == "":
        line_cnt+=1
        continue
    else:
        if line.split()[0]== "var":
            if is_valid_var_instn(line):
                var_dic[line.split()[1]] = {"adrs": 0, "data": 0}
            else:
                print("line", line_cnt, gn_err)
                exit()
        else:
            lst_line = line
            break
    line_cnt += 1

instrn_cnt = 1
update_dic = {}
gapped_string_lst = []
hlt_reached = False
main_str = ""
# print("main code starts")
for i in range(line_cnt - 1, len(line_list)):
    line = line_list[i].strip()
    if line == "":
        line_cnt+=1
        continue
    if hlt_reached:
        print("line", line_cnt-1, "hlt not being used as the last instruction")
        exit()
    split_lst = line.split()
    if split_lst[0] == "var" and (is_valid_var_instn(line)):
        print("line:", line_cnt, ": Error!, Variable not declared at the beginning.")
        exit()

    if split_lst[0][-1] == ":":
        if split_lst[0][:-1] in label_dic:
            print("line", line_cnt, gn_err, "Repetition in labelling")
            exit()
        label_dic[split_lst[0][:-1]] = instrn_cnt
        if split_lst[0][:-1] in var_dic:
            print("line", line_cnt, "Misuse of variable as label.")
            exit()
        if len(split_lst)==1:
            line_cnt+=1
            continue
        opcd = split_lst[1]
        line = " ".join(split_lst[1:])
        line_list[line_cnt-1] = line + "\n"
        line = line.strip()
        split_lst=line.split()
        #this being written with the assumption that label instructions can be present without any instruction referring it.
    else:
        opcd = split_lst[0]

    if opcd not in opcode_list:
        print("line", line_cnt, ": Typos in instruction name")
        exit()
    else:
        if opcd in typA:
            if check_typA(line, line_cnt):
                main_str = main_str + trnslt_A(line) + "\n"
                #print(trnslt_A(line))
            else:
                exit()
        elif opcd == "mov":
            if check_mov(line, line_cnt):
                if split_lst[2][0]=="$":
                    main_str = main_str + trnslt_B(line) + "\n"
                    # print(trnslt_B(line))
                else:
                    main_str = main_str + trnslt_C(line) + "\n"
                    # print(trnslt_C(line))
            else:
                exit()
        elif opcd in typB:
            if check_typB(line, line_cnt):
                main_str = main_str + trnslt_B(line) + "\n"
                # print(trnslt_B(line))
            else:
                exit()
        elif opcd in typC:
            if check_typC(line, line_cnt):
                main_str = main_str + trnslt_C(line) + "\n"
                # print(trnslt_C(line))
            else:
                exit()
        elif opcd in typD:
            if check_typD(line, line_cnt):
                update_dic[line_cnt] = "D"
                gapped_string_lst.append(main_str)
                main_str = ""
            else:
                exit()
        elif opcd in typE:
            if len(line.split())!=2:
                print("line", line_cnt, gn_err)
                exit()
            update_dic[line_cnt] = "E"
            gapped_string_lst.append(main_str)
            main_str = ""
        elif opcd in typF:
            if len(line.split())!=1:
                print("line", line_cnt, gn_err)
                exit()
            main_str = main_str + "1101000000000000" + "\n"
            # print("1101000000000000")
            hlt_reached = True
        line_cnt+=1
        # print(line)
        # print(instrn_cnt)
        instrn_cnt+=1
gapped_string_lst.append(main_str)
if not hlt_reached:
    print("Missing hlt instruction")
    exit()
fin_str = ""

tot_instrn_cnt = instrn_cnt-1
if (tot_instrn_cnt>128) :
    print(gn_err, "instruction limit exceeded, limit = 128")
    exit()
elif tot_instrn_cnt + len(var_dic)>128:
    print(gn_err, "variable storage overflow")
    exit()


# print(tot_instrn_cnt)
# print("main code ends")

# print("var_dic:", var_dic)
# print("***")
# print("label_dic:", label_dic)
# print("***")
# print("update_dic:", update_dic)
j = 0
add_str = ""
# for i in gapped_string_lst:
#print(line_list)

#     print("***")
#     print(i)
# print("#"*10)
for line in update_dic:
    if update_dic[line] == "D":
        # print("DD")
        # print("this->", line_list[line-1])
        add_str = trnslt_D(line_list[line-1], tot_instrn_cnt)

    else:
        # print("eee")
        # print(line_list[line-1])
        if check_typE(line_list[line-1], line):
            add_str = trnslt_E(line_list[line-1])
            # print(add_str)
        else:
            exit()
    fin_str = fin_str + gapped_string_lst[j] + add_str + "\n"
    j+=1
fin_str = fin_str + gapped_string_lst[j]
fin_str = fin_str.strip()
print(fin_str, end="")

file_o = open("binary_cd.txt", "w")
file_o.write(fin_str)
file_o.close()

