#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 10:06:14 2021

@author: basnetn2
"""

import numpy as np
import math
import argparse,pathlib



parser = argparse.ArgumentParser(description = 'This script helps you create a dynamo table from the coordinate text file that could be generated from other programs like IMOD')
parser.add_argument("--filename",type=pathlib.Path,help='coordinate file, column seoarated by space,')
parser.add_argument("--filament",type=int,help='if the points your picking is filamnet like MT or actin otherwise give 0')
parser.add_argument("--binning",type=int,default=1,help='givie binning factor if you picked particels in binned tomograms')
parser.add_argument("--output_file",type=str,help='name of the output file')

args = parser.parse_args()
names = args.filename
filament = args.filament
output = args.output_file
binf = args.binning


def directional_vector(coordinates):
    """
    calculates the directional vector between two points

    Parameters
    ----------
    coordinates : array
        coordinates with filament ID

    Returns
    -------
    array: composed of directional vector

    """
    
    arr = np.array([coordinates[:,0],coordinates[:,1],coordinates[:,2]]).swapaxes(1,0)
    d_vector = np.empty([0,3])
    count = 0
    l = len(arr)
    for x, y in enumerate(arr):
        if count < l-1:
            vector = np.array(arr[x+1]-y).reshape(1,3)
            print(vector,y)
        d_vector = np.append(d_vector,vector,axis=0)
        count += 1


    return d_vector


def angle_betn_vectors(v1,v2):
      """
      Calculates the angle between two vector

      Parameters
      ----------
      v1 : 1 d array 
            Directional vector
      v2 : 1d array
            for xy plane it will be (1,1,0)

      Returns
      -------
      angle in degrees

      """
      dot_product = v1.dot(v2)
      norms = np.linalg.norm(v1)*np.linalg.norm(v2)
      return np.rad2deg(np.arccos(dot_product/norms))


def angle_plane(vector_array,V2=[0,1,0]):

    """
    calculates the angle and magnitude of the given directional vector
    Parameters
    ----------
    vector_array : array
        directional vector

    Returns
    -------
    array: magnitude, angle in degrees
    

    """

    magnitude = []
    angle = []
    for v in vector_array:
        mag = math.sqrt((v[0])**2+(v[1])**2+(v[2]**2))
        degree=angle_betn_vectors(v, V2)
        magnitude.append(mag)
        angle.append(degree)

    return angle


def read_coordinates(array,ID):
      X =  int(input('Enter the column index for X coordinates(index starts from 0): '))
      Y =  int(input('Enter the column index for Y coordinates(index starts from 0): '))
      Z =  int(input('Enter the column index for Z coordinates(index starts from 0): '))
      if ID==True:
            filament_ID = int(input('Enter the column index for filament ID(index starts from 0): '))
            coordinates = np.array([array[:,filament_ID],array[:,X],array[:,Y],array[:,Z]]).swapaxes(1,0)
      else:
            coordinates = np.array([array[:,X],array[:,Y],array[:,Z]]).swapaxes(1,0)

      return coordinates



def main(names,filament,binf,output):
      data = np.loadtxt(names, dtype=float, delimiter=None)
      mintilt = input('Enter the minimum tilt: ')
      maxtilt = input('Enter the maximum tilt: ')
      length = len(data)
      table = np.zeros([length,35])
      tag = np.linspace(1,length,endpoint=True,num=length,dtype=int)
      table[:,0]=tag
      table[:,1] = 1
      table[:,2] = 1
      table[:,13] = mintilt  #input
      table[:,14] = maxtilt# input
      table[:,15] = mintilt
      table[:,16] = maxtilt
      table[:,12] = 1

      if filament==1:
            phi = int(input('Enter the angular twist of the subunits in degrees: '))
            ID = True
            coordi = read_coordinates(data,ID)
            filament = int(coordi[:,0][-1])
            coord_table = np.empty([0,4])
            for i in range(1,filament+1):
                  coord = coordi[coordi[:,0]==i]
                  sort = np.array(sorted(coord, key=lambda x : x[1]))
                  coord_table = np.append(coord_table,sort,axis=0)
            table[:,23:26] = coord_table[:,0:3]*binf   #input
            table[:,21] = coordi[:,0]
            drot =[]
            angular_rot = []
            #y_plane = np.array([0,1,0])
            for i in range(1,filament+1):
                  arr = table[table[:,21]==i]
                  coords = arr[:,23:26]
                  dir_arr = directional_vector(coords)
                  angles = angle_plane(dir_arr)
                  arot = [angles[0]]
                  for i in range(1,len(angles)):
                        rot = arot[i-1]+phi
                        if abs(rot) > 180:
                              if rot  > 0:
                                    new_rot = 360-rot
                              else:
                                    new_rot = rot+360
                              arot.append(new_rot)
                        else:
                              arot.append(rot)
                  angular_rot.append(arot)
                  drot.append(angles)
            
            
            drot = [x for i in drot for x in i]
            angular_rot = [x for i in angular_rot for x in i]
            
            table[:,6]=drot
            table[:,8]= angular_rot
            table[:,7] = 90
            final_table = table[table[:,6].astype(str) != 'nan']
            new_index = np.linspace(1,len(final_table),len(final_table),endpoint=True)
            final_table[:,0] = new_index
      else:
            ID = False
            coordi = read_coordinates(data,ID)
            table[:,23:26] = coordi[:,0:3]*binf
            final_table = table


      np.savetxt(output,final_table,fmt='%s',delimiter=' ')


if __name__ == "__main__":
      main(names,filament,binf,output)
