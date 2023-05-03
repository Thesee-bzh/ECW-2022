# Misc / jigsaw 1/3

## Challenge
Some questions will be asked. Can you win at this game ?

PS : You will have a limited time for each question.

## Inputs
- Docker instance

## Solution
We're asked a couple of questions. We use `pwntools` to script the interaction with the docker instance. Since the questions are of different nature, we build the script one question after the other.

Here is the output of the interaction with the docker instance (removing the empty lines):

```console
$ python3 sol.py                      
[+] Opening connection to 213.32.7.237 on port 23888: Done
1. Do you want to play ?
yes
Try to answer to each question in less than 3 seconds
Next question
2. What is the name of the longest landing runway of the Rennes airport
10/28
Next question
3. Easy maths :
11-12
-1
Next question
b'342E20496E2077686963682062617365207761732074686973207175657374696F6E20656E636F646564203F2020'
16
Congratulations for the first steps. Your first flag is : ECW{EAS1ER_WITH_A_SCR1PT}
Next question
[*] Closed connection to 213.32.7.237 port 23888
```

## Python code
Complete solution in [sol.py](sol.py)

## Flag
ECW{EAS1ER_WITH_A_SCR1PT}
