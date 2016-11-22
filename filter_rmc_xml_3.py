'''
Created on 16.08.2016

@author: ingr2465
'''

import xml.etree.ElementTree as ET
import sys
import os.path.normpath as normpath


def getcitiesandcityparts(tree):
    '''
    Collects and returns the names of cities and city parts from the passed in XML tree. Returns
    these names as dictionary keyed by city name and carrying for each city name key a value that
    is the set of names of the city parts of the corresponding city.
    '''
    cities = {}
    for country in tree.getroot().findall('COUNTRY'):
        for state in country.findall('STATE'):
            for city in state.findall('CITY'):
                cityparts = set()
                for citypart in city.findall('CITY_PART'):
                    cityparts.add(citypart.get('NAME'))
                cities[city.get('NAME')] = cityparts
    return cities

def removecitiesandcityparts(tree, citiestokeep):
    '''
    Removes from the passed in XML tree those cities and city parts
    that are not listed in the passed in cities to keep dictionary.
    '''
    for country in tree.getroot().findall('COUNTRY'):
        for state in country.findall('STATE'):
            for city in state.findall('CITY'):
                cityname = city.get('NAME')
                if (cityname in citiestokeep):
                    citypartstokeep = citiestokeep[cityname]
                    for citypart in city.findall('CITY_PART'):
                        if (citypart.get('NAME') not in citypartstokeep):
                            city.remove(citypart)
                else:
                    state.remove(city)

def FilterXML(controlFileName, inputFileName, outputFileName):
    '''
    Filters RMC VDE XML input files. That is, creates an XML input file
    by partial copying of contents of an RMC VDE resource generation.
    
    Assumes XML tree structure as encountered in RMC XML input files, i.e., AREACODE nodes within
    CITY or CITY_PART nodes and CITY_PART nodes within CITY nodes within STATE nodes within COUNTRY
    nodes.
    '''
    
    controltree = ET.parse(controlFileName)
    citiestokeep = getcitiesandcityparts(controltree)
    #alternativeadminstokeep = 
    tree = ET.parse(inputFileName)
    removecitiesandcityparts(tree, citiestokeep)#, alternativeadminstokeep)
    tree.write(outputFileName, 'utf-8', True, None, 'xml')


if __name__ == '__main__':
    if len(sys.argv) == 4:
        inputFileName = normpath(sys.argv[1])
        controlFileName = normpath(sys.argv[2])
        outputFileName = normpath(sys.argv[3])
        print  "input file: %s \n" %inputFileName
        print  "control file: %s \n" %controlFileName
        print  "output file: %s \n" %outputFileName

        FilterXML(controlFileName, inputFileName, outputFileName)

    if len(sys.argv) == 3:
        inputFileName = normpath(sys.argv[1])
        outputFileName = normpath(sys.argv[2])
        print  "input file: %s \n" %inputFileName
        print  "output file: %s \n" %outputFileName

        FilterXML(inputFileName, outputFileName)

    else:
        print ("Wrong number of system arguments for running script. This script uses 2 or 3 argumets \n"
               "The first is always the path to the input file \n"
               "The second is either the control file OR the output file \n"
               "The third is the output file\n")

