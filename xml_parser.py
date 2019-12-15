import xml.etree.ElementTree as ET

xml_file = open('C:\TrackApp\input\hlt\LapTimer-All-20191127-140507.xml', 'r')
xmlstr = xml_file.read()
xml_file.close()

root = ET.fromstring(xmlstr)
#root = ET.parse('C:\TrackApp\input\hlt\LapTimer-All-20191127-140507.xml', huge_tree=True)


from lxml.etree import XMLParser, parse
p = XMLParser(huge_tree=True)
tree = parse('C:\TrackApp\input\hlt\LapTimer-All-20191127-140507.xml', parser=p)



from io import BytesIO, StringIO
from lxml.etree import XMLParser, parse
from lxml import etree

some_file_or_file_like_object = StringIO(xmlstr)
tree = etree.parse(some_file_or_file_like_object)

# name
name = tree.getroot().findall('name')[0].text

def get_laps(tree):

    # laps
    laps = tree.getroot().findall('lap')


    lap_db_dict = dict()
    lap_db_ts_dict = dict()
    lap_db_sector = dict()

    # dict of laps
    for lap in laps:
        lap_db_dict[lap.attrib['index']] = dict()
        lap_db_ts_dict[lap.attrib['index']] = dict()


        for item in lap:
            # lap headers
            if item.tag not in {'intermediates', 'recording', 'video'}:
                lap_db_dict[lap.attrib['index']][item.tag] = item.text

            # sectors
            elif item.tag in {'intermediates'}:
                # extract sectors
                #TODO: split string
                #'\n\t\t\t00:35.10,1116.4\n\t\t\t02:23.01,5093.0\n\t\t\t04:26.63,9444.4\n\t\t\t06:58.61,14396.5\n\t\t'
                # print(item.tag)
                df = convert_sector_string(item.text, lap.attrib['index'])
                # print(df)
                lap_db_sector[lap.attrib['index']] = df

            elif item.tag in {'video'}:
                #TODO: video placeholder
                pass

            # lap timeseries data
            else:
                item_ts = item
                i = -1
                for fix in item_ts:
                    i += 1
                    lap_db_ts_dict[lap.attrib['index']][str(i)] = dict()

                    for element in fix:

                        if element.tag != 'acceleration':
                            lap_db_ts_dict[lap.attrib['index']][str(i)][element.tag] = element.text

                        elif element.tag == 'acceleration':
                            for acc_element in element:
                                if acc_element.tag != 'coordinate':
                                    lap_db_ts_dict[lap.attrib['index']][str(i)][acc_element.tag] = acc_element.text



    # lap_db_dict
    df = pd.DataFrame.from_dict(lap_db_dict, orient='index')
    df.index = df.index.astype(int)
    df.sort_index(inplace=True)

    # lap_db_sector
    lap_db_sector[str(25)]


    # lap_db_ts_dict
    # df = pd.DataFrame.from_dict(lap_db_ts_dict['26'], orient='index')
    # '21-JUL-19,16:31:32.83'
    df['date'] = pd.to_datetime(df['date'], format='%d-%b-%y,%H:%M:%S.%f')
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    df[['distance', 'time']] = df["relativeToStart"].str.split(",", n=1, expand=True)
    df[['latitude', 'longitude', 'altitude']] = df["coordinate"].str.split(",", n=2, expand=True)

    df.drop(columns=['coordinate'])

    df['speed'] = df['speed'].astype(float)
    df['lateral'] = df['lateral'].astype(float)
    df['lineal'] = df['lineal'].astype(float)













# vehicles
vehicles = tree.getroot().findall('vehicles')

for item in vehicles[2].find('vehicledef'):
    print(item.tag + " = " + item.text)
