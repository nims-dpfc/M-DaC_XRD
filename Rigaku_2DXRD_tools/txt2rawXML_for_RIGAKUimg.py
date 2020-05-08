# -------------------------------------------------
# txt2rawXML_for_RIGAKUimg.py
#
# Copyright (c) 2019, Data PlatForm Center, NIMS
#
# This software is released under the MIT License.
# -------------------------------------------------
# coding: utf-8

"""txt2rawXML_for_RIGAKUimg.py

This module extracts raw parameter from
RIGAKU img text file.

Copyright (c) 2019, Data PlatForm Center, NIMS
This software is released under the MIT License.

Example
-------

    Parameters
    ----------
    inputfile : RIGAKU img text file
    templatefile : template file for RIGAKU img raw Data
    outputfile : output file

    $ python txt2rawXML_for_RIGAKUimg.py [inputfile] [templatefile] [outputfile]

"""
__package__ = "M-DaC_XRD/Rigaku_2DXRD_tools"
__version__ = "1.0.0"

import argparse
import xml.dom.minidom
import re
import xml.etree.ElementTree as ET
import codecs


def make_xml(key, value, channel, prefix):
    """This function appends XML node

    Parameters
    ----------
    key: meta key
    value: meta value
    channel: HEADER INFORMATION = 0
             Numeric Data Info > 0
    prefix: meta[@key="DETECTOR_NAMES"].text

    """
    subnode = dom.createElement('meta')
    subnode.appendChild(dom.createTextNode(value))
    subnode_attr = dom.createAttribute('key')
    if re.match(r'%DETECTOR_NAMES%_', key) != None:
        prefix_value = "%DETECTOR_NAMES%_"
        prefix_key = key.replace(prefix_value, prefix)
    else:
        prefix_key = key
    subnode_attr.value = prefix_key
    subnode.setAttributeNode(subnode_attr)
    subnode_attr = dom.createAttribute('type')
    typename = template.find('meta[@key="{value}"]'.format(value=key))
    if typename is not None:
        if typename.get("type") is not None:
            subnode_attr.value = typename.get("type")
        else:
            subnode_attr.value = "String"
        subnode.setAttributeNode(subnode_attr)
        metadata.appendChild(subnode)

    if channel != 0:
        subnode_attr = dom.createAttribute('column')
        subnode_attr.value = str(channel)
        subnode.setAttributeNode(subnode_attr)
        metadata.appendChild(subnode)


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

    template = ET.parse(templatefile)
    columns = []
    metas = template.findall('meta')
    for meta in metas:
       columns.append(meta.attrib["key"])
    dom = xml.dom.minidom.Document()
    metadata = dom.createElement('metadata')
    dom.appendChild(metadata)
    channel = 0
    wide = 1
    maxcolumn = 1
    metapart = "header"
    infopart = 0
    prefix = ""
    with codecs.open(readfile, 'r', 'utf-8', 'ignore') as f:
        for line in f:
            line = line.strip()
            comment = line[0:2]
            if line == '':
                if metapart == "header":
                    metapart = "numericData"
                    infopart = 1
            elif metapart == "header" and comment.find("//") != 0:
                lines = line.split(":")
                lines = [item.strip() for item in lines]
                key = lines[0]
                value = lines[1]
                if key == "DETECTOR_NAMES":
                    prefix = value
                if len(prefix) > 0:
                    prefix_value = "%DETECTOR_NAMES%_"
                    key = key.replace(prefix, prefix_value)
                if 2 < len(lines):
                    for index, item in enumerate(lines):
                        if 1 < index:
                            value = value + ':' + item
                make_xml(key, value, channel, prefix)

            elif metapart == "numericData":
                if line == "//Numeric Data":
                    infopart = 0

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
