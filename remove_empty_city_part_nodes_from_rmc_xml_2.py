'''
Created on 16.08.2016

@author: ingr2465
'''

import xml.etree.ElementTree as ET
import sys
import os.path.normpath as normpath

def removecitypartsifempty(tree):
    '''
    Removes city part nodes that are effectively empty. That is, removes city part nodes that either
    do not have any child elements or have only areacode nodes as child elements that have
    themselves no child elements
    
    Assumes XML tree structure as encountered in RMC XML input files, i.e., AREACODE nodes within
    CITY or CITY_PART nodes and CITY_PART nodes within CITY nodes within STATE nodes within COUNTRY
    nodes.
    '''
    stillavailableareacodes = set()
    for country in tree.getroot().findall('COUNTRY'):
        for state in country.findall('STATE'):
            for city in state.findall('CITY'):
                for areacode in city.findall('AREACODE'):
                    stillavailableareacodes.add(areacode.get('UID'))
                for citypart in city.findall('CITY_PART'):
                    for areacode in citypart.findall('AREACODE'):
                        if (0 == len(list(areacode))):
                            citypart.remove(areacode)
                        else:
                            stillavailableareacodes.add(areacode.get('UID'))
                    if (0 == len(list(citypart))):
                        city.remove(citypart)
    return stillavailableareacodes


def reworkorremovealternativeadmins(element, stillavailableareacodes):
    '''
    Iterates over the immediate alternative admin child elements of the passed in element. Removes
    areacode references from alternative admin nodes if the referenced areacode UIDs are not
    included in the passed in set of still available areacode UIDs. Removes alternative admin nodes
    that carry no child elements or that carried only areacode references that are no longer valid.
    '''
    for alternativeadmin in element.findall('ALTERNATIVE_ADMIN'):
        for areacode in alternativeadmin.findall('AREACODE'):
            if (areacode.get('REF') not in stillavailableareacodes):
                alternativeadmin.remove(areacode)
        if (0 == len(list(alternativeadmin))):
            element.remove(alternativeadmin)


def removealternativeadminsifempty(tree, stillavailableareacodes):
    '''
    Removes areacode references from alternative admin nodes if the referenced areacode UIDs are not
    included in the passed in set of still available areacode UIDs. Removes alternative admin nodes
    that carry no child elements or that carried only areacode references that are no longer valid.
    '''
    for country in tree.getroot().findall('COUNTRY'):
        reworkorremovealternativeadmins(country, stillavailableareacodes)
        for state in country.findall('STATE'):
            reworkorremovealternativeadmins(state, stillavailableareacodes)


def filterxml(inputFileName, outputFileName):
    '''
    Filters RMC VDE XML input files. That is, creates an XML input file
    by partial copying of contents of an RMC VDE resource generation.
    '''
    tree = ET.parse(inputFileName)
    stillavailableareacodes = removecitypartsifempty(tree)
    removealternativeadminsifempty(tree, stillavailableareacodes)
    tree.write(outputFileName, 'utf-8', True, None, 'xml')


if __name__ == '__main__':
    if len(sys.argv) == 4:
        inputFileName = normpath(sys.argv[1])
        controlFileName = normpath(sys.argv[2])
        outputFileName = normpath(sys.argv[3])
        print  "input file: %s \n" %inputFileName
        print  "control file: %s \n" %controlFileName
        print  "output file: %s \n" %outputFileName

        filterxml(controlFileName, inputFileName, outputFileName)

    if len(sys.argv) == 3:
        inputFileName = normpath(sys.argv[1])
        outputFileName = normpath(sys.argv[2])
        print  "input file: %s \n" %inputFileName
        print  "output file: %s \n" %outputFileName

        filterxml(inputFileName, outputFileName)

    else:
        print ("Wrong number of system arguments for running script. This script uses 2 or 3 argumets \n"
               "The first is always the path to the input file \n"
               "The second is either the control file OR the output file \n"
               "The third is the output file\n")