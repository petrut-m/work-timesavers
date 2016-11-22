import xml.etree.ElementTree as ET
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import csv
import subprocess
import codecs
old_XML_folder_path = ""
new_XML_folder_path = ""
scripts_path = ""
xml_list_for_first_argument = []
xml_list_for_second_argument = []
scripts = []
arguments = []
full_path_1 = ""
full_path_2 = ""



def pathman(path):  # path manipulations, clean-up, xml search, country list creation
    # os.listdir on input folder, gets us to the folders with the .xml
    xml_list = []
    os.path.normpath(path)
    if os.path.exists(path):
        valid_path = path
        print("Path: %s") % valid_path
    else:
        print("Path %s does not exist!") % path
        exit()

#    os.listdir(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xml"):
                xml_list.append(os.path.join(root, file))
            if file.endswith(".py"):
                scripts.append(file)

    return valid_path, xml_list


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


def statistics(target_xml):
    country_name = ""
    altadmin_nr = 0
    states_nr = 0
    city_nr = 0
    citypart_nr = 0
    areacode_nr = 0
    street_nr = 0
    empty_citypart_nr = 0
    empty_city_nr = 0
    empty_areacode_nr = 0
    empty_altadmin_nr = 0

    #    count city, city_part, area code, street, empty city_part, empty areacode
    tree = ET.parse(target_xml)
    for count in tree.getroot().findall('COUNTRY'):
        country_name = count.get('NAME')
        states_nr += len(count.findall('STATE'))
        for state in count.findall('STATE'):
            city_nr += len(state.findall('CITY'))
            altadmin_nr += len(state.findall('ALTERNATIVE_ADMIN'))

            for altadmin in state.findall('ALTERNATIVE_ADMIN'):
                if 0 == len(list(altadmin.findall('AREACODE'))):
                    empty_altadmin_nr += 1
                areacode_nr += len(altadmin.findall('AREACODE'))
                street_nr += len(altadmin.findall('STREET'))

            for city in state.findall('CITY'):
                street_nr += len(list(city.findall('STREET')))
                areacode_nr += len(city.findall('AREACODE'))
                citypart_nr += len(city.findall('CITY_PART'))
                if 0 == len(city.findall('CITY_PART')) and 0 == len(city.findall('AREACODE')):
                    empty_city_nr += 1

                for areacode in city.findall('AREACODE'):
                    street_nr += len(list(areacode.findall('STREET')))
                    if 0 == len(areacode.findall('STREET')):
                        empty_areacode_nr += 1

                for citypart in city.findall('CITY_PART'):
                    street_nr += len(list(citypart.findall('STREET')))
                    areacode_nr += len(citypart.findall('AREACODE'))
                    if 0 == len(citypart.findall('AREACODE')) and 0 == len(citypart.findall('STREET')):
                        empty_citypart_nr += 1

                    for areacode in citypart.findall('AREACODE'):
                        street_nr += len(list(areacode.findall('STREET')))
                        if 0 == len(areacode.findall('STREET')):
                            empty_areacode_nr  += 1

            for areacode in state.findall('AREACODE'):
                for street in areacode.findall('STREET'):
                    if 0 == len(list(street)):
                        empty_areacode_nr += 1
    print "\nFor %s found:" % target_xml
    print "states_nr %s, altadmin_nr %s, city_nr %s, citypart_nr %s, areacode_nr %s, street_nr %s " % (
    states_nr, altadmin_nr, city_nr, citypart_nr, areacode_nr, street_nr,)
    print "empty_citypart_nr %s, empty_city_nr %s, empty_areacode_nr %s, empty_altadmin_nr %s \n" % (
    empty_citypart_nr, empty_city_nr, empty_areacode_nr, empty_altadmin_nr)
    if os.path.isfile(target_xml):
        byte_size = file_size(target_xml)
    #write output to CSV file

    writer.writerow((country_name, states_nr, altadmin_nr, city_nr, citypart_nr, areacode_nr, street_nr, empty_citypart_nr,
                    empty_city_nr, empty_areacode_nr, empty_altadmin_nr, byte_size))

    return (altadmin_nr, states_nr, city_nr, citypart_nr, areacode_nr, street_nr, empty_citypart_nr, empty_city_nr,
            empty_areacode_nr, empty_altadmin_nr, byte_size)

def user_interface():
    print ("Welcome to xml filtering script \n You have triggered this script without any input arguments\n you can choose the available options: ")
    print ("Please enter the number corresponding to your desired option\n "
           "[1]Create statistics for a single set of XMl's \n [2]")

def triggerfilterscript(path, arguments):

    subprocess.call("test1.py", shell=True)
    pass

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        sanitised_paths = pathman(sys.argv[1])
        full_path_1 = sanitised_paths[0]
        xml_list_for_first_argument = sanitised_paths[1]
        print ("\n Path where .xml's found:")
        print full_path_1

    if len(sys.argv) >= 3:
        sanitised_paths = pathman(sys.argv[2])
        full_path_2 = sanitised_paths[0]
        xml_list_for_second_argument = sanitised_paths[1]
        print ("\n Path where .xml's found:")
        print full_path_2
        if xml_list_for_first_argument != xml_list_for_second_argument and len(sys.argv) == 3 :
            print ("Countries in first set are not the same as the countries in the second set!!")

    if len(sys.argv) == 4:
        scripts_path = pathman(sys.argv[3])


    # generate statistics for original XML's

    if len(sys.argv) >= 2:
        ofile = open(os.path.join(full_path_1,'test.csv'), "wb")
        writer = csv.writer(ofile, dialect='excel-tab', delimiter = '\t')
        writer.writerow(('country', 'states_nr', 'altadmin_nr', 'city_nr', 'citypart_nr', 'areacode_nr', 'street_nr',
                      'empty_citypart_nr', 'empty_city_nr', 'empty_areacode_nr', 'empty_altadmin_nr', 'size'))

        for xml in xml_list_for_first_argument:
            print("Generating statistics for %s in %s") % (xml.rsplit(os.sep)[len(xml.rsplit(os.sep))-1], full_path_1)
            xml_path = xml
            statistics(xml_path)
        ofile.close()



    if len(sys.argv) >= 3:
        ofile = open(os.path.join(full_path_2,'test.csv'), "wb")
        writer = csv.writer(ofile, dialect='excel-tab', delimiter = '\t')
        writer.writerow(('country', 'states_nr', 'altadmin_nr', 'city_nr', 'citypart_nr', 'areacode_nr', 'street_nr',
                          'empty_citypart_nr', 'empty_city_nr', 'empty_areacode_nr', 'empty_altadmin_nr'))

        for xml in xml_list_for_second_argument:
            print("Generating statistics for %s country in %s") % (xml, full_path_2)
            xml_path =  xml
            statistics(xml_path)
        ofile.close()

        #let the scripts process the second set of data.

    if len(sys.argv) == 4:
        for script in scripts:
            script_path = os.path.join(scripts_path, script)
            triggerfilterscript(script_path, arguments)



    print ("################### DONE #########################")
    exit()
    # TO DO :
    # find available filters and grup in 2 args and 3 args
    # apply filters for each country in second group, place results in
    # for XML's in path
    # statistics of XML in path !!!!
    # aplly filters in
