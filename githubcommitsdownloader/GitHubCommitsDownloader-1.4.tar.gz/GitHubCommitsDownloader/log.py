class Colors:
	RED = "\033[1;31m"
	YELLOW = "\033[1;33m"
	GREEN = "\033[1;32m"
	BLUE = "\033[1;34m"
	PURPLE = "\033[1;35m"
	CYAN = "\033[1;36m"
	WHITE = "\033[1;37m"
	NONE = "\033[0m"


def log(mess, color, *options):
	print(f"{color}{mess}{Colors.NONE}", *options)