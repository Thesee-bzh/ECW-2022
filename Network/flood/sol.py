#!/usr/bin/python3

def get_cred(value):
    previous_index = 0
    previous_packet = ""
    cred = ""
    with (open('packets.txt', 'r') as f):
        for packet in f:
            if value in packet:
                index = int(packet.split("users),")[1].split(",")[0])
                if (previous_packet != ""):
                    c = previous_packet.split("'")[2]
                    if (index != previous_index and previous_index != 33):
                        cred += c
                previous_index = index
                previous_packet = packet
    return cred
        

print("username", get_cred("username"))
print("password", get_cred("password"))

# username maverick
# password bb9a36b4bd5b42600d8c36e19cc857db

# ECW{162.210.198.131_maverick_bb9a36b4bd5b42600d8c36e19cc857db}
