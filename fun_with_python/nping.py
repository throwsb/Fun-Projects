#!/usr/bin/env python3

import sys
import os
import argparse
import subprocess
import time
from configparser import ConfigParser

def run_nping():

    NPING = "/usr/bin/nping"
    NPG_OPTS = "-p 80 -q google.com"
    NPING_CMD = (NPING + " " + NPG_OPTS)

    print("NPING CMD", NPING, "OPTS",NPG_OPTS )
    print("CMD", NPING_CMD)

    print("Running nping ...")
    ##results = subprocess.run(NPING_CMD.split(), stdout=subprocess.PIPE)
    results = subprocess.run(NPING_CMD.split(), capture_output=True, text=True).stdout


    ##print(results.stdout)
    print(results)

def main():
	run_nping()

if __name__ == '__main__':
    main()