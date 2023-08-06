#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 17:55:14 2021

@author: basnetn2
"""

import starfile
import pandas as pd
import numpy as np
import argparse,pathlib

parser = argparse.ArgumentParser(description = 'This script helps you create a relion descr .star file')
parser.add_argument("--filename",type=pathlib.Path,help='text file containing tomogram number and tomogram name')
parser.add_argument("--base",type=str,help='Basename of tomogram directory')
parser.add_argument("--directory",type=str,help='name of tomogram directory')

args = parser.parse_args()
names = args.filename
basename = args.base
direct = args.directory


def main(names,basename,direct):
    tomograms = np.loadtxt(names,dtype=str,delimiter=None)
    
    tomolist = list(tomograms[:,0])
    name = list(tomograms[:,1])
    
    data = {}
    
    TomoName = [f'{basename}_{i}'for i in tomolist]
    TomoSeriesName = [f'{direct}/{basename}_{i}/{name[int(i)-1]}.mrc' for i in tomolist]
    TomoImportCtfFindFile = [f'{direct}/{basename}_{i}/{name[int(i)-1]}_output.txt' for i in tomolist]
    TomoImportImodDir = [f'{direct}/{basename}_{i}'for i in tomolist]
    TomoImportFractionalDose = [f'{direct}/{basename}_{i}/{name[int(i)-1]}_dose.csv' for i in tomolist]
    TomoImportOrderList = [f'{direct}/{basename}_{i}/{name[int(i)-1]}_order.csv' for i in tomolist]
    
    
    data['rlnTomoName'] = TomoName
    data['rlnTomoTiltSeriesName'] = TomoSeriesName
    data['rlnTomoImportCtfFindFile'] = TomoImportCtfFindFile
    data['rlnTomoImportImodDir'] = TomoImportImodDir
    data['rlnTomoImportFractionalDose'] = TomoImportFractionalDose
    data['rlnTomoImportOrderList'] = TomoImportOrderList
    
    df = pd.DataFrame.from_dict(data)
    
    starfile.write(df,'Tomo_descr.star',overwrite=True)
    




if __name__ == "__main__":
      main(names,basename,direct)




