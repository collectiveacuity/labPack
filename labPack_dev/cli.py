__author__ = 'rcj1492'
__created__ = '2016.03'

'''
https://docs.python.org/3.5/library/argparse.html?highlight=argparse#module-argparse
'''
'''
from optparse import OptionParser

import sys

def main(argv):
    module_args = {
        'description': 'A sample command line input parser.',
        'version': '%prog 0.1.0',
        'usage': '%prog COMMAND [options]'
    }
    parser = OptionParser(**module_args)
    def error_msg(err):
        print('Errr! %s\n' % err)
        cliInput(['%prog','-h'])
        sys.exit(2)
    parser.error = error_msg
    parser.add_option(
        "-f", "--file",
        dest="filename", default="", help="write report to FILE",
        metavar="FILE"
    )
    parser.add_option(
        "-q", "--quiet",
        dest="verbose", default=True, help="don't print status messages to stdout",
        action="store_false"
    )
    parser.add_option(
        "-g", "--group",
        dest="gid", default="", help="group id for billing"
    )
    parser.add_option(
        "strings",
        metavar='N', type=int, nargs='+',
        help='an integer for the accumulator'
    )
    options, args = parser.parse_args(argv)
    print(options)
    print(args)

if __name__ == "__main__":
    main(sys.argv[1:])
'''
'''
import sys, getopt

def main(argv):
    # wait for user input
    line = input('Enter a sentence: ')
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,'hi:o:',['ifile=','ofile='])
    except getopt.GetoptError:
        print('Invalid arguments\nTry -h or -help.')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is %s' % inputfile)
    print('Output file is %s' % outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
'''

import sys
from argparse import ArgumentParser

def start(**kwargs):
    print(kwargs)

def stop(**kwargs):
    print(kwargs)

def pause(**kwargs):
    print(kwargs)

def cli(argv):

# construct main module
    module_args = {
        'description': 'A sample command line input parser.',
        'epilog': '%(prog)s can also make coffee.',
        'usage': '%(prog)s command [options]'
    }
    parser = ArgumentParser(**module_args)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')

# replace stderr message with help output
    def error_msg(err):
        print('Errr! %s\n' % err)
        cli(['-h'])
        sys.exit(2)
    parser.error = error_msg

# construct sub-command methods
    subparsers = parser.add_subparsers(title='sub-commands', help='sub-command help')

# define start sub-command & options
    start_args = {
        'usage': 'cli.py start [options]',
        'description': 'initiates the program',
        'help': 'initiates the program'
    }
    parser_start = subparsers.add_parser('start', **start_args)
    parser_start.set_defaults(func=start, command='start')
    parser_start.add_argument(
        "-q", "--quiet", default=True,
        dest="verbose", help="don't print status messages to stdout (default: %(default)s)",
        action="store_false"
    )
    parser_start.add_argument(
        "-g", "--group", type=int, default=1,
        dest="gid", help="group id %(type)s for billing (default: %(default)s)"
    )

# define stop sub-command & options
    stop_args = {
        'usage': 'cli.py stop [options]',
        'description': 'terminates the program',
        'help': 'terminates the program'
    }
    parser_stop = subparsers.add_parser('stop', **stop_args)
    parser_stop.set_defaults(func=stop, command='stop')
    parser_stop.add_argument(
        "-f", "--file", type=str, default='',
        dest="filename", help="write log report to FILE",
        metavar="FILE"
    )

# define pause sub-command
    pause_args = {
        'usage': 'cli.py pause [options]',
        'description': 'pauses the program',
        'help': 'pauses the program'
    }
    parser_pause = subparsers.add_parser('pause', **pause_args)
    parser_pause.set_defaults(func=pause, command='pause')

# call parsing function and print output as dictionary
    args = parser.parse_args(argv)
    opt_dict = vars(args)
    args.func(**opt_dict)

if __name__ == "__main__":
    cli(sys.argv[1:])