cap = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alph = "abcdefghijklmnopqrstuvwxyz"

def decap(text):
    output = ""
    for i in text:
        if i in cap:
            output += alph[cap.index(i)]
        else:
            output += i
    return output
