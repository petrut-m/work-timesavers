# create a dictionary from admin xml file for a specific file
def create_dict_from_xml(inputFilePath):
    streetNr = 0
    state = ""
    city = ""
    dataDictionary = Vividict()
    stateNr = 0
    cityNr = 0
    totalStreetNr = 0
    cityPartNr = 0
    unique_streets_names = Vividict()

    parser = ET.iterparse(inputFilePath, events=['start', 'end'])

    for event, elem in parser:
        if event == "start" and elem.tag == "CITY":
            city = elem.attrib['NAME']
            streetNr = 0
            cityNr+=1

        if event == "start" and elem.tag == "STATE":
            state = elem.attrib['NAME']


        if event == "end" and elem.tag == "STATE":
            elem.clear()
            stateNr+=1

        if event == "start" and elem.tag == "CITY_PART":
            cityPartNr+=1

        if event == "start" and elem.tag == "AREACODE":
            cityPartNr+=1

        if event == "end" and elem.tag == "CITY" and streetNr > 0:
            dataDictionary[state][city] = streetNr
            elem.clear()

        if event == "end" and elem.tag == "STREET":
            unique_streets_names[elem.attrib['NAME']]=1
            streetNr += 1
            totalStreetNr+=1
            elem.clear()

    print "total Number of streets %s" %totalStreetNr
    total = totalStreetNr+stateNr+cityPartNr+cityNr

    print "At the end, the statistics:"
    print "Number of states = %s" %stateNr
    print "Number of cities = %s" %cityNr
    print "Number of city parts = %s" %cityPartNr
    print "Number of street names(unique) = %s" %len(unique_streets_names)
    print "Number of addresss entries = %s " %total

    return dataDictionary
