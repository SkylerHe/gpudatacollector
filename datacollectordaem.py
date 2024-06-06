# -*- coding: utf-8 -*-

import os
import sys

# Standard imports.

import argparse
import json
import random
import shutil
import signal
import time

# Imports from UR's hpclib.

from   dorunrun import dorunrun, ExitCode
import linuxutils
from   sqlitedb import SQLiteDB
from   urdecorators import show_exceptions_and_frames as trap

###
# Credits
###
__author__ = 'Skyler He'
__copyright__ = 'Copyright 2024'
__credits__ = 'George Flanagin'
__version__ = 1.0
__maintainer__ = 'Skyler He'
__email__ = ['yingxinskyler.he@gmail.com', 'skyler.he@richmond.edu']

#################################################
# This program has a lot of static data
#################################################

caught_signals = [  signal.SIGINT, signal.SIGQUIT,
                    signal.SIGUSR1, signal.SIGUSR2, signal.SIGTERM ]

                        
db_handle = None
##################################################
# Intercept signals and die gracefully
##################################################
def handler(signum:int, stack:object=None) -> None:
    """
    Universal signal handler.
    """
    if signum == signal.SIGHUP:
        return

    if signum in caught_signals:
        try:
            db_handle.commit()
            db_handle.db.close()
        except Exception as e:
            sys.stderr.write(f"Error on exit {e}\n")
            sys.exit(os.EX_IOERR)
        else:
            sys.exit(os.EX_OK)
    else:
        return


def dither_time(t:int) -> int:
    """
    Avoid measuring the power at regular intervals.
    """
    lower = int(t * 0.95)
    upper = int(t * 1.05)
    while True:
        yield random.randint(lower, upper)    


@trap
def datacollectordaem_main(myargs:argparse.Namespace) -> int:
    """
    This function collects gpu data from all workstations and output the result to SQLite3
    """
    global db_handle

    # dither_time
    n=0
    dither_iter = dither_time(myargs.freq)

    while n < myargs.n:
        result = collect_gpu_data()
        
        insert_data(data)
        n += 1
        time.sleep(next(dither_iter))
    
    return os.EX_OK
    

if __name__=='__main__':

    ################################################################
    # Make sure we can press control-C to leave if we are running
    # interactively. Otherwise, handle it.
    ################################################################
    os.isatty(0) and caught_signals.remove(signal.SIGINT)

    parser = argparse.ArgumentParser(prog='datacollectordaem', 
        description='Skeleton of collecting gpu data')
    
    parser.add_argument('-f', '--freq', type=int, default=300,
        help='number of seconds between polls (default:300)')
    parser.add_argument('--db', type=str, default='power.db',
        help='name of database (default:"power.db")')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='be chatty')
    parser.add_argument('-n', type=int, default=sys.maxsize,
        help="For debugging, limit number of readings (default:unlimited)")

    myargs = parser.parse_args()
    linuxutils.dump_cmdline(myargs)
    linuxutils.setproctitle('veryhungrycluster')

    for _ in caught_signals:
        try:
            signal.signal(_, handler)
        except OSError as e:
            myargs.verbose and sys.stderr.write(f"Cannot reassign signal {_}\n")
        else:
            myargs.verbose and sys.stderr.write(f"Signal {_} is being handled.\n")

    exit_code = ExitCode(veryhungrycluster_main(myargs))
    print(exit_code)
    sys.exit(int(exit_code))
    
