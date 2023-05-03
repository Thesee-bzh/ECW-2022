# Hardware / gates 3/3

## Challenge
We have a last one for you.

As a remember :
- Every output bit is determined separately
- The value of one output bit is the result of a logical equation using a series of AND, OR and XOR Gates
  - The number of gates for each output is fixed and equal to 5 Example : bit_0 AND bit_1 OR bit_2 AND bit_4 XOR bit_6 OR bit_7
- For each output bit, a given input bit is never used more than once
  - One input bit can be used for multiple output bits
  - One output bit does not use multiple times the same input bit
- The size of the input is equal to the size of the output
  - For this circuit, the inputs and outputs are 8 bits long

We want you to find and submit the results of inputs that are not in the list (using the same format).

NB: No need to calculate for value 00000000

## Inputs
- message: [inputs_outputs.txt](./inputs_outputs.txt)

## Solution
There are only 5 types of circuits with 5 operators and 8 input bits (considering input bits can only be used once):
- Starting with OP1(OP2(a,b),OP3(c,d)):
  - OP1(OP2(OP4(a,b),OP5(c,d)),OP3(e,f))
  - OP1(OP2(OP4(a,b),c),OP3(OP5(d,e),f))
  - OP1(OP2(OP4(OP5(a,b),c),d),OP3(e,f))
- Starting with OP1(a,OP2(b,OP3(c,d)):
  - OP1(a,OP2(b,OP3(c,OP4(d,OP5(e,f)))))
  - OP1(a,OP2(b,OP3(OP4(c,d),OP5(e,f))))

With (a,b,c,d,e,f) 6 of the 8 the input bits

Like in `gates 2/3`, We'll generate all possibilities with following python code:
```python
op = ["AND", "OR", "XOR"]
l = [[op1, op2, op3, op4, op5] for op1 in op for op2 in op for op3 in op for op4 in op for op5 in op]
circuits = list()

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
```

Then we need to test each these against the inputs we have ! The idea is to maintain 8 lists of 'circuits', one list matching each output bit. The process is exactly the same as in `gates 2/3`, except with have 8bits instead of 4.

It took a bit less than 20 minnutes and found a solution !

We get this output:
```console
$ head suite.txt
00000001 : 01010000
00000010 : 01110001
00000011 : 00110001
00000101 : 11110010
00000111 : 10110011
00001010 : 00111001
00001100 : 01101011
00001101 : 10111011
00001110 : 00111011
00010001 : 10111011
```

There is a trailing newline at the end that we need to remove before computing the `md5sum`:
```console
$ head -c -1 suite.txt | md5sum
c294c8123169b2a743c9701a1fcefe04  -

```

## Python code
Complete solution in [sol.py](sol.py)

## Flag
ECW{c294c8123169b2a743c9701a1fcefe04}
