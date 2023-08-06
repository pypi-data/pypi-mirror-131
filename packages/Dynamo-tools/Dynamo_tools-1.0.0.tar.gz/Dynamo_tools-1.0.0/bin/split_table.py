#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 09:30:05 2021

@author: basnetn2
"""

import numpy as np
import argparse,pathlib

parser = argparse.ArgumentParser(description='it will split dynamo table to table for each tomograms')
parser.add_argument("--filename",type=pathlib.Path,help='Table file that you want to split')
parser.add_argument("--indice_file",type=pathlib.Path, help='indices_column20.doc is a index file that relates each tomogram to the tablle.This is present inside the data directory(where you cropped your particle)')
parser.add_argument("--binning",type=int,default=1)


args = parser.parse_args()
names = args.filename
index = args.indice_file
binf = args.binning

def main(names,index,binf):
      tomo_info = np.loadtxt(index,dtype = 'str', delimiter = None)
      tomo=np.loadtxt(names,delimiter=None,dtype ='str')
      tomo[:,23:26] = tomo[:,23:26].astype('float32')/binf
      tomo[:,3:6] = tomo[:,3:6].astype('float32')/binf
      for i in tomo_info:
            tomo_table = tomo[tomo[:,19]==i[0]]
            np.savetxt(f'{i[1].split("/")[-1].strip(".mrc")}.tbl',tomo_table,fmt='%s')

if __name__ == "__main__":
      main(names,index,binf)

