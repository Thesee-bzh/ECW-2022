# Misc / jigsaw 2/3

## Challenge
Some questions will be asked. Can you win at this game ?

PS : You will have a limited time for each question.

## Inputs
- Docker instance

## Solution
This is the following of jigsaw 1/3.

Additional questions:

Question 5 is "5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas." For this one we change our implementation to store successive responses in a list, to easier crafting the response to this question 5, like so:
```python
    resp = resp_l[0] + b',' + resp_l[1] + b',' + resp_l[2] + b',' + resp_l[3]
```

Question 6 is "6. I did not understand. Can you repeat your previous answers for the following questions using the same format ?", with an example input like `[1, 3]`. Here we need to parse the input and I use Python's `eval()` to evaluate the input into a Python list, like so:
```python
    req_l = eval(req)  # to get a Python list
    resp = b''
    for i in range(len(req_l)):
        resp += resp_l[req_l[i] - 1]
        if (i != len(req_l) - 1):
            resp += b','
```

Question 7 is fun (just kidding):  "7. Random question time !" We're asked one of the previous questions, randomly. Here, the trick is to change our implementation so that we use function calls `q1()`, `q2()`, etc. to handle each question. The random question is identified using the starting number, defaulting to question 4 (baseN encoded question).

Here is the output of the interaction with the docker instance (removing the empty lines):

```console
$ python3 sol.py
[+] Opening connection to 213.32.7.237 on port 27603: Done
1. Do you want to play ?
yes
Try to answer to each question in less than 3 seconds
Next question
2. What is the name of the longest landing runway of the Rennes airport
10/28
Next question
3. Easy maths :
19*4
76
Next question
b'342E20496E2077686963682062617365207761732074686973207175657374696F6E20656E636F646564203F20202020'
16
Congratulations for the first steps. Your first flag is : ECW{EAS1ER_WITH_A_SCR1PT}
Next question
5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas.
yes,10/28,76,16
Next question
6. I did not understand. Can you repeat your previous answers for the following questions using the same format ? :
[1, 3]
yes,76
Next question
7. Random question time ! :
b'NC4gSW4gd2hpY2ggYmFzZSB3YXMgdGhpcyBxdWVzdGlvbiBlbmNvZGVkID8gICAgICAgICA='
64
Well done ! Here is your flag : ECW{B3TTER_WITH_FUNCT1ONS}
[*] Closed connection to 213.32.7.237 port 27603
```

## Python code
Complete solution in [sol.py](sol.py)

## Flag
ECW{B3TTER_WITH_FUNCT1ONS}
