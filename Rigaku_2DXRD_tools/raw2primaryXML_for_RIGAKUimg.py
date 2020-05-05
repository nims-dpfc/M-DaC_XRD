# -------------------------------------------------
# raw2primaryXML_for_RIGAKUimg.py
#
# Copyright (c) 2019, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
# -------------------------------------------------
# coding: utf-8
#__author__ = "nagao"

"""raw2primaryXML_for_RIGAKUimg.py

This module extracts primary parameter from
RIGAKU img raw file.

Copyright (c) 2019, Data PlatForm Center, NIMS
This software is released under the MIT License.

Example
-------

    Parameters
    ----------
    inputfile : RIGAKU img raw file
    templatefile : template file for RIGAKU img primary parameter
    outputfile : output file (primary parameter (XML))

    $ python raw2primaryXML_for_RIGAKUimg.py [inputfile] [templatefile] [outputfile]

"""
import argparse
import xml.dom.minidom
import re
import xml.etree.ElementTree as ET
from datetime import datetime
import codecs


def registdf(key, channel, value, metadata, unitlist, template, prefix_key):
    column = key
    value_unit = ""
    tempflag = 1
    if column not in columns:
        tempflag = 0
    if tempflag == 1:
        if value is not None:
            arrayvalue = value.split()
            unitcolumn = template.find('meta[@key="{value}"][@unit]'.format(value=key))
            transition = 0
            if unitcolumn is not None:
                value = arrayvalue[0] 
                if key == "SOURCE_WAVELENGTH":
                    value_unit = unitcolumn.get("unit")
                    value = arrayvalue[1]
                elif key == "CRYSTAL_GONIO_VALUE1":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_VALUES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[0]
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_UNITS"]').text
                    tempvalue = temp.split()
                    value_unit = tempvalue[0]
                elif key == "CRYSTAL_GONIO_VALUE2":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_VALUES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[1]
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_UNITS"]').text
                    tempvalue = temp.split()
                    value_unit = tempvalue[1]
                elif key == "CRYSTAL_GONIO_VALUE3":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_VALUES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[2]
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_UNITS"]').text
                    tempvalue = temp.split()
                    value_unit = tempvalue[2]
                elif key == "DETECTOR_SIZE_X":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_SIZE"]').text
                    tempvalue = temp.split()
                    value = tempvalue[0]
                    value_unit = unitcolumn.get("unit")
                elif key == "DETECTOR_SIZE_Y":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_SIZE"]').text
                    tempvalue = temp.split()
                    value = tempvalue[1]
                    value_unit = unitcolumn.get("unit")
                elif key == "GONIO_VALUE2":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_GONIO_VALUES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[1]
                    text = prefix_key
                    prefix_unit = re.sub('VALUES$',"UNITS",text)
