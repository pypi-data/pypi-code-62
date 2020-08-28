from sys import argv
from time import strftime
from getopt import getopt, GetoptError
from nmap import PortScanner


def version():

    print("+-----------------------------------------------------------------------------------+")
    print("| Pyscan. Copyright (C) 2020 BrainDisassembly, Contact: braindisassm@gmail.com      |")
    print("| Version: 1.0.0                                                                    |")
    print("|                                                                                   |")
    print("| This program comes with ABSOLUTELY NO WARRANTY; for details type `show w`.        |")
    print("| This is free software, and you are welcome to redistribute it                     |")
    print("| under certain conditions; type `show c` for details.                              |")
    print("+-----------------------------------------------------------------------------------+")


def usage():

    print("Pyscan 1.0.0 [Python Scanner]")
    print("Written by: BrainDisassembly <braindisassm@gmail.com>\n")

    print("Usage: {0} --ip 192.168.1.0 --prt 21-443".format(argv[0]))

    print("\nOptions:")
    print("  -h: --help                           Print usage and exit.")
    print("  -V: --version                        Print version information and exit.")
    print("  -i: --ip                             IP to scan.")
    print("  -p: --prt                            Ports to scan.")

def pyscan():

    print("---------------------------------------------")
    print("[+] Starting at: ({0})".format(strftime("%c")))
    print("---------------------------------------------")

    nm = PortScanner()
    nm.scan(ip, prt)

    for host in nm.all_hosts():
        print("[+] Host : ({0}) ({1})".format(host, nm[host].hostname()))
        print("[+] State : ({0})".format(nm[host].state()))

        for proto in nm[host].all_protocols():
            print("[+] Protocol : ({0})\n".format(proto))

            lport = nm[host][proto].keys()
            lport.sort()

            for port in lport:
                print("[+] Port : {0}\tState : ({1})".format(port, nm[host][proto][port]['state']))

    print("---------------------------------------------")
    print("[+] Finished at: ({0})".format(strftime("%c")))
    print("[+] Exiting...")
    print("---------------------------------------------")


def main():

    global ip
    ip = ""

    global prt
    prt = ""

    try:
        opts, args = getopt(argv[1:], "hVi:p:", ["help", "version", "ip=", "prt="])

    except GetoptError: usage()

    else:
        try:
            for opt, arg in opts:
                if opt in ("-h", "--help"): usage(); exit(1)
                if opt in ("-V", "--version"): version(); exit(1)
                if opt in ("-i", "--ip"): ip = arg
                if opt in ("-p", "--prt"): prt = arg

            if ip and prt: pyscan()

            else:
                usage()

        except (UnboundLocalError):
            pass

        except (TypeError):
            pass


if __name__ == "__main__":
        main()
