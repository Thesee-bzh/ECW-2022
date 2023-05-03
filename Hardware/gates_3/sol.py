#!/usr/bin/python3

import itertools

def AND(b1, b2):
    return b1 & b2

def OR(b1, b2):
    return b1 | b2

def XOR(b1, b2):
    return b1 ^ b2

op = ["AND", "OR", "XOR"]
l = [[op1, op2, op3, op4, op5] for op1 in op for op2 in op for op3 in op for op4 in op for op5 in op]
circuits = list()

# There are only 5 types of circuits with 5 operators and 8 input bits
# (Considering input bits can only be used once):
# - Starting with OP1(OP2(a,b),OP3(c,d)):
#   * OP1(OP2(OP4(a,b),OP5(c,d)),OP3(e,f))
#   * OP1(OP2(OP4(a,b),c),OP3(OP5(d,e),f))
#   * OP1(OP2(OP4(OP5(a,b),c),d),OP3(e,f))
# - Starting with OP1(a,OP2(b,OP3(c,d)):
#   * OP1(a,OP2(b,OP3(c,OP4(d,OP5(e,f)))))
#   * OP1(a,OP2(b,OP3(OP4(c,d),OP5(e,f))))
# With (a,b,c,d,e,f) 6 of the 8 the input bits

# We need list comprehensions for:
# - 4bits among 8
# - 2bits among 8
_8bits = ['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7']
_4bits_l = list(itertools.combinations(_8bits, 4))
_2bits_l = list(itertools.combinations(_8bits, 2))

# List of all circuits of type OP1(OP2(OP4(a,b),OP5(c,d)),OP3(e,f))
for x in l:
    for _4bits in _4bits_l:
        _4bits_1 = [x for x in _8bits if x not in _4bits]
        _2bits_ll = list(itertools.combinations(_4bits_1, 2))
        for _2bits in _2bits_ll:
            a = _4bits[0]; b = _4bits[1]; c = _4bits[2]; d = _4bits[3]
            e = _2bits[0]; f = _2bits[1]
            circuits.append(x[0]+'('+x[1]+'('+x[2]+'('+a+','+b+'),'+x[3]+'('+c+','+d+')),'+x[4]+'('+e+','+f+'))')

# List of all circuits of type OP1(OP2(OP4(a,b),c),OP3(OP5(d,e),f))
for x in l:
    for _4bits in _4bits_l:
        _4bits_1 = [x for x in _8bits if x not in _4bits]
        _2bits_ll = list(itertools.combinations(_4bits_1, 2))
        for _2bits in _2bits_ll:
            a = _4bits[0]; b = _4bits[1]; d = _4bits[2]; e = _4bits[3]
            c = _2bits[0]; f = _2bits[1]
            circuits.append(x[0]+'('+x[1]+'('+x[2]+'('+a+','+b+'),'+c+'),'+x[3]+'('+x[4]+'('+d+','+e+'),'+f+'))')
            c = _2bits[1]; f = _2bits[0]
            circuits.append(x[0]+'('+x[1]+'('+x[2]+'('+a+','+b+'),'+c+'),'+x[3]+'('+x[4]+'('+d+','+e+'),'+f+'))')

# List of all circuits of type OP1(OP2(OP4(OP5(a,b),c),d),OP3(e,f))
for x in l:
    for _2bits_1 in _2bits_l:
        for _2bits_2 in _2bits_l:
            _4bits_1 = [x for x in _8bits if x not in _2bits_1 if x not in _2bits_2]
            _2bits_ll = list(itertools.combinations(_4bits_1, 2))
            for _2bits_3 in _2bits_ll:
                a = _2bits_1[0]; b = _2bits_1[1]; e = _2bits_2[0]; f = _2bits_2[1]
                c = _2bits_3[0]; d = _2bits_3[1]
                circuits.append(x[0]+'('+x[1]+'('+x[2]+'('+x[3]+'('+a+','+b+'),'+c+'),'+d+'),'+x[4]+'('+e+','+f+'))')
                c = _2bits_3[1]; d = _2bits_3[0]
                circuits.append(x[0]+'('+x[1]+'('+x[2]+'('+x[3]+'('+a+','+b+'),'+c+'),'+d+'),'+x[4]+'('+e+','+f+'))')

# List of all circuits of type OP1(a,OP2(b,OP3(c,OP4(d,OP5(e,f)))))
for x in l:
    for _2bits in _2bits_l:
        e = _2bits[0]; f = _2bits[1];
        _6bits_1 = [x for x in _8bits if x not in _2bits]
        _4bits_ll = list(itertools.combinations(_6bits_1, 4))
        for _4bits in _4bits_ll:
            a = _4bits[0]; b = _4bits[1]; c = _4bits[2]; d = _4bits[2]
            circuits.append(x[0]+'('+a+','+x[1]+'('+b+','+x[2]+'('+c+','+x[3]+'('+d+','+x[4]+'('+e+','+f+')))))')

