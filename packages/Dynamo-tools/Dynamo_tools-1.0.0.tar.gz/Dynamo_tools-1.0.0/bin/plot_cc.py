#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 08:38:58 2021

@author: basnetn2
"""

import glob
import dynamotable
import matplotlib.pyplot as plt
import numpy as np
import argparse,pathlib

parser = argparse.ArgumentParser(description = 'This script gives you the histogram of the particle distribution accoriding to CC values in dynamo,needs dynamotable library')
parser.add_argument("--filename",type=pathlib.Path,help='name of dynamo table')
args = parser.parse_args()
names = args.filename


def main(names):
       table = dynamotable.read(names)
       hist_cc = np.array(table["cc"])
       bin_edge = np.arange(min(hist_cc),max(hist_cc),0.01)
       xtick = [round((x+0.005),2) for x in bin_edge]
       plt.hist(hist_cc,density=False,rwidth=0.8,bins=bin_edge,edgecolor='b')
       plt.ylabel('Number of particles')
       plt.xlabel('cc')
       plt.title('cc distribution')
       plt.xticks(xtick,rotation=90)
       plt.show()
       plt.savefig(f'{str(names).strip(".tbl")}.png')

if __name__ == "__main__":
      main(names)

