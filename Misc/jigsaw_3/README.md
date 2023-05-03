# Misc / jigsaw 3/3

## Challenge
Some questions will be asked. Can you win at this game ?

PS : You will have a limited time for each question.

## Inputs
- Docker instance

## Solution
This is the following of jigsaw 2/3.

Additional questions:

Question 8 is ""8. I used a ROT cipher to encrypt a word from a list some times ago and I forgot the key. Can you tell me what word it was ?"

We don't know the ROT offset, and experiencing a bit shows that it changes every time, so we need to bruteforce it but trying all 26 possibilities. Then, we use a spell checker (`pyspellchecker`) to determine the correct one (could be mutiple solutions for short words). With this, we're able to build the original wordlist by iterating many times ! Here's the python code:

```python
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
```

And here's the original wordlist we're able to reconstruct:
```python
WORDLIST = ['radial', 'clearance', 'prototype', 'porthole', 'eject', 'gyroscope', 'buoyancy', 'vibration', 'glider', 'oxygen', 'pallet', 'zeal', 'stabilizer', 'motion', 'aerodynamic', 'vector', 'aperture', 'cruise', 'insulation', 'aeronautics', 'accuracy', 'tail', 'squadron', 'hanger', 'tandem', 'engine', 'wing', 'throttle', 'pod', 'overshoot', 'terminal', 'operation', 'haul', 'thrust', 'cyclical', 'horizon', 'quiet', 'ballooning', 'ejection', 'captivate', 'nozzle', 'aisle', 'generate', 'taxi', 'antenna', 'attack', 'cockpit', 'acceleration', 'flight', 'principal', 'turbine', 'craft', 'cargo', 'flap', 'accommodation', 'intercept', 'inventor', 'ignition', 'elevation', 'flares', 'cabin', 'safety', 'biplane', 'range', 'superiority', 'radar', 'unmanned', 'turbulence', 'cylinder', 'sensors', 'torque', 'security', 'precautionary', 'control', 'launch', 'sync', 'supersonic', 'strike', 'propeller', 'lift', 'airstream', 'passenger', 'surveillance', 'piston', 'pom', 'airplane', 'autopilot', 'simulator', 'fuselage', 'takeoff', 'vertical', 'aircraft', 'transport', 'gunship', 'edge', 'battle', 'altitude', 'ids', 'nix', 'principle', 'rudder', 'ditch', 'maneuver', 'spoiler', 'provision', 'helicopter', 'navigation', 'flying', 'bap', 'tank', 'rocket', 'stealth', 'dirigible', 'signal', 'bay']
```

This will come handy for the next questions.

Question 9 is "9. Do the same with this one, ciphered with a substitution cipher. Keep in mind you have 3 seconds :". We don't know which substitution is applied, but we reconstructed the original wordlist, so we should be able to recognize what original word the substitution applied to. First original and substituted words share the same length, of course. Also, they share a common pattern regarding letter occurences (or letter index occurences).

Example: `xllepxlj`
- length 8: words of length 8 from the wordlist are the following: 'porthole', 'buoyancy', 'aperture', 'accuracy', 'squadron', 'throttle', 'terminal', 'cyclical', 'ejection', 'generate', 'inventor', 'ignition', 'unmanned', 'cylinder', 'security', 'airplane', 'fuselage', 'vertical', 'aircraft', 'altitude', 'maneuver'.
- one letter (`x`) is repeated twice at position/index [0, 5] and another one (`l`) is repeated three times at positions [1, 2, 6]: from the previous shortlist, only `accuracy` shares the same pattern.

So what we're going to do is build a list of letter positions/indexes for each word from our wordlist, which will act as a signature for that word. For instance `accuracy`/`xllepxlj` will share same signature `[[0, 5], [1, 2, 6], [3], [4], [7]]`. Then we just need to match a word from the wordlist with same length and signature.

Here's the code to generated the list of signatures:
```python
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

if not build_wordlist:
    WORDLIST_INDEX = generate_wordlist_index(WORDLIST)
```