# List of all circuits of type OP1(a,OP2(b,OP3(OP4(c,d),OP5(e,f))))
for x in l:
    for _4bits in _4bits_l:
        c = _4bits[0]; d = _4bits[1]; e = _4bits[2]; f = _4bits[3]
        _4bits_1 = [x for x in _8bits if x not in _4bits]
        _2bits_ll = list(itertools.combinations(_4bits_1, 2))
        for _2bits in _2bits_ll:
            a = _2bits[0]; b = _2bits[1]
            circuits.append(x[0]+'('+a+','+x[1]+'('+b+','+x[2]+'('+x[3]+'('+c+','+d+'),'+x[4]+'('+e+','+f+'))))')
            a = _2bits[1]; b = _2bits[0]; 
            circuits.append(x[0]+'('+a+','+x[1]+'('+b+','+x[2]+'('+x[3]+'('+c+','+d+'),'+x[4]+'('+e+','+f+'))))')

circuits0 = circuits1 = circuits2 = circuits3 = circuits
circuits4 = circuits5 = circuits6 = circuits7 = circuits

# Read input file
count = 0
with open('inputs_outputs.txt', 'r') as f:
    for line in f:
        count += 1
        print()
        print("##", count)
        _in  = int(line.split()[0], 2)
        _out = int(line.split()[2], 2)

        # Extract individual bits from input value
        b0 = (_in >> 7) & 1; b1 = (_in >> 6) & 1; b2 = (_in >> 5) & 1; b3 = (_in >> 4) & 1
        b4 = (_in >> 3) & 1; b5 = (_in >> 2) & 1; b6 = (_in >> 1) & 1; b7 = (_in >> 0) & 1

        # Extract individual bits from output value
        out0 = (_out >> 7) & 1; out1 = (_out >> 6) & 1; out2 = (_out >> 5) & 1; out3 = (_out >> 4) & 1
        out4 = (_out >> 3) & 1; out5 = (_out >> 2) & 1; out6 = (_out >> 1) & 1; out7 = (_out >> 0) & 1

        # Loop on all generated circuits to match the output bit0
        # Build a new list of circuits matching output bit0
        circuits_match0 = list()
        for c in circuits0:
            if (out0 == eval(c)):
                circuits_match0.append(c)
        circuits0 = circuits_match0
        print("b0 done: ", len(circuits0))

        # Loop on all generated circuits to match the output bit1
        # Build a new list of circuits matching output bit1
        circuits_match1 = list()
        for c in circuits1:
            if (out1 == eval(c)):
                circuits_match1.append(c)
        circuits1 = circuits_match1
        print("b1 done: ", len(circuits1))

        # Loop on all generated circuits to match the output bit2
        # Build a new list of circuits matching output bit2
        circuits_match2 = list()
        for c in circuits2:
            if (out2 == eval(c)):
                circuits_match2.append(c)
        circuits2 = circuits_match2
        print("b2 done: ", len(circuits2))

        # Loop on all generated circuits to match the output bit3
        # Build a new list of circuits matching output bit3
        circuits_match3 = list()
        for c in circuits3:
            if (out3 == eval(c)):
                circuits_match3.append(c)
        circuits3 = circuits_match3
        print("b3 done: ", len(circuits3))

        # Loop on all generated circuits to match the output bit4
        # Build a new list of circuits matching output bit4
        circuits_match4 = list()
        for c in circuits4:
            if (out4 == eval(c)):
                circuits_match4.append(c)
        circuits4 = circuits_match4
        print("b4 done: ", len(circuits4))

        # Loop on all generated circuits to match the output bit5
        # Build a new list of circuits matching output bit5
        circuits_match5 = list()
        for c in circuits5:
            if (out5 == eval(c)):
                circuits_match5.append(c)
        circuits5 = circuits_match5
        print("b5 done: ", len(circuits5))

        # Loop on all generated circuits to match the output bit6
        # Build a new list of circuits matching output bit6
        circuits_match6 = list()
        for c in circuits6:
            if (out6 == eval(c)):
                circuits_match6.append(c)
        circuits6 = circuits_match6
        print("b6 done: ", len(circuits6))

        # Loop on all generated circuits to match the output bit7
        # Build a new list of circuits matching output bit7
        circuits_match7 = list()
        for c in circuits7:
            if (out7 == eval(c)):
                circuits_match7.append(c)
        circuits7 = circuits_match7
        print("b7 done: ", len(circuits7))

# We might have multiple circuits to give the same output bit for a given entry
# Pick up the first one for each bit
circuit = [circuits0[0], circuits1[0], circuits2[0], circuits3[0], circuits4[0], circuits5[0], circuits6[0], circuits7[0]]

# Re-read input file, to remove the already known values when generating all the values
known_values = list()
with open('inputs_outputs.txt', 'r') as f:
    for line in f:
        known_values.append(int(line.split()[0], 2))

# Finaly generate all values with the circuit we found, excluding the already known values
with open("suite.txt", "w") as f:
    for val in range(1, 256):
        if val not in known_values:
            # Extract individual bits from input value
            b0 = (val >> 7) & 1; b1 = (val >> 6) & 1; b2 = (val >> 5) & 1; b3 = (val >> 4) & 1
            b4 = (val >> 3) & 1; b5 = (val >> 2) & 1; b6 = (val >> 1) & 1; b7 = (val >> 0) & 1
            # Compute & reassemble the ouput
            out = (eval(circuit[0]) << 7) | (eval(circuit[1]) << 6) | (eval(circuit[2]) << 5) | (eval(circuit[3]) << 4) | (eval(circuit[4]) << 3) | (eval(circuit[5]) << 2) | (eval(circuit[6]) << 1) | eval(circuit[7])
            # Generate expected string: <input> : <output>
            f.write(bin(val)[2:].zfill(8) + " : " + bin(out)[2:].zfill(8) + "\n")
