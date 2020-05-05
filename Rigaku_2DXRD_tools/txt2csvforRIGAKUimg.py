# -------------------------------------------------
# txt2csvforRIGAKUimg.py
#
# Copyright (c) 2019, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
# -------------------------------------------------
# coding: utf-8
#__author__ = "nagao"

"""txt2csvforRIGAKUimg.py

This module creates a formatted numerical data
by creating a text version of the RIGAKU imgfile.

Copyright (c) 2019, Data PlatForm Center, NIMS
This software is released under the MIT License.

Example
-------

    Parameters
    ----------
    inputfile : RIGAKU text file
        Measurement data file measured by RIGAKU
    outputfile : output csv file

    $ python txt2csvforRIGAKUimg.py [inputfile] [outputfie]

"""
import argparse
import csv
import itertools
import io
import os.path
import codecs
import numpy
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="input file")
    options = parser.parse_args()
    readfile = options.file_path
    basename = os.path.basename(readfile)
    name, ext = os.path.splitext(basename)
    flag = 0
    head = 0
    prefix = ""
    acqdate = ""
    description = name + ext
    writefile = name + '.csv'
    with open(writefile, 'w', encoding='utf-8') as f2:
        with codecs.open(readfile, 'r', 'utf-8') as f:
            for line in f:
                line = line.strip()
                if flag == 0:
                    if line.find('Numeric Data') > -1:
                        flag = 1
                    else:
                        key = line.split(':')
                        if key[0].find('DETECTOR_NAMES') > -1:
                            prefix = key[1]
                        if key[0].find('FILENAME') > -1:
                            description = key[1]
                        if key[0].find('SIZE1') > -1:
                            pixel_y = key[1]
                        if key[0].find('SIZE2') > -1:
                            pixel_x = key[1]
                        if key[0].find(prefix + 'DETECTOR_SIZE') > -1:
                            value = key[1].split(' ')
                            x_scale_value = value[1]
                            y_scale_value = value[0]
                        if key[0].find('XY_STAGE_UNITS') > -1:
                            value = key[1].split(' ')
                            x_unit = value[1]
                            y_unit = value[0]
                        if key[0].find(prefix + 'CREATE_DATETIME') > -1:
                            acqdate = line
                            prefix_date = prefix + "CREATE_DATETIME:"
                            acqdate = acqdate.replace(prefix_date,"")
                        if key[0].find('COMMENT') > -1:
                            comment = key[1]
                else:
                    if head == 0:
                        x_scale = float(x_scale_value) / float(pixel_x)
                        y_scale = float(y_scale_value) / float(pixel_y)
                        f2.write('##This text data file is converted by Fabio.\n')
                        f2.write('#title,'+description + '\n')
                        f2.write('#type,image\n')
                        f2.write('#dimension,x,y\n')
                        f2.write('#x,abscissa\n')
                        f2.write('#y,ordinate\n')
                        f2.write('#legend\n')
                        f2.write('#image_size,'+ pixel_x + ',' + pixel_y + '\n')
                        f2.write('#image_step,'+ str(x_scale) + ',' + str(y_scale) + '\n')
                        f2.write('#image_step_unit,'+ x_unit + ',' + y_unit + '\n')
                        f2.write('##acq_date,'+ acqdate + '\n')
                        f2.write('##comment,' + comment + '\n\n')
                        itemList = line.split(',')
                        n_array = list(map(int, itemList))
                        n_array = numpy.array(n_array, dtype=numpy.int)
                        df = pd.Series(n_array)
                        df = df.fillna(0)
                        n_array = df.tolist()
                        itemList = ["%d" % x for x in n_array]
                        itemList = ','.join(itemList)
                        f2.write(itemList+'\n')
                        head = 1
                    else:
                        itemList = line.split(',')
                        n_array = list(map(int, itemList))
                        n_array = numpy.array(n_array, dtype=numpy.int)
                        df = pd.Series(n_array)
                        df = df.fillna(0)
                        n_array = df.tolist()
                        itemList = ["%d" % x for x in n_array]
                        itemList = ','.join(itemList)
                        f2.write(itemList+'\n')
