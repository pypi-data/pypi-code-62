def wait():
		import termios, fcntl, sys, os
		fd = sys.stdin.fileno()
		flags_save = fcntl.fcntl(fd, fcntl.F_GETFL)
		attrs_save = termios.tcgetattr(fd)
		attrs = list(attrs_save) 
		attrs[0] &= ~(termios.IGNBRK | termios.BRKINT | termios.PARMRK
									| termios.ISTRIP | termios.INLCR | termios. IGNCR
									| termios.ICRNL | termios.IXON )
		attrs[1] &= ~termios.OPOST
		attrs[2] &= ~(termios.CSIZE | termios. PARENB)
		attrs[2] |= termios.CS8
		attrs[3] &= ~(termios.ECHONL | termios.ECHO | termios.ICANON
									| termios.ISIG | termios.IEXTEN)
		termios.tcsetattr(fd, termios.TCSANOW, attrs)
		fcntl.fcntl(fd, fcntl.F_SETFL, flags_save & ~os.O_NONBLOCK)
		ret = []
		try:
				ret.append(sys.stdin.read(1))
				fcntl.fcntl(fd, fcntl.F_SETFL, flags_save | os.O_NONBLOCK)
				c = sys.stdin.read(1)
				while len(c) > 0:
						ret.append(c)
						c = sys.stdin.read(1)
		except KeyboardInterrupt:
				ret.append('\x03')
		finally:
				termios.tcsetattr(fd, termios.TCSAFLUSH, attrs_save)
				fcntl.fcntl(fd, fcntl.F_SETFL, flags_save)
		return tuple(ret)