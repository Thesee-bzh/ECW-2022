#!/usr/bin/python3

def AND(b1, b2):
    return b1 & b2

def OR(b1, b2):
    return b1 | b2

def XOR(b1, b2):
    return b1 ^ b2

op = ["AND", "OR", "XOR"]
l = [[op1, op2, op3] for op1 in op for op2 in op for op3 in op]
circuits = list()

# There are only 2 types of circuits with 3 operators and 4 input bits
# (Considering input bits can only be used once):
# - OP1(OP2(a,b),OP3(c,d))
# - OP1(a,OP2(b,OP3(c,d))
# With (a,b,c,d) the input bits

# List of all circuits of type OP1(OP2(a,b),OP3(c,d))
for c in l:
    circuits.append(c[0] + '(' + c[1] + '(b0, b1), ' + c[2] + '(b2, b3))')

# List of all circuits of type OP1(a,OP2(b,OP3(c,d))
for c in l:
    circuits.append(c[0] + '(b0, ' + c[1] + '(b1, ' + c[2] + '(b2, b3)))')
    circuits.append(c[0] + '(b0, ' + c[1] + '(b2, ' + c[2] + '(b1, b3)))')
    circuits.append(c[0] + '(b0, ' + c[1] + '(b3, ' + c[2] + '(b1, b2)))')
    circuits.append(c[0] + '(b1, ' + c[1] + '(b2, ' + c[2] + '(b0, b3)))')
    circuits.append(c[0] + '(b1, ' + c[1] + '(b3, ' + c[2] + '(b0, b2)))')
    circuits.append(c[0] + '(b2, ' + c[1] + '(b3, ' + c[2] + '(b0, b1)))')

circuits0 = circuits1 = circuits2 = circuits3 = circuits

# Read input file
with open('input.txt', 'r') as f:
    for line in f:
        _in  = int(line.split()[0], 2)
        _out = int(line.split()[2], 2)

        # Extract individual bits from input value
        b0 = (_in >> 3) & 1
        b1 = (_in >> 2) & 1
        b2 = (_in >> 1) & 1
        b3 = (_in >> 0) & 1

        # Extract individual bits from output value
        out0 = (_out >> 3) & 1
        out1 = (_out >> 2) & 1
        out2 = (_out >> 1) & 1
        out3 = (_out >> 0) & 1

        # Loop on all generated circuits to match the output bit0
        # Build a new list of circuits matching output bit0
        circuits_match0 = list()
        for c in circuits0:
            if (out0 == eval(c)):
                circuits_match0.append(c)
        circuits0 = circuits_match0

        # Loop on all generated circuits to match the output bit1
        # Build a new list of circuits matching output bit1
        circuits_match1 = list()
        for c in circuits1:
            if (out1 == eval(c)):
                circuits_match1.append(c)
        circuits1 = circuits_match1

        # Loop on all generated circuits to match the output bit2
        # Build a new list of circuits matching output bit2
        circuits_match2 = list()
        for c in circuits2:
            if (out2 == eval(c)):
                circuits_match2.append(c)
        circuits2 = circuits_match2

        # Loop on all generated circuits to match the output bit3
        # Build a new list of circuits matching output bit3
        circuits_match3 = list()
        for c in circuits3:
            if (out3 == eval(c)):
                circuits_match3.append(c)
        circuits3 = circuits_match3

# We might have multiple circuits to give the same output bit for a given entry
# Pick up the first one for each bit
circuit = [circuits0[0], circuits1[0], circuits2[0], circuits3[0]]

# Re-read input file, to remove the already known values when generating all the values
known_values = list()
with open('input.txt', 'r') as f:
    for line in f:
        known_values.append(int(line.split()[0], 2))

# Finaly generate all values with the circuit we found, excluding the already known values
with open("suite.txt", "w") as f:
    for val in range(1, 16):
        if val not in known_values:
            # Extract individual bits from input value
            b0 = (val >> 3) & 1
            b1 = (val >> 2) & 1
            b2 = (val >> 1) & 1
            b3 = (val >> 0) & 1
            # Compute & reassemble the ouput
            out = (eval(circuit[0]) << 3) | (eval(circuit[1]) << 2) | (eval(circuit[2]) << 1) | eval(circuit[3])
            # Generate expected string: <input> : <output>
            f.write(bin(val)[2:].zfill(4) + " : " + bin(out)[2:].zfill(4) + "\n")
