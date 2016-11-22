'''
Created on 16.08.2016

@author: ingr2465
'''
import sys
import os.path.normpath as normpath
import xml.etree.ElementTree as ET

# AdminXML1_Location = os.normapath.sys.argv[1] #Location of base XML
# AdminXML2_Location = os.normapath.sys.argv[2] #location of to be adapted XML
tripleTupleHolder = []
quadrupleTupleHolder = []
tupleList = []


def RemoveCitiesAndCity_partsIfEmpty(tree):
    ''''
    Removes city and city part nodes that are effectively empty. That is, removes:
     * city part nodes that either do not have any child elements or have only areacode nodes as
       child elements that have themselves no child elements
     * city nodes that either do not have any child elements or have as child elements only
       effectively empty city part nodes and/or areacode nodes that have no child elements
    
    Assumes XML tree structure as encountered in RMC XML input files, i.e., AREACODE nodes within
    CITY or CITY_PART nodes and CITY_PART nodes within CITY nodes within STATE nodes within COUNTRY
    nodes.
    '''
    for country in tree.getroot().findall('COUNTRY'):
        for state in country.findall('STATE'):
            for city in state.findall('CITY'):
                for areacode in city.findall('AREACODE'):
                    if (0 == len(list(areacode))):
                        city.remove(areacode)
                for city_part in city.findall('CITY_PART'):
                    for areacode in city_part.findall('AREACODE'):
                        if (0 == len(list(areacode))):
                            city_part.remove(areacode)
                    if (0 == len(list(city_part))):
                        city.remove(city_part)
                if (0 == len(list(city))):
                    state.remove(city)


def GetCityAndCity_partFromFirst(tree):
    for country in tree.getroot().findall('COUNTRY'):
        for state in country.findall('STATE'):
            for city in state.findall('CITY'):
                # if (0 != len(list(areacode))):
                holder = (state.get('NAME'), city.get('NAME'))
                tripleTupleHolder.append(holder)

                for city_part in city.findall('CITY_PART'):
                    #for areacode in city_part.findall('AREACODE'):
                    #    if (0 != len(list(areacode))):
                    holder = (state.get('NAME'), city.get('NAME'), city_part.get('NAME'))
                    quadrupleTupleHolder.append(holder)

    print "Got City and city part from first file"
    print "***** tripleTupleHolder : **************"
    foo = open("D:\\Work\\STF_Testing\\NDB-15547\\adminXML\\RussiaNew\\Russia.tripple","a")

    foo.write(unicode(tripleTupleHolder).encode('utf8'))
    foo.write(unicode(quadrupleTupleHolder).encode('utf8'))


def RemoveUnmatchingCityAndCity_part(tree):
    for country in tree.getroot().findall('COUNTRY'):
        for state in country.findall('STATE'):
            for city in state.findall('CITY'):
                holder = ()
                holder = (state.get('NAME'), city.get('NAME'))

                if holder not in tripleTupleHolder:
                    state.remove(city)
                    print ("Warning: removed city: ", city.get('NAME'))
                for city_part in city.findall('CITY_PART'):
                    holder = ()
                    holder = (state.get('NAME'), city.get('NAME'), city_part.get('NAME'))
                    if holder not in quadrupleTupleHolder:
                        city.remove(city_part)
                        print ("Warning: removed city_part ", city_part.get('NAME'))

    print ("Removed unmatching")


def FilterXML(inputFileName1, inputFileName2, outputFileName):
    '''
    Filters RMC VDE XML input files. That is, creates an XML input file
    by partial copying of contents of an RMC VDE resource generation.
    '''
    tree1 = ET.parse(inputFileName1);
    print "parsing first XML"
    tree2 = ET.parse(inputFileName2);
    print "parsing second XML"
    # RemoveCitiesAndCity_partsIfEmpty(tree)
    GetCityAndCity_partFromFirst(tree1)
    RemoveUnmatchingCityAndCity_part(tree2)
    tree2.write(outputFileName, 'utf-8', True, None, 'xml')
    print "writing output file"


def intersectXML(inputFileName1, inputFileName2, outputFileName):
    tree = ET.parse(inputFileName1);


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
        print  "output file: %s \n" %outputFileName;
        FilterXML(inputFileName, outputFileName)

    else:
        print ("Wrong number of system arguments for running script. This script uses 2 or 3 argumets \n"
               "The first is always the path to the input file \n"
               "The second is either the control file OR the output file \n"
               "The third is the output file\n")