And here's the generated list of signatures for the wordlist:
```python
WORDLIST_INDEX = [[[0], [1, 4], [2], [3], [5]], [[0, 7], [1], [2, 8], [3, 5], [4], [6]], [[0, 7], [1], [2, 4], [3, 5], [6], [8]], [[0], [1, 5], [2], [3], [4], [6], [7]], [[0, 2], [1], [3], [4]], [[0], [1], [2], [3, 6], [4], [5], [7], [8]], [[0], [1], [2], [3, 7], [4], [5], [6]], [[0], [1, 6], [2], [3], [4], [5], [7], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2, 3], [4], [5]], [[0], [1], [2], [3]], [[0], [1], [2], [3], [4, 6], [5], [7], [8], [9]], [[0], [1, 4], [2], [3], [5]], [[0, 7], [1], [2], [3], [4], [5], [6], [8], [9], [10]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2, 7], [3, 6], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0, 7], [1, 9], [2], [3], [4], [5], [6], [8]], [[0, 5], [1], [2], [3], [4], [6], [7], [8], [9], [10]], [[0, 5], [1, 2, 6], [3], [4], [7]], [[0], [1], [2], [3]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0, 5], [1, 4], [2], [3]], [[0], [1], [2], [3]], [[0, 4, 5], [1], [2], [3], [6], [7]], [[0], [1], [2]], [[0, 6, 7], [1], [2], [3], [4], [5], [8]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0, 7], [1], [2], [3], [4], [5], [6], [8]], [[0], [1], [2], [3]], [[0, 5], [1], [2], [3], [4]], [[0, 2, 5], [1], [3, 7], [4], [6]], [[0], [1, 5], [2], [3], [4], [6]], [[0], [1], [2], [3], [4]], [[0], [1], [2, 3], [4, 5], [6, 8], [7], [9]], [[0, 2], [1], [3], [4], [5], [6], [7]], [[0], [1, 6], [2], [3, 7], [4], [5], [8]], [[0], [1], [2, 3], [4], [5]], [[0], [1], [2], [3], [4]], [[0], [1, 3, 7], [2], [4], [5], [6]], [[0], [1], [2], [3]], [[0, 6], [1, 4, 5], [2], [3]], [[0, 3], [1, 2], [4], [5]], [[0, 2], [1], [3], [4], [5], [6]], [[0, 7], [1, 2], [3, 5], [4], [6], [8], [9], [10], [11]], [[0], [1], [2], [3], [4], [5]], [[0, 6], [1], [2, 5], [3], [4], [7], [8]], [[0], [1], [2], [3], [4], [5], [6]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3]], [[0, 8], [1, 2], [3, 6, 11], [4, 5], [7], [9], [10], [12]], [[0], [1], [2, 8], [3, 6], [4], [5], [7]], [[0], [1, 4], [2], [3], [5], [6], [7]], [[0, 3, 5], [1], [2, 7], [4], [6]], [[0, 2], [1], [3], [4], [5], [6], [7], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5], [6]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3], [4, 7], [5, 8], [6], [9], [10]], [[0, 4], [1, 3], [2]], [[0], [1, 4, 5], [2], [3], [6], [7]], [[0], [1, 4], [2], [3], [5], [6, 9], [7], [8]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0, 3, 6], [1], [2], [4], [5]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0], [1, 11], [2], [3], [4, 10], [5], [6], [7], [8], [9], [12]], [[0], [1, 5], [2], [3], [4], [6]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2], [3]], [[0, 5], [1], [2], [3], [4], [6], [7], [8], [9]], [[0], [1], [2], [3], [4], [5]], [[0, 3], [1, 8], [2], [4, 7], [5, 6]], [[0], [1], [2], [3]], [[0, 7], [1], [2, 5], [3], [4], [6], [8]], [[0], [1], [2, 3], [4, 7], [5], [6], [8]], [[0], [1], [2], [3], [4, 11], [5], [6, 7], [8], [9], [10]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2]], [[0, 5], [1], [2], [3], [4], [6], [7]], [[0], [1], [2, 8], [3, 7], [4], [5], [6]], [[0], [1], [2], [3], [4], [5], [6], [7], [8]], [[0], [1], [2], [3, 7], [4], [5], [6]], [[0], [1], [2], [3], [4], [5, 6]], [[0], [1], [2], [3], [4], [5], [6], [7]], [[0, 5], [1], [2, 4], [3], [6], [7]], [[0, 8], [1, 7], [2], [3], [4], [5], [6]], [[0], [1], [2], [3], [4], [5], [6]], [[0, 3], [1], [2]], [[0], [1], [2, 3], [4], [5]], [[0], [1], [2, 4], [3], [5], [6], [7]], [[0], [1], [2]], [[0], [1], [2]], [[0, 6], [1], [2, 5], [3], [4], [7], [8]], [[0, 5], [1], [2, 3], [4]], [[0], [1], [2], [3], [4]], [[0], [1], [2], [3, 6], [4], [5], [7]], [[0], [1], [2], [3], [4], [5], [6]], [[0], [1], [2, 7], [3], [4, 6], [5], [8]], [[0], [1, 8], [2], [3], [4], [5], [6], [7], [9]], [[0, 9], [1, 5], [2], [3, 7], [4], [6], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2]], [[0], [1], [2], [3]], [[0], [1], [2], [3], [4], [5]], [[0], [1, 5], [2], [3], [4], [6]], [[0], [1, 3, 5], [2], [4], [6], [7], [8]], [[0], [1], [2], [3], [4], [5]], [[0], [1], [2]]]
```

Resolving question 9 is just a matter of generating the signature for the substituted word and find a match in the list of signatures, like so:
```python
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
```

Question 10 is "10. You should have the required skill for the last one. This one is very confidential, I might have reused 3 different methods from some previous questions to be sure it remains secret."

Here are the different steps to apply:
- Step1 - Decode base N (of course N is unknown...)
- Check speller (if known word, try it...)
- Step2 - Decode rot N (of course N is unknown...)
- Check speller (if known word, try it...)
- Step3 Decode substitution cipher

We already have all the ingredients, we just need to piece them together:
```python
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
```

Also, we put the all quizz inside a loop, in case we fail an answer or something (see in the full script). Eventually, we get the flag!

## Python code
Complete solution in [sol.py](sol.py)

## Flag
ECW{EAS1ER_WITH_A_BR4IN}
