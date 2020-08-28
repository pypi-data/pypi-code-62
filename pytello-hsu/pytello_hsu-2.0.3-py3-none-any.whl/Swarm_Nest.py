import socket
import threading


class drone:
    def __init__(self, ip):
        self.host = ''
        self.port = 9000
        self.locaddr = (self.host, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tello_address = (ip, 8889)
        self.sock.bind(self.locaddr)
        self.count = 0

    def send(self, msg):
        try:
            if not msg:
                return
            if 'end' in msg:
                print('...')
                self.sock.close()
                return
            msg = msg.encode(encoding="utf-8")
            sent = self.sock.sendto(msg, self.tello_address)
        except KeyboardInterrupt:
            print('\n . . .\n')
            self.sock.close()
            return

    def ipconfig(self, x):
        x = str(x)
        self.tello_address = (x, 8889)

    def recv(self):
        self.count = 0
        while True:
            try:
                data, server = self.sock.recvfrom(1518)
                print(data.decode(encoding="utf-8"))
            except Exception:
                print('\nExit . . .\n')
                break

    def takeoff(self):
        self.send("takeoff")

    def land(self):
        self.send("land")

    def command(self):
        self.send("command")

    def eland(self):
        self.send("emergency")

    def up(self, x):
        self.send("up " + x)

    def down(self, x):
        self.send("down " + x)

    def left(self, x):
        self.send("left " + x)

    def right(self, x):
        self.send("right " + x)

    def forward(self, x):
        self.send("forward " + x)

    def backward(self, x):
        self.send("back " + x)

    def clockwise(self, degrees):
        self.send("cw " + degrees)

    def counterclockwise(self, degrees):
        self.send("ccw " + degrees)

    def flip(self, direction):
        self.send("flip " + direction)

    def speed(self, x):
        self.send("speed " + x)

    def init(self):
        self.command()
        recvthread = threading.Thread(target=self.recv)
        recvthread.start()
