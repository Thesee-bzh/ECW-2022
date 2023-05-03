# Hardware / gates 2/3

## Challenge
In addition to the circuit schema, we also found test results of unidentified circuits. These circuits seems to have a similar design pattern as the previous one. Which means :

- Every output bit is determined separately
- The value of one output bit is the result of a logical equation using a series of AND, OR and XOR Gates
  - The number of gates for each output is fixed and equal to 3 Example : bit_0 AND bit_1 OR bit_2 AND bit_3
- For each output bit, a given input bit is never used more than once
  - One input bit can be used for multiple output bits
  - One output bit does not use multiple times the same input bit Example : OUTPUT_0 = bit_0 AND bit_1 OR bit_2 AND bit_3 OUTPUT_1 = bit_0 OR bit_1 XOR bit_2 AND bit_3
- The size of the input is equal to the size of the output
  - For this circuit, the inputs and outputs are 4 bits long

We want you to find and submit the results of inputs that are not in the list (using the same format).

NB: No need to calculate for value 00000000

## Inputs
- message: [input.txt](./input.txt)

## Solution
There are only 2 types of circuits with 3 operators and 4 input bits (considering input bits can only be used once):
- OP1(OP2(a,b),OP3(c,d))
- OP1(a,OP2(b,OP3(c,d))

With (a,b,c,d) the input bits

We'll generate all possibilities with following python code:
```python
op = ["AND", "OR", "XOR"]
l = [[op1, op2, op3] for op1 in op for op2 in op for op3 in op]
circuits = list()

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
```

Then we need to test each of these against the inputs we have ! The idea is to maintain 4 lists of 'circuits', one list matching each output bit:
```python
circuits0 = circuits1 = circuits2 = circuits3 = circuits
```

Each list is updated after evaluating every single input line as follow (example for output bit0, but same is done for output bit1, bit2 and bit3). Note the dynamic evaluation of the circuit using the `eval` function:
```python
        # Extract individual bits from input value
        b0 = (_in >> 3) & 1
        b1 = (_in >> 2) & 1
        b2 = (_in >> 1) & 1
        b3 = (_in >> 0) & 1

        # Extract individual bits from output value
        out0 = (_out >> 3) & 1

        # Loop on all generated circuits to match the output bit0
        # Build a new list of circuits matching output bit0
        circuits_match0 = list()
        for c in circuits0:
            if (out0 == eval(c)):
                circuits_match0.append(c)
        circuits0 = circuits_match0
```

At the end, we get a list of circuits that match all the inputs. One list for each bit. Since we might have multiple circuits in each list, we simply pick up the first one for each bit:
```python
circuit = [circuits0[0], circuits1[0], circuits2[0], circuits3[0]]
```

Then we simply have to loop over value from 1 to 16 (0b1111) and write the output to a file, excluding the already known values (stored in `known_values`):
```python
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
```

We get this output:
```console
$ cat suite.txt
0010 : 1011
1101 : 1111
1111 : 0111

```

There is a trailing newline at the end that we need to remove before computing the `md5sum`:
```console
$ head -c -1 suite.txt | md5sum
18595d1d67910ccdfd833950f96c50c5  -

```

## Python code
Complete solution in [sol.py](sol.py)

## Flag
ECW{18595d1d67910ccdfd833950f96c50c5}