#                    print ("####",text_mod)
                    temp = rawdata.find('meta[@key="' + prefix_unit + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_GONIO_UNITS"]').text
                    tempvalue = temp.split()
                    value_unit = tempvalue[1]
                elif key == "GONIO_VALUE6":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_GONIO_VALUES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[5]
                    text = prefix_key
                    prefix_unit = re.sub('VALUES$',"UNITS",text)
                    temp = rawdata.find('meta[@key="' + prefix_unit + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_GONIO_UNITS"]').text
                    tempvalue = temp.split()
                    value_unit = tempvalue[5]
                elif key == "X_STAGE_VALUE":
                    temp = rawdata.find('meta[@key="XY_STAGE_VALUES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[0]
                    temp = rawdata.find('meta[@key="XY_STAGE_UNITS"]').text
                    tempvalue = temp.split()
                    value_unit = tempvalue[0]
                elif key == "Y_STAGE_VALUE":
                    temp = rawdata.find('meta[@key="XY_STAGE_VALUES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[1]
                    temp = rawdata.find('meta[@key="XY_STAGE_UNITS"]').text
                    tempvalue = temp.split()
                    value_unit = tempvalue[1]
                elif key == "PIXEL_SIZE_X":
#                    print("!!=",prefix_key)
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_SIZE"]').text
                    tempvalue = temp.split()
                    size = rawdata.find('meta[@key="SIZE1"]').text
                    value = float(tempvalue[0]) / float(size)
                    value_unit = unitcolumn.get("unit")

                elif key == "PIXEL_SIZE_Y":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_SIZE"]').text
                    tempvalue = temp.split()
                    size = rawdata.find('meta[@key="SIZE2"]').text
                    value = float(tempvalue[1]) / float(size)
                    value_unit = unitcolumn.get("unit")
                else:
                    value_unit = unitcolumn.get("unit")
            else:
                if key == "Year" or key == "Month" or key == "Day":
                    date = value.split(" ")
                    dt = datetime.strptime(date[0], '%Y/%m/%d')
                    if key == "Year":
                        value = dt.year
                    elif key == "Month":
                        value = "{0:02d}".format(dt.month)
                    elif key == "Day":
                        value = "{0:02d}".format(dt.day)
                elif key == "CRYSTAL_GONIO_NAME1":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_NAMES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[0]
                elif key == "CRYSTAL_GONIO_NAME2":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_NAMES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[1]
                elif key == "CRYSTAL_GONIO_NAME3":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_NAMES"]').text
                    tempvalue = temp.split()
                    value = tempvalue[2]
                elif key == "CRYSTAL_GONIO_VECTOR1":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + str(int(float(tempvalue[0]))) + " " + str(int(float(tempvalue[1]))) + " " + str(int(float(tempvalue[2]))) + ")"
                elif key == "CRYSTAL_GONIO_VECTOR2":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + str(int(float(tempvalue[3]))) + " " + str(int(float(tempvalue[4]))) + " " + str(int(float(tempvalue[5]))) + ")"
                elif key == "CRYSTAL_GONIO_VECTOR3":
                    temp = rawdata.find('meta[@key="CRYSTAL_GONIO_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + str(int(float(tempvalue[6]))) + " " + str(int(float(tempvalue[7]))) + " " + str(int(float(tempvalue[8]))) + ")"
                elif key == "DETECTOR_DIMENSION_X":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_DIMENSIONS"]').text
                    tempvalue = temp.split()
                    value = tempvalue[0]
                elif key == "DETECTOR_DIMENSION_Y":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_DIMENSIONS"]').text
                    tempvalue = temp.split()
                    value = tempvalue[1]
                elif key == "DETECTOR_VECTOR_X":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + tempvalue[0] + " " + tempvalue[1] + " " + tempvalue[2] + ")"
                elif key == "DETECTOR_VECTOR_Y":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_DETECTOR_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + tempvalue[3] + " " + tempvalue[4] + " " + tempvalue[5] + ")"
                elif key == "SPATIAL_BEAM_POSITION_X":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_SPATIAL_BEAM_POSITION"]').text
                    tempvalue = temp.split()
                    value = tempvalue[0]
                elif key == "SPATIAL_BEAM_POSITION_Y":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_SPATIAL_BEAM_POSITION"]').text
                    tempvalue = temp.split()
                    value = tempvalue[1]
                elif key == "GONIO_VECTOR2":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_GONIO_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + str(int(float(tempvalue[3]))) + " " + str(int(float(tempvalue[4]))) + " " + str(int(float(tempvalue[5]))) + ")"
                elif key == "GONIO_VECTOR6":
                    temp = rawdata.find('meta[@key="' + prefix_key + '"]').text
#                    temp = rawdata.find('meta[@key="PXD_GONIO_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + str(int(float(tempvalue[15]))) + " " + str(int(float(tempvalue[16]))) + " " + str(int(float(tempvalue[17]))) + ")"
                elif key == "X_STAGE_VECTOR":
                    temp = rawdata.find('meta[@key="XY_STAGE_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + tempvalue[0] + " " + tempvalue[1] + " " + tempvalue[2] + ")"
                elif key == "Y_STAGE_VECTOR":
                    temp = rawdata.find('meta[@key="XY_STAGE_VECTORS"]').text
                    tempvalue = temp.split()
                    value = "(" + tempvalue[3] + " " + tempvalue[4] + " " + tempvalue[5] + ")"

            subnode = dom.createElement('meta')
            subnode.appendChild(dom.createTextNode(str(value)))
            subnode_attr = dom.createAttribute('key')
            subnode_attr.value = column
            subnode.setAttributeNode(subnode_attr)
            metadata.appendChild(subnode)

            if len(value_unit) > 0:
                subnode_attr = dom.createAttribute('unit')
                subnode_attr.value = value_unit
                subnode.setAttributeNode(subnode_attr)
                metadata.appendChild(subnode)
                unitlist.append(key)

            subnode_attr = dom.createAttribute('type')
            typename = template.find('meta[@key="{value}"]'.format(value=key))
            if typename.get("type") is not None:
                subnode_attr.value = typename.get("type")
            else:
                subnode_attr.value = "String"
            subnode.setAttributeNode(subnode_attr)
            metadata.appendChild(subnode)

            if channel != 0:
                subnode_attr = dom.createAttribute('column')
                subnode_attr.value = channel
                subnode.setAttributeNode(subnode_attr)
                metadata.appendChild(subnode)

            if transition == 1:
                subnode = dom.createElement('meta')
                subnode.appendChild(dom.createTextNode(str(value2)))
                subnode_attr = dom.createAttribute('key')
                subnode_attr.value = "Transitions"
                subnode.setAttributeNode(subnode_attr)
                metadata.appendChild(subnode)

                subnode_attr = dom.createAttribute('type')
                typename = template.find('meta[@key="Transitions"]')
                if typename.get("type") is not None:
                    subnode_attr.value = typename.get("type")
                else:
                    subnode_attr.value = "String"
                subnode.setAttributeNode(subnode_attr)
                metadata.appendChild(subnode)

                if channel != 0:
                    subnode_attr = dom.createAttribute('column')
                    subnode_attr.value = channel
                    subnode.setAttributeNode(subnode_attr)
                    metadata.appendChild(subnode)

                transition = 0

        return metadata


def regist(column, key, rawdata, metadata, channel, value, unitlist, template):
    if column in rawcolumns:
        registdf(key, channel, value, metadata, unitlist, template, column)
    return metadata


def conv(column, temp_name, rawdata, metadata, channel, unitlist, template):
    if channel == 0:
        metadata = regist(column, temp_name, rawdata, metadata, 0, rawdata.find('meta[@key="{value}"]'.format(value=column)).text, unitlist, template)
    else:
        for node in rawdata.findall('meta[@key="{value}"]'.format(value=column)):
            columnnum = node.attrib.get('column')
            metadata = regist(column, temp_name, rawdata, metadata, columnnum, node.text, unitlist, template)
    return(metadata)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path")
    parser.add_argument("template_file")
    parser.add_argument("out_file")
    parser.add_argument("--stdout", action="store_true")
    options = parser.parse_args()
    readfile = options.file_path
    templatefile = options.template_file
    outputfile = options.out_file
    print_option = options.stdout
    channel = 0
    rawdata = ET.parse(readfile)
    rawcolumns = []
    rawmetas = rawdata.findall('meta')
    for meta in rawmetas:
        rawcolumns.append(meta.attrib["key"])
    rawcolumns = list(set(rawcolumns))
    template = ET.parse(templatefile)
    columns = []
    metas = template.findall('meta')
    for meta in metas:
        columns.append(meta.attrib["key"])
    dom = xml.dom.minidom.Document()
    metadata = dom.createElement('metadata')
    dom.appendChild(metadata)
    count = 0

    metalist = {"Year": "%DETECTOR_NAMES%_CREATE_DATETIME",
                "Month": "%DETECTOR_NAMES%_CREATE_DATETIME",
                "Day": "%DETECTOR_NAMES%_CREATE_DATETIME",
                "HEADER_BYTES": "HEADER_BYTES",
                "BYTE_ORDER":"BYTE_ORDER",
                "SIZE1":"SIZE1",
                "SIZE2":"SIZE2",
                "Data_type":"Data_type",
                "FILENAME":"FILENAME",
                "DTDISPLAY_ORIENTATION":"DTDISPLAY_ORIENTATION",
                "SOURCE_WAVELENGTH":"SOURCE_WAVELENGTH",
                "SOURCE_AMPERAGE":"SOURCE_AMPERAGE",
                "SOURCE_VOLTAGE":"SOURCE_VOLTAGE",
                "SOURCE_FOCUS":"SOURCE_FOCUS",
                "CRYSTAL_GONIO_NUM_VALUES":"CRYSTAL_GONIO_NUM_VALUES",
                "CRYSTAL_GONIO_NAME1":"CRYSTAL_GONIO_NAMES",
                "CRYSTAL_GONIO_VECTOR1":"CRYSTAL_GONIO_VECTORS",
                "CRYSTAL_GONIO_VALUE1":"CRYSTAL_GONIO_VALUES",
                "CRYSTAL_GONIO_NAME2":"CRYSTAL_GONIO_NAMES",
                "CRYSTAL_GONIO_VECTOR2":"CRYSTAL_GONIO_VECTORS",
                "CRYSTAL_GONIO_VALUE2":"CRYSTAL_GONIO_VALUES",
                "CRYSTAL_GONIO_NAME3":"CRYSTAL_GONIO_NAMES",
                "CRYSTAL_GONIO_VECTOR3":"CRYSTAL_GONIO_VECTORS",
                "CRYSTAL_GONIO_VALUE3":"CRYSTAL_GONIO_VALUES",
                "DETECTOR_NAMES":"DETECTOR_NAMES",
                "DETECTOR_DIMENSION_X":"%DETECTOR_NAMES%_DETECTOR_DIMENSIONS",
                "DETECTOR_DIMENSION_Y":"%DETECTOR_NAMES%_DETECTOR_DIMENSIONS",
                "DETECTOR_SIZE_X":"%DETECTOR_NAMES%_DETECTOR_SIZE",
                "DETECTOR_VECTOR_X":"%DETECTOR_NAMES%_DETECTOR_VECTORS",
                "DETECTOR_SIZE_Y":"%DETECTOR_NAMES%_DETECTOR_SIZE",
                "DETECTOR_VECTOR_Y":"%DETECTOR_NAMES%_DETECTOR_VECTORS",
                "DARK_PEDESTAL":"DARK_PEDESTAL",
                "SPATIAL_BEAM_POSITION_X":"%DETECTOR_NAMES%_SPATIAL_BEAM_POSITION",
                "SPATIAL_BEAM_POSITION_Y":"%DETECTOR_NAMES%_SPATIAL_BEAM_POSITION",
                "GONIO_NUM_VALUES":"%DETECTOR_NAMES%_GONIO_NUM_VALUES",
                "GONIO_VALUE2":"%DETECTOR_NAMES%_GONIO_VALUES",
                "GONIO_VECTOR2":"%DETECTOR_NAMES%_GONIO_VECTORS",
                "GONIO_VALUE6":"%DETECTOR_NAMES%_GONIO_VALUES",
                "GONIO_VECTOR6":"%DETECTOR_NAMES%_GONIO_VECTORS",
                "X_STAGE_VALUE":"XY_STAGE_VALUES",
                "X_STAGE_VECTOR":"XY_STAGE_VECTORS",
                "Y_STAGE_VALUE":"XY_STAGE_VALUES",
                "Y_STAGE_VECTOR":"XY_STAGE_VECTORS",
                "PIXEL_SIZE_X":"%DETECTOR_NAMES%_DETECTOR_SIZE",
                "PIXEL_SIZE_Y":"%DETECTOR_NAMES%_DETECTOR_SIZE"}
    columns_unique = list(dict.fromkeys(columns))
    unitlist = []
    maxcolumn = 0
    prefix = rawdata.find('meta[@key="DETECTOR_NAMES"]').text
    for k in columns_unique:
        if k in metalist:
            v = metalist[k]
            if re.match(r'%DETECTOR_NAMES%_', v) != None:
                prefix_value = "%DETECTOR_NAMES%_"
                prefix_key = v.replace(prefix_value, prefix)
                v = prefix_key
            tempcolumn = len(rawdata.findall('meta[@key="{value}"]'.format(value=v)))-1
            if maxcolumn < tempcolumn + 1:
                maxcolumn = tempcolumn + 1
            metadata = conv(v, k, rawdata, metadata, len(rawdata.findall('meta[@key="{value}"]'.format(value=v)))-1, unitlist, template)

    subnode = dom.createElement('column_num')
    subnode.appendChild(dom.createTextNode(str(maxcolumn)))
    metadata.appendChild(subnode)
    column_name = template.find('column_name').text
    subnode = dom.createElement('column_name')
    subnode.appendChild(dom.createTextNode(column_name))
    metadata.appendChild(subnode)
    if print_option:
        print(dom.toprettyxml())
    file = codecs.open(outputfile, 'wb', encoding='utf-8')

    dom.writexml(file, '', '\t', '\n', encoding='utf-8')

    file.close()
    dom.unlink()
