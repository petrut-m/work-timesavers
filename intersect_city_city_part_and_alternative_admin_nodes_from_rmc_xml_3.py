'''
Created on 16.08.2016

@author: ingr2465
'''

import xml.etree.ElementTree as ET
import sys
import os.path.normpath as normpath

def getnamesofcitiescitypartsandalternativeadmins(tree):
    '''
    Collects and returns from the passed in XML tree the names of cities, city parts and alternative
    admins. Returns these names as a tuple of one dictionary (keyed by city name and carrying for
    each city name key a value that is the set of names of the city parts of the corresponding city)
    and one set (carrying the names of alternative admins).
    '''
    cities = {}
    cityparts = set()
    numberofcitieswithduplicatename = 0
    alternativeadmins = set()
    for country in tree.getroot().findall('COUNTRY'):
        for alternativeadmin in country.findall('ALTERNATIVE_ADMIN'):
            alternativeadmins.add(alternativeadmin.get('NAME'))
        for state in country.findall('STATE'):
            for alternativeadmin in state.findall('ALTERNATIVE_ADMIN'):
                alternativeadmins.add(alternativeadmin.get('NAME'))
            for city in state.findall('CITY'):
                cityname = city.get('NAME')
                if (cityname in cities):
                    cityparts = cities[cityname]
                    numberofcitieswithduplicatename = numberofcitieswithduplicatename + 1
                else:
                    cityparts = set()
                    cities[cityname] = cityparts
                for citypart in city.findall('CITY_PART'):
                    cityparts.add(citypart.get('NAME'))
        if (numberofcitieswithduplicatename > 0):
            print('Found ' + str(numberofcitieswithduplicatename) + ' cities with duplicate ' +
                  'names => created combined set of city part names for each duplicate city name.')
    return (cities, alternativeadmins)


def removecitiesandcityparts(tree, citiestokeep):
    '''
    Removes from the passed in XML tree those cities and city parts that are not listed in the
    passed in cities to keep dictionary. Collects and returns the UIDs of those areacode nodes
    that are still available after pruning cities and city parts.
    '''
    stillavailableareacodes = set()
    for country in tree.getroot().findall('COUNTRY'):
        for state in country.findall('STATE'):
            for city in state.findall('CITY'):
                cityname = city.get('NAME')
                if (cityname in citiestokeep):
                    for areacode in city.findall('AREACODE'):
                        stillavailableareacodes.add(areacode.get('UID'))
                    citypartstokeep = citiestokeep[cityname]
                    for citypart in city.findall('CITY_PART'):
                        if (citypart.get('NAME') in citypartstokeep):
                            for areacode in citypart.findall('AREACODE'):
                                stillavailableareacodes.add(areacode.get('UID'))
                        else:
                            city.remove(citypart)
                else:
                    state.remove(city)
    return stillavailableareacodes


def reworkorremovealternativeadmins(element, alternativeadminstokeep, stillavailableareacodes):
    '''
    Iterates over the immediate alternative admin child elements of the passed in element. Removes
    alternative admin nodes if their names are not included in the passed in set of names of
    alternative admins to keep. Also removes areacode references from alternative admin nodes if the
    referenced areacode UIDs are not included in the passed in set of still available areacode UIDs.
    Also removes alternative admin nodes that carry no child elements or that carried only areacode
    references that are no longer valid.
    '''
    for alternativeadmin in element.findall('ALTERNATIVE_ADMIN'):
        if (alternativeadmin.get('NAME') in alternativeadminstokeep):
            for areacode in alternativeadmin.findall('AREACODE'):
                if (areacode.get('REF') not in stillavailableareacodes):
                    alternativeadmin.remove(areacode)
            if (0 == len(list(alternativeadmin))):
                element.remove(alternativeadmin)
        else:
            element.remove(alternativeadmin)


def removealternativeadmins(tree, alternativeadminstokeep, stillavailableareacodes):
    '''
    Removes alternative admin nodes if their names are not included in the passed in set of names of
    alternative admins to keep. Also removes areacode references from alternative admin nodes if the
    referenced areacode UIDs are not included in the passed in set of still available areacode UIDs.
    Also removes alternative admin nodes that carry no child elements or that carried only areacode
    references that are no longer valid.
    '''
    for country in tree.getroot().findall('COUNTRY'):
        reworkorremovealternativeadmins(country, alternativeadminstokeep, stillavailableareacodes)
        for state in country.findall('STATE'):
            reworkorremovealternativeadmins(state, alternativeadminstokeep, stillavailableareacodes)


def FilterXML(controlFileName, inputFileName, outputFileName):
    '''
    Filters RMC VDE XML input files. That is, creates an XML input file for RMC VDE resource
    generation by copying the contents from one such file and using a second such file to decide
    whether cities, city parts and alternative admins shall be copied or filtered out (=> use case
    is to keep them only if they were included in XML input data of a prior production, say, to keep
    only cities, city parts and alternative admins from 2016_03 input data if cities, city parts and
    alternative admins of the same name were part of the 2015_03 input data).
    
    Assumes XML tree structure as encountered in RMC XML input files, i.e.:
     * AREACODE nodes within CITY or CITY_PART nodes or - as reference nodes within
       ALTERNATIVE_ADMIN nodes
     * CITY_PART nodes within CITY nodes within STATE nodes within COUNTRY nodes.
     * ALTERNATIVE_ADMIN nodes within COUNTRY or STATE nodes
    '''
    
    controltree = ET.parse(controlFileName)
    (citiestokeep, alternativeadminstokeep) = getnamesofcitiescitypartsandalternativeadmins(controltree)
    tree = ET.parse(inputFileName)
    stillavailableareacodes = removecitiesandcityparts(tree, citiestokeep)
    removealternativeadmins(tree, alternativeadminstokeep, stillavailableareacodes)
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