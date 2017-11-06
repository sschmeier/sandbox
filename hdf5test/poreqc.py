#!/usr/bin/env python
"""
NAME: poreqc.py
===============

DESCRIPTION
===========

INSTALLATION
============

USAGE
=====

VERSION HISTORY
===============

{{version}}   {{date}}    Initial version.

LICENCE
=======
2017, copyright {{author}} ({{email}}), {{url}}

template version: 1.8 (2017/10/06)
"""
from signal import signal, SIGPIPE, SIG_DFL
import sys
import os
import os.path
import argparse
import csv
import collections
import gzip
import bz2
import zipfile
import time
import h5py
import numpy as np

# When piping stdout into head python raises an exception
# Ignore SIG_PIPE and don't throw exceptions on it...
# (http://docs.python.org/library/signal.html)
signal(SIGPIPE, SIG_DFL)

__version__ = 'v0.1'
__date__ = '2017/10/30'
__email__ = 's.schmeier@gmail.com'
__author__ = 'Sebastian Schmeier'


# For color handling on the shell
try:
    from colorama import init, Fore, Style
    # INIT color
    # Initialise colours for multi-platform support.
    init()
    reset=Fore.RESET
    colors = {'success': Fore.GREEN, 'error': Fore.RED, 'warning': Fore.YELLOW, 'info':''}
except ImportError:
    sys.stderr.write('colorama lib desirable. Install with "conda install colorama".\n\n')
    reset=''
    colors = {'success': '', 'error': '', 'warning': '', 'info':''}

def alert(atype, text, log):
    textout = '%s [%s] %s\n' % (time.strftime('%Y%m%d-%H:%M:%S'),
                                atype.rjust(7),
                                text)
    log.write('%s%s%s' % (colors[atype], textout, reset))
    if atype=='error': sys.exit()
        
def success(text, log=sys.stderr):
    alert('success', text, log)
    
def error(text, log=sys.stderr):
    alert('error', text, log)
    
def warning(text, log=sys.stderr):
    alert('warning', text, log)
    
def info(text, log=sys.stderr):
    alert('info', text, log)  

    
def parse_cmdline():
    """ Parse command-line args. """
    ## parse cmd-line -----------------------------------------------------------
    description = 'Read delimited file.'
    version = 'version %s, date %s' % (__version__, __date__)
    epilog = 'Copyright %s (%s)' % (__author__, __email__)

    parser = argparse.ArgumentParser(description=description, epilog=epilog)

    parser.add_argument('--version',
                        action='version',
                        version='%s' % (version))

    parser.add_argument(
        'str_file',
        metavar='FILE',
        help=
        'Delimited file. [if set to "-" or "stdin" reads from standard in]')
    parser.add_argument('-d',
                        '--delimiter',
                        metavar='STRING',
                        dest='delimiter_str',
                        default='\t',
                        help='Delimiter used in file.  [default: "tab"]')
    parser.add_argument('-o',
                        '--out',
                        metavar='STRING',
                        dest='outfile_name',
                        default=None,
                        help='Out-file. [default: "stdout"]')

    # if no arguments supplied print help
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    return args, parser


def main():
    """ The main funtion. """
    args, parser = parse_cmdline()

    try:
        f5 = h5py.File(args.str_file, "r")
    except:
        error('Could not load file. EXIT.')

    # create outfile object
    if not args.outfile_name:
        outfileobj = sys.stdout
    elif args.outfile_name in ['-', 'stdout']:
        outfileobj = sys.stdout
    elif args.outfile_name.split('.')[-1] == 'gz':
        outfileobj = gzip.open(args.outfile_name, 'wb')
    else:
        outfileobj = open(args.outfile_name, 'w')

    # some info
    #TRACKING_ID = "/UniqueGlobalKey/tracking_id"
    #for k,v in f5[TRACKING_ID].attrs.items():
    #    print('%s\t%s'%(k,str(v)))

    #CONTEXT_TAGS = "/UniqueGlobalKey/context_tags"
    #for k,v in f5[CONTEXT_TAGS].attrs.items():
    #    print('%s\t%s'%(k,str(v)))

    ## Raw read signal
    #RAW_READS = '/Raw/Reads/'
    #read_subgroup = []
    #f5[RAW_READS].visit(read_subgroup.append)
    #print(read_subgroup)
    #for k,v in f5['%s/%s'%(RAW_READS, read_subgroup[0])].attrs.items():
    #    print('%s\t%s'%(k,str(v)))

    
    # FASTQ
    #FASTQ = 'Analyses/Basecall_1D_000/BaseCalled_template/Fastq'
    #print(f5[FASTQ])

    #from pandas import read_hdf
    #hdf = read_hdf(args.str_file)
    #print(hdf)

    # print all groups and attr.
    f5.visititems(print_attrs_for_all_group)

    # ------------------------------------------------------
    outfileobj.close()
    return


def print_attrs_for_all_group(name, obj):
    print(name)
    for key, val in obj.attrs.items():
        print("\t%s: %s" % (key, val))



if __name__ == '__main__':
    sys.exit(main())

