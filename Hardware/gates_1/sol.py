#!/usr/bin/python3

def AND(b1, b2):
    return b1 & b2

def OR(b1, b2):
    return b1 | b2

def XOR(b1, b2):
    return b1 ^ b2

def compute(value):
    # Extract individual bits from input value
    b0 = (value >> 3) & 1
    b1 = (value >> 2) & 1
    b2 = (value >> 1) & 1
    b3 = (value >> 0) & 1

    # Compute the ouput
    b0_ = OR(XOR(b1, b2), AND(b0, b3))
    b1_ = OR(XOR(b1, b3), XOR(b0, b2))
    b2_ = OR(b3, XOR(b1, XOR(b0, b2)))
    b3_ = AND(b3, AND(b1, AND(b0, b2)))

    # Reassemble the output
    out = (b0_ << 3) | (b1_ << 2) | (b2_ << 1) | b3_

    # Generate expected string: <input> : <output>
    return bin(value)[2:].zfill(4) + " : " + bin(out)[2:].zfill(4) + "\n"

with open("suite.txt", "w") as f:
    for val in range(1, 16):
        f.write(compute(val))
