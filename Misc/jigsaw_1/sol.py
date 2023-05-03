from pwn import *

HOST = "213.32.7.237"
PORT = 23888

c = remote(HOST, PORT)

# 1. Do you want to play ?
print(c.recvuntil(b"1. Do you want to play ?").decode())
resp = b"yes"
c.sendline(resp); print(resp.decode())

# 2. What is the name of the longest landing runway of the Rennes airport
print(c.recvuntil(b"2. What is the name of the longest landing runway of the Rennes airport").decode())
resp = b"10/28"
c.sendline(resp); print(resp.decode())

# 3. Easy maths
print(c.recvuntil(b"3. Easy maths :").decode())
print(c.recvline().decode())
req = c.recvline()
print(req.decode())
resp = bytes(str(eval(req)), 'ascii')
c.sendline(resp); print(resp.decode())

# 4. In which base was this question encoded ?
print(c.recvline().decode())
print(c.recvline().decode())
print(c.recvline().decode())
req = c.recvline()
print(req.decode())
if (b'NC4gSW4gd2' in req):
    resp = b'64'
elif (b'342E20496E' in req):
    resp = b'16'
elif (b'G%g@XZXkDP' in req):
    resp = b'8'
else:
    resp = b'32'
c.sendline(resp); print(resp.decode())

print(c.recvline().decode())
print(c.recvline().decode())
print(c.recvline().decode())
print(c.recvline().decode())
