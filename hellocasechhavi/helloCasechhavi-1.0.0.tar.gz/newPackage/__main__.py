import argparse


def main():
    # Initializing Parser
    parser = argparse.ArgumentParser(description='Hello World')
    # Adding Argument
    parser.add_argument("-u", "--upperr", type=str, nargs='+',
                        metavar="uppercase", default='', help="Uppercase")
    parser.add_argument("-l", "--lowerr", type=str, nargs='+',
                        metavar="lowercase", default='', help="Lowercase")
    args = parser.parse_args()
    for i in range(0, len(args.upperr)):
        if args.upperr != '':
            print(args.upperr[i].upper())
        if args.lowerr != '':
            print(args.lowerr[i].lower())


if __name__ == "__main__":
    main()
