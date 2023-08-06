These are general tools that I repeatedly used while doing subtomogram averaging in dynamo.

1) make_table.py

This creates dynamo table for given tomograms using the coordinates of particle that you picked using other software like IMOD.
You have two option of creating table, one is general(dynamo convention) when particles are scatterd over the tomogram(for eg. ribosomes) and the other is 
filamnet(Microtubules or actin). For filamnet a initial euler angles are determined according to their orientation in tomogram and twist angle for each subunits.
This will provide a good starting point and will reduce the need of large angular search during golbal alignment.
 

usage: make_table.py [--filename FILENAME] [--filament FILAMENT]
                     [--binning BINNING] [--output_file OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --filename    coordinate file, column seoarated by space,
  --filament    if the points your picking is filamnet like MT or actin otherwise give 0
                        
  --binning     provide  binning factor if you picked particels in binned tomograms
                        
  --output_file name of the output file
                        
2) split_table.py

Normally dynamo table contains the coordinates and alignment parameter for allt eh tomograms and sometime you might need the table for each tomogram.
I needed it when I wanted to plot the points in Chimera for visualization. You need this indices_column_20.doc file to keep track of tomograms in dynamo table.
It is found inside the data folder or folder where you cropped the particles.

usage: split_table.py [--filename FILENAME] [--indice_file INDICE_FILE]
                      [--binning BINNING]



optional arguments:

  --filename    Table file that you want to split
  --indice_file  indices_column20.doc is a index file that relates each tomogram to the tablle.This is present inside the data directory(where you cropped your particle)
                                               
  --binning      if you wnat to bin while extracting the coordinates
  
  
  
3) recenter.py
After initial round of alignemnt sometime you want to recenter the particles or remove the shifht that is calculated during alignemnt and re-pick particles and
start refinement.

usage: recenter.py [--filename FILENAME]

--filename  name of dynamo table


4)plot_cc.py
During refinement you want to check the distribution of particles CC values to see if you can filter the particle based on low CC during refinement.
This module will plot the CC histogram to give you the basic idea.

usage: plot_cc.py [-h] [--filename FILENAME]
--filename  name of dynamo table

5) relion_make_descr.py
this will create a decr.star file for you tomograms which is required as input in relion 4.0
you tomogram folder name should be (rlnTomoName) [string]_[number] for e.g. TS_01. i would suggest to make folder for each tomograms like that and number 01,02,..,
following same order as indices_20.doc or your dynamo table. You can use library relion2dynamo to convert the dynmao table to relion particle set.
[pip install relion2dynamo].
you can use this and the descr.sar file generated here as input to transfer form dynamo to relion 4.0

Most of the time inside the the real tomogram name could be different rather than the convention followed byt relion, you can give that name in the text file as input.
example tomograms.txt

Be careful of the zeroes inf ront of the numbers.

make sure you copy all the required files from the IMOD directory.

Since I use dose symmetric to collect data, I provided the dose for each tomogram in a text file.


I follow the directiory organization as suggestied in Relion documentation



usage: relion_make_descr.py [--filename FILENAME] [--base BASE] [--directory DIRECTORY]
                            
optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME   text file containing tomogram number and tomogram name
  --base BASE           Basename of tomogram directory
  --directory           name of tomogram directory
                        