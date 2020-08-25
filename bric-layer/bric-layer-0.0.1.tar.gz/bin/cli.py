import argparse

from .create_new_bric import create_bric

# TODO - redo; extend bin options
# works for now
parser = argparse.ArgumentParser(description='Select command:')
parser.add_argument('-create_bric', '-c', metavar='create_bric',
                    help='Input name to create a new bric template')
parser.add_argument('--test', '-t',
                    help='test')

args = parser.parse_args()
print(args)
for arg in vars(args):
    value = getattr(args, arg)
    if arg == 'create_bric' and value is not None:
        create_bric(value)
