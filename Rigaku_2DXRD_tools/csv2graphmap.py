# -------------------------------------------------
# csv2graphmap.py
#
# Copyright (c) 2019, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
# -------------------------------------------------
# coding: utf-8

"""csv2graphmap.py

This module creates a visualization of a csv file
in FND(Formated Numerical Data) format.

Copyright (c) 2019, Data PlatForm Center, NIMS
This software is released under the MIT License.

Example
-------

    Parameters
    ----------
    inputfile : RIGAKU img csv file

    $ python csv2graphmap.py [inputfile]

"""
__package__ = "M-DaC_XRD/Rigaku_2DXRD_tools"
__version__ = "1.0.0"

import argparse
import os.path
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import matplotlib.font_manager as fm
fontprops = fm.FontProperties(size=18)
import matplotlib.ticker as ticker
from matplotlib_scalebar.scalebar import SI_LENGTH_RECIPROCAL
from matplotlib_scalebar.scalebar import SI_LENGTH

def getKey(key, row):
    if row[0] == key:
        return row[1]
    else:
        return 0

def scale_bar(anchor, pixel):
    baseWidth = anchor * pixel/3
    scaleValues = [1, 2, 3, 4, 5]
    oldWidth = 1
    factor = 1
    j = 0
    for t in range(20):
        scaleWidth = scaleValues[j] * factor
        if baseWidth > scaleWidth:
            j = j + 1
            oldWidth = scaleWidth
            if j >= len(scaleValues):
                j = 0
                factor = factor * 10
        else:
            scaleWidth = oldWidth
            if scaleWidth > baseWidth:
                scaleWidth = scaleWidth / 2;
    return scaleWidth

parser = argparse.ArgumentParser()
parser.add_argument("file_path")
parser.add_argument("--encoding", default="utf_8")
parser.add_argument("--jupytermode", help="for jupyter mode", action="store_true")
parser.add_argument("--scale", nargs=3, type=float)
parser.add_argument("--unit", nargs=3)
options = parser.parse_args()
readfile = options.file_path
jupytermode = options.jupytermode
scale_option = options.scale
unit_option = options.unit
name, ext = os.path.splitext(readfile)
axis = []
with open(readfile, 'r') as f:
    reader = csv.reader(f)
    line = 1
    xrevFlag = False
    yrevFlag = False
    for row in reader:
        if len(row) != 0:
            line += 1
            key = getKey('#title', row)
            if (key != 0):
                title = key
            key = getKey('#image_size', row)
            if (key != 0):
                image_size = row[:]
                image_size.pop(0)
                pixel_width = image_size[0]
                pixel_height = image_size[1]
            key = getKey('#image_step', row)
            if (key != 0):
                image_step = row[:]
                image_step.pop(0)
                pixel_step_x = image_step[0]
                pixel_step_y = image_step[1]
            key = getKey('#image_step_unit', row)
            if (key != 0):
                image_step_unit = row[:]
                image_step_unit.pop(0)
                width_unit = image_step_unit[0]
                height_unit = image_step_unit[1]
            key = getKey('#dimension', row)
            if (key != 0):
                axis = row[:]
                axis.pop(0)
                dimension = len(axis)
            key = getKey('#dim_axis', row)
            if (key != 0):
                dim_option = row[:]
                dim_option.pop(0)
            if len(axis) > 0:
                key = getKey('#'+axis[0], row)
                if key != 0:
                    xaxis = row[1]
                    if len(row) > 2:
                        xaxis = xaxis + "(" + row[2] + ")"
                    if len(row) > 3:
                        if row[3] == 'reverse':
                            xrevFlag = True
                key = getKey('#'+axis[1], row)
                if key != 0:
                    yaxis = row[1]
                    if len(row) > 2:
                        yaxis = yaxis + "(" + row[2] + ")"
                    if len(row) > 3:
                        if row[3] == 'reverse':
                            yrevFlag = True
        else:
            break
df = pd.read_csv(readfile, header=None, delimiter=',',skiprows=line)
df = df.dropna(axis=0, how='all')
df = df.dropna(axis=1)
df.reset_index(drop=True, inplace=True)
command = 'csvtographmap.py '+name+ext
width = 1.0 * float(pixel_step_x) * float(pixel_width)
height = 1.0 * float(pixel_step_y) * float(pixel_height)
dx = float(width)/int(pixel_width)
dimension = SI_LENGTH

if isinstance(unit_option, list):
    width_unit = unit_option[0]
    height_unit = unit_option[1]

if '/' in  width_unit:
    dimension = SI_LENGTH_RECIPROCAL

if isinstance(scale_option, list):
    width = 1.0 * scale_option[0] * float(pixel_width)
    height = 1.0 * scale_option[1] * float(pixel_height)
    brightness_scale = float(scale_option[2])
    command = command +' --scale '+str(scale_option[0])+' '+str(scale_option[1])+' '+str(scale_option[2])
    dx = scale_option[0]
    if '/' in  width_unit:
        df = df ** brightness_scale
        df = df.fillna(0)
        dimension = SI_LENGTH_RECIPROCAL
    else:
        df = df.applymap(lambda x: x * brightness_scale)
        df = df.fillna(0)

if isinstance(unit_option, list):
    command = command +' --unit '+str(unit_option[0])+' '+str(unit_option[1])+' '+str(unit_option[2])

scalebar = ScaleBar(dx, width_unit, dimension, color='white', frameon=False, location=4)
maxColumn = len(df.columns)
plt.imshow(df)
plt.gray()
ax = plt.gca()
ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))

x_label = str(width) + ' ' + width_unit + '\n(' + pixel_width + 'pixel)'
y_label = str(height) + ' ' + height_unit + '\n(' + pixel_height + 'pixel)'
ax.annotate(y_label, xy=(0.98, 0), xytext=(-20,-20), ha='left', va='top', xycoords='axes fraction', textcoords='offset pixels')
ax.annotate(x_label, xy=(0, 1), xytext=(-30,40), ha='left', va='top', xycoords='axes fraction', textcoords='offset pixels')
ax.add_artist(scalebar)
length = 35
if len(title) > length:
    string = title[:length] + '...'
else:
    string = title
plt.title(string)
ax.set_yticks([])
ax.set_xticks([])
writefile = name + '.png'
if jupytermode == True:
    plt.show()
plt.savefig(writefile)
plt.close()
