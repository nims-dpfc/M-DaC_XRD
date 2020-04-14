# -------------------------------------------------
# RIGAKU_img2txt.py
#
# Copyright (c) 2019, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
# -------------------------------------------------
# coding: utf-8
"""RIGAKU_img2txt.py

This module creates a formatted numerical data
by creating a text version of the RIGAKU imgfile.

Copyright (c) 2019, Data PlatForm Center, NIMS
This software is released under the MIT License.

Example
-------

    Parameters
    ----------
    inputfile : RIGAKU img binary file
        Measurement data file measured by RIGAKU

    $ python RIGAKU_img2txt.py [inputfile]

"""
import argparse
import os.path
import fabio

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", help="input file")
    options = parser.parse_args()
    readfile = options.file_path
    basename = os.path.basename(readfile)
    name, ext = os.path.splitext(basename)
    img = fabio.open(readfile)
    outputfile = name + '.txt'
    with open(outputfile, 'w', encoding="utf-8", newline="\n") as f:
        f.write("//This text data file is converted by Fabio.\n")
        f.write("//HEADER INFORMATION\n")
        for key, value in img.header.items():
            temp = key + ':' + value + "\n"
            f.write(temp)
        f.write("\n//Numeric Data\n")
        for a in img.data:
            print(*a, sep=",", file = f)
