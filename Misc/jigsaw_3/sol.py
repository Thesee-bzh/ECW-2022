from pwn import *
from spellchecker import SpellChecker
import base64

HOST = "213.32.7.237"
PORT = 22377

WORDLIST = ['radial', 'clearance', 'prototype', 'porthole', 'eject', 'gyroscope', 'buoyancy', 'vibration', 'glider', 'oxygen', 'pallet', 'zeal', 'stabilizer', 'motion', 'aerodynamic', 'vector', 'aperture', 'cruise', 'insulation', 'aeronautics', 'accuracy', 'tail', 'squadron', 'hanger', 'tandem', 'engine', 'wing', 'throttle', 'pod', 'overshoot', 'terminal', 'operation', 'haul', 'thrust', 'cyclical', 'horizon', 'quiet', 'ballooning', 'ejection', 'captivate', 'nozzle', 'aisle', 'generate', 'taxi', 'antenna', 'attack', 'cockpit', 'acceleration', 'flight', 'principal', 'turbine', 'craft', 'cargo', 'flap', 'accommodation', 'intercept', 'inventor', 'ignition', 'elevation', 'flares', 'cabin', 'safety', 'biplane', 'range', 'superiority', 'radar', 'unmanned', 'turbulence', 'cylinder', 'sensors', 'torque', 'security', 'precautionary', 'control', 'launch', 'sync', 'supersonic', 'strike', 'propeller', 'lift', 'airstream', 'passenger', 'surveillance', 'piston', 'pom', 'airplane', 'autopilot', 'simulator', 'fuselage', 'takeoff', 'vertical', 'aircraft', 'transport', 'gunship', 'edge', 'battle', 'altitude', 'ids', 'nix', 'principle', 'rudder', 'ditch', 'maneuver', 'spoiler', 'provision', 'helicopter', 'navigation', 'flying', 'bap', 'tank', 'rocket', 'stealth', 'dirigible', 'signal', 'bay']

WORDLIST_INDEX = [[[0], [1, 4], [2], [3], [5]], [[0, 7], [1], [2, 8], [3, 5], [4], [6]], [[0, 7], [1], [2, 4], [3, 5], [6], [8]], [[0], [1, 5], [2], [3], [4], [6], [7]], [[0, 2], [1], [3], [4]], [[0], [1], [2], [3, 6], [4], [5], [7], [8]], [[0], [1], [2], [3, 7], [4], [5], [6]], [[0], [1, 6], [2], [3], [4], [5], [7], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2, 3], [4], [5]], [[0], [1], [2], [3]], [[0], [1], [2], [3], [4, 6], [5], [7], [8], [9]], [[0], [1, 4], [2], [3], [5]], [[0, 7], [1], [2], [3], [4], [5], [6], [8], [9], [10]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2, 7], [3, 6], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0, 7], [1, 9], [2], [3], [4], [5], [6], [8]], [[0, 5], [1], [2], [3], [4], [6], [7], [8], [9], [10]], [[0, 5], [1, 2, 6], [3], [4], [7]], [[0], [1], [2], [3]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0, 5], [1, 4], [2], [3]], [[0], [1], [2], [3]], [[0, 4, 5], [1], [2], [3], [6], [7]], [[0], [1], [2]], [[0, 6, 7], [1], [2], [3], [4], [5], [8]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0, 7], [1], [2], [3], [4], [5], [6], [8]], [[0], [1], [2], [3]], [[0, 5], [1], [2], [3], [4]], [[0, 2, 5], [1], [3, 7], [4], [6]], [[0], [1, 5], [2], [3], [4], [6]], [[0], [1], [2], [3], [4]], [[0], [1], [2, 3], [4, 5], [6, 8], [7], [9]], [[0, 2], [1], [3], [4], [5], [6], [7]], [[0], [1, 6], [2], [3, 7], [4], [5], [8]], [[0], [1], [2, 3], [4], [5]], [[0], [1], [2], [3], [4]], [[0], [1, 3, 7], [2], [4], [5], [6]], [[0], [1], [2], [3]], [[0, 6], [1, 4, 5], [2], [3]], [[0, 3], [1, 2], [4], [5]], [[0, 2], [1], [3], [4], [5], [6]], [[0, 7], [1, 2], [3, 5], [4], [6], [8], [9], [10], [11]], [[0], [1], [2], [3], [4], [5]], [[0, 6], [1], [2, 5], [3], [4], [7], [8]], [[0], [1], [2], [3], [4], [5], [6]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3]], [[0, 8], [1, 2], [3, 6, 11], [4, 5], [7], [9], [10], [12]], [[0], [1], [2, 8], [3, 6], [4], [5], [7]], [[0], [1, 4], [2], [3], [5], [6], [7]], [[0, 3, 5], [1], [2, 7], [4], [6]], [[0, 2], [1], [3], [4], [5], [6], [7], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5], [6]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3], [4, 7], [5, 8], [6], [9], [10]], [[0, 4], [1, 3], [2]], [[0], [1, 4, 5], [2], [3], [6], [7]], [[0], [1, 4], [2], [3], [5], [6, 9], [7], [8]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0, 3, 6], [1], [2], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0], [1, 11], [2], [3], [4, 10], [5], [6], [7], [8], [9], [12]], [[0], [1, 5], [2], [3], [4], [6]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3]], [[0, 5], [1], [2], [3], [4], [6], [7], [8], [9]], [[0], [1], [2], [3], [4], [5]], [[0, 3], [1, 8], [2], [4, 7], [5, 6]], [[0], [1], [2], [3]], [[0, 7], [1], [2, 5], [3], [4], [6], [8]], [[0], [1], [2, 3], [4, 7], [5], [6], [8]], [[0], [1], [2], [3], [4, 11], [5], [6, 7], [8], [9], [10]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2]], [[0, 5], [1], [2], [3], [4], [6], [7]], [[0], [1], [2, 8], [3, 7], [4], [5], [6]], [[0], [1], [2], [3], [4], [5], [6], [7], [8]], [[0], [1], [2], [3, 7], [4], [5], [6]], [[0], [1], [2], [3], [4], [5, 6]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0, 5], [1], [2, 4], [3], [6], [7]], [[0, 8], [1, 7], [2], [3], [4], [5], [6]], [[0], [1], [2], [3], [4], [5], [6]], [[0, 3], [1], [2]], [[0], [1], [2, 3], [4], [5]], [[0], [1], [2, 4], [3], [5], [6], [7]], [[0], [1], [2]], [[0], [1], [2]], [[0, 6], [1], [2, 5], [3], [4], [7], [8]], [[0, 5], [1], [2, 3], [4]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3, 6], [4], [5], [7]], [[0], [1], [2], [3], [4], [5], [6]], [[0], [1], [2, 7], [3], [4, 6], [5], [8]], [[0], [1, 8], [2], [3], [4], [5], [6], [7], [9]], [[0, 9], [1, 5], [2], [3, 7], [4], [6], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2]], [[0], [1], [2], [3]], [[0], [1], [2], [3], [4], [5]], [[0], [1, 5], [2], [3], [4], [6]], [[0], [1, 3, 5], [2], [4], [6], [7], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2]]]

