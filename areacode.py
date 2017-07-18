class Areacode:

    xmlcitydata = None
    xmlregiondata = None
    args = ''
    areacode = ''
    cityresult = ''
    regionresult = ''
    result = ''

    def __init__(self,areacode):
        parser = argparse.ArgumentParser(description='Area code lookup tool.')
        parser.add_argument('acode')
        self.args = parser.parse_args()
        self.areacode = self.args.acode
        self.fetchXML()
        self.parseXML()

    def fetchXML(self):
        citybuffer = StringIO()
        regionbuffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://www.localcallingguide.com/xmlrc.php?npa='+self.areacode)
        c.setopt(c.WRITEDATA,citybuffer)
        c.perform()
        c.close()
        self.xmlcitydata = citybuffer.getvalue()
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://www.localcallingguide.com/xmllistnpa.php?npa='+self.areacode)
        c.setopt(c.WRITEDATA,regionbuffer)
        c.perform()
        c.close()
        self.xmlregiondata = regionbuffer.getvalue()

    def parseXML(self):
        city_result_list = []
        region_result_list = 'Area Code '+self.areacode+': '
        if self.xmlcitydata is None:
            self.fetchXML()
        for i in ET.fromstring(self.xmlcitydata).findall('.//rc'):   
            city_result_list.append(i.text)
        for j in ET.fromstring(self.xmlregiondata).findall('.//rname'):   
           region_result_list += j.text
        self.cityresult = ', '.join(str(item) for item in city_result_list)
        self.regionresult = region_result_list

    def outputResults(self):
        self.result = self.regionresult+'\n\n'
        self.result += self.cityresult