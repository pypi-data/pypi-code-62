import os
import colorama as col

if os.name == 'nt':
    col.init(autoreset = True, wrap = True)
else:
    col.init(autoreset = True)
if __name__ == '__main__':
    print("建造中...")