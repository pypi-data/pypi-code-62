import socket
import threading
host = ''
port = 9000
locaddr = (host, port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)


def send(msg):
    try:
        if not msg:
            return
        if 'end' in msg:
            print('...')
            sock.close()
            return
        msg = msg.encode(encoding="utf-8")
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()
        return


def ipconfig(x):
    global tello_address
    x = str(x)
    tello_address = (x, 8889)


def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print('\nExit . . .\n')
            break


def takeoff():
    send("takeoff")


def land():
    send("land")


def command():
    send("command")


def eland():
    send("emergency")


def up(x):
    send("up " + x)


def down(x):
    send("down " + x)


def left(x):
    send("left " + x)


def right(x):
    send("right " + x)


def forward(x):
    send("forward " + x)


def backward(x):
    send("back " + x)


def clockwise(degrees):
    send("cw " + degrees)


def counterclockwise(degrees):
    send("ccw " + degrees)


def flip(direction):
    send("flip " + direction)


def speed(x):
    send("speed " + x)


def init():
    command()
    recvthread = threading.Thread(target=recv)
    recvthread.start()