#build_wordlist = True
build_wordlist = False

resp_l = list()

def compute_word_index_list(word):
    wl = list()
    for c in word:
        pos = [ i.start() for i in re.finditer(c, word) ]
        if pos not in wl:
            wl.append(pos)
    return wl

def generate_wordlist_index(wl):
    # Build list of char positions (still per word length)
    wl_pos = list()
    count = 0
    for word in wl:
        wl_pos.append([])
        wl_pos[count].append(compute_word_index_list(word))
        count += 1
    return wl_pos

def q1(random=False):
    q = b"1. Do you want to play ?"
    if not random:
        c.recvuntil(q); print(q.decode())
    resp = b"yes"
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q2(random=False):
    q = b"2. What is the name of the longest landing runway of the Rennes airport"
    if not random:
        c.recvuntil(q); print(q.decode())
    resp = b"10/28"
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q3(random=False):
    q = b"3. Easy maths"
    if not random:
        c.recvuntil(q); print(q.decode())
        c.recvline()
    req = c.recvline().strip()
    print(req.decode())
    resp = bytes(str(eval(req)), 'ascii')
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q4(random=False, q=None):
    # 4. In which base was this question encoded ?
    if not random:
        c.recvline()
        c.recvline()
        c.recvline()
        req = c.recvline().strip()
        print(req.decode())
    else:
        req = q
    if (b'NC4gSW4gd2' in req):
        resp = b'64'
    elif (b'342E20496E' in req):
        resp = b'16'
    elif (b'G%g@XZXkDP' in req):
        resp = b'85'
    else:
        resp = b'32'
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)

def q5(random=False):
    q = b"5. I forgot everything. Send me back your answers to questions 1 to 4, separated by commas."
    if not random:
        try:
            c.recvuntil(q); print(q.decode())
        except:
            return False
    resp = resp_l[0] + b',' + resp_l[1] + b',' + resp_l[2] + b',' + resp_l[3]
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)
    return True

def q6(random=False):
    q = b"6. I did not understand. Can you repeat your previous answers for the following questions using the same format ? :"
    if not random:
        try:
            c.recvuntil(q); print(q.decode())
        except:
            return False
        c.recvline()
    req = c.recvline().strip() # ex. [1, 3]
    print(req.decode())
    req_l = eval(req)  # to get a Python list
    resp = b''
    for i in range(len(req_l)):
        resp += resp_l[req_l[i] - 1]
        if (i != len(req_l) - 1):
            resp += b','
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)
    return True

def q7():
    q = b"7. Random question time ! :"
    try:
        c.recvuntil(q); print(q.decode())
    except:
        return False
    c.recvline()
    req = c.recvline()[1:].strip() # Skip the starting tab
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
    return True

def rot_encode(n):
    from string import ascii_lowercase as lc, ascii_uppercase as uc
    lookup = str.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return lambda s: s.translate(lookup)

