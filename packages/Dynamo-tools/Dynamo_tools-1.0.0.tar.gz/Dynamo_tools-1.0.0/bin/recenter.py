#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 08:57:20 2021

@author: basnetnirakar

This script recenters the translational shift present in particle after allignment in dynamo
"""

import numpy as np
import argparse,pathlib

parser = argparse.ArgumentParser(description = 'This script recenters the translational shift present in particle after allignment in dynamo')
parser.add_argument("--filename",type=pathlib.Path,help='name of dynamo table')
args = parser.parse_args()
names = args.filename

def main(names):
      tomo=np.loadtxt(names,delimiter=None,dtype ='str')
      #name = str(names)
      tomo[:,23:26] = tomo[:,23:26].astype('float32') + tomo[:,3:6].astype('float32')
      tomo[:,3:6] = 0
      np.savetxt(f'{str(names).strip(".tbl")}_centered.tbl',tomo,fmt = '%s', delimiter = " ")

if __name__ == "__main__":
      main(names)