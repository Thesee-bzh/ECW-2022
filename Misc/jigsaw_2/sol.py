from pwn import *

HOST = "213.32.7.237"
PORT = 27603

c = remote(HOST, PORT)

resp_l  = list()

def q1(random=False):
    # 1. Do you want to play ?
    if not random:
        print(c.recvuntil(b"1. Do you want to play ?").decode())
    resp = b"yes"
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q2(random=False):
    # 2. What is the name of the longest landing runway of the Rennes airport
    if not random:
        print(c.recvuntil(b"2. What is the name of the longest landing runway of the Rennes airport").decode())
    resp = b"10/28"
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q3(random=False):
    # 3. Easy maths
    if not random:
        print(c.recvuntil(b"3. Easy maths :").decode())
        print(c.recvline().decode())
    req = c.recvline()
    print(req.decode())
    resp = bytes(str(eval(req)), 'ascii')
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q4(random=False, q=None):
    # 4. In which base was this question encoded ?
    if not random:
        print(c.recvline().decode())
        print(c.recvline().decode())
        print(c.recvline().decode())
        req = c.recvline()
        print(req.decode())
    else:
        req = q
    if (b'NC4gSW4gd2' in req):
        resp = b'64'
    elif (b'342E20496E' in req):
        resp = b'16'
    elif (b'G%g@XZXkDP' in req):
        resp = b'128' # Doesn't work ?..
    else:
        resp = b'32'
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q5(random=False):
    # 5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas
    if not random:
        print(c.recvuntil(b"5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas.").decode())
    resp = resp_l[0] + b',' + resp_l[1] + b',' + resp_l[2] + b',' + resp_l[3]
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q6(random=False):
    # 6. I did not understand. Can you repeat your previous answers for the following questions using the same format ?
    if not random:
        print(c.recvuntil(b"6. I did not understand. Can you repeat your previous answers for the following questions using the same format ? :").decode())
        print(c.recvline().decode())
    req = c.recvline() # ex. [1, 3]
    print(req.decode())
    req_l = eval(req)  # to get a Python list
    resp = b''
    for i in range(len(req_l)):
        resp += resp_l[req_l[i] - 1]
        if (i != len(req_l) - 1):
            resp += b','
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def random():
    # 7. Random question time ! :
    print(c.recvuntil(b"7. Random question time ! :").decode())
    print(c.recvline().decode())
    req = c.recvline()[1:] # Skip the starting tab
    print(req.decode())
    # Identify the random question by the starting number
    # If no starting number, default to question 4 (baseN encoded question)
    q = req.decode()[0]
    if q == '1':
        q1(random=True)
    elif q == '2':
        q2(random=True)
    elif q == '3':
        q3(random=True)
    elif q == '5':
        q5(random=True)
    elif q == '6':
        q6(random=True)
    else:
        q4(random=True, q=req)

# First sequence: non-random questions
q1()
q2()
q3()
q4()
q5()
q6()
# Second sequence: random questions !
random()

print(c.recvline().decode())
print(c.recvline().decode())
print(c.recvline().decode())