def rot_decode(n):
    return rot_encode(-n)

def q8():
    q = b"8. I used a ROT cipher to encrypt a word from a list some times ago and I forgot the key. Can you tell me what word it was ?"
    try:
        c.recvuntil(q); print(q.decode())
    except:
        return False
    c.recvline()
    req = c.recvline().strip()
    print(req.decode())
    encoded = req.decode().strip()
    # ROT(n) decode for every possible n
    candidates = list()
    for n in range(1, 26):
        candidates.append(rot_decode(n)(encoded))
    # Setup the spellChecker (pyspellchecker)
    spell = SpellChecker()
    known = spell.known(candidates)
    if len(list(known)) == 0:
        return False
    resp = list(known)[0].encode()
    # Feed the wordlist with this decoded word !!!! (if we need to generate it)
    if build_wordlist:
        if resp not in WORDLIST:
            WORDLIST.append(resp)
    c.sendline(resp); print(resp.decode())
    resp_l.append(resp)
    return True

def q9():
    q = b"9. Do the same with this one, ciphered with a substitution cipher. Keep in mind you have 3 seconds :"
    try:
        c.recvuntil(q); print(q.decode())
    except:
        return False
    c.recvline()
    c.recvline()
    req = c.recvline().strip()
    print(req.decode())
    if (len(req) == 3):
        return True
    wl_pos = compute_word_index_list(req.decode())
    if wl_pos in WORDLIST_INDEX:
        pos = WORDLIST_INDEX.index(wl_pos)
        resp = WORDLIST[pos].encode()
        c.sendline(resp); print(resp.decode())
        resp_l.append(resp)
        return True
    else:
        return False

def decode_base_n(coded, base):
    candidate = None
    try:
        if base == 16:
            candidate = base64.b16decode(coded)
        elif base == 32:
            candidate = base64.b32decode(coded)
        elif base == 64:
            candidate = base64.b64decode(coded)
        elif base == 85:
            candidate = base64.b85decode(coded)
        else:
            return None
    except:
        candidate = None
        pass
    return candidate

def decode_bases(coded):
    candidate = None
    # Try various base(N) decodings: N = 16, 32, 64, 85
    bases = [ 16, 32, 64, 85]
    for base in bases:
        candidate = decode_base_n(coded, base)
        if candidate != None:
            if candidate.isalpha():
                print("BASE", base, candidate)
                return candidate
    if candidate == None:
        return False

def check_spell(candidates):
    # Setup the spellChecker (pyspellchecker)
    spell = SpellChecker()
    try:
        known = spell.known(candidates)
    except:
        return None
    if len(list(known)) == 0:
        return None
    return list(known)[0]

def q10():
    q = b"10. You should have the required skill for the last one. This one is very confidential, I might have reused 3 different methods from some previous questions to be sure it remains secret."
    try:
        c.recvuntil(q); print(q.decode())
    except:
        return False
    c.recvline()
    req = c.recvline().strip()
    req = req.decode()[2:][:-1]
    print(req)
    # b'Z3Rlb2RxbmRxbGg='
    # b'Z*6#N'
    # b'6D6C7479656E'
    # b'N5TG443HNZXXM2A='
    # b'cHJrYXJrYw=='
    # Step1 - Decode base N (of course N is unknown...)
    step1 = decode_bases(req)
    if step1 == None:
        return False
    # Check speller (if known word, try it...)
    candidates = list()
    candidates.append(step1)
    resp = check_spell(candidates)
    if resp != None:
        c.sendline(resp); print(resp.decode())
        resp_l.append(resp)
        return True
    # Step2 - Decode rot N (of course N is unknown...)
    candidates.clear()
    for n in range(1, 26):
        candidates.append(rot_decode(n)(step1.decode()))
    # Check speller (if known word, try it...)
    candidates.clear()
    candidates.append(step1.decode())
    step2 = check_spell(candidates)
    if step2 != None:
        resp = step2
        c.sendline(resp); print(resp.decode())
        resp_l.append(resp)
        return True
    # Step3 Decode substitution cipher
    if (len(step1) == 3):
        return True
    wl_pos = compute_word_index_list(step1.decode())
    if wl_pos in WORDLIST_INDEX:
        pos = WORDLIST_INDEX.index(wl_pos)
        resp = WORDLIST[pos].encode()
        c.sendline(resp); print(resp.decode())
        resp_l.append(resp)
    return True

def quizz():
    q1()
    q2()
    q3()
    q4()
    if q5() == False:
        return False
    if q6() == False:
        return False
    if q7() == False: # Q7: random question !
        return False
    if q8() == False:
        return False
    if q9() == False: # Q10: bruteforce
        return False
    return q10()

def main():
    global c # Burk...
    while True:
        c = remote(HOST, PORT)
        resp_l.clear()
        ret = quizz()
        if ret == True:
            return
        c.close()

#if not build_wordlist:
#    WORDLIST_INDEX = generate_wordlist_index(WORDLIST)

main()
print(c.recvline().decode())

