from flask import render_template,json,request
import pycurl,xml.etree.ElementTree as ET
from StringIO import StringIO
from app import app
from werkzeug.contrib.fixers import ProxyFix

class Areacode:
    xmlcitydata = None
    xmlregiondata = None
    args = ''
    areacode = ''
    cityresult = ''
    regionresult = ''
    region_shortcode = ''
    result = ''

    def __init__(self,areacode):
        self.areacode = areacode
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
        region_result_list = ''        
        if self.xmlcitydata is None:
            self.fetchXML()
        for i in ET.fromstring(self.xmlcitydata).findall('.//rc'):   
            city_result_list.append(i.text)
        for j in ET.fromstring(self.xmlregiondata).findall('.//rname'):   
           region_result_list += j.text
        for k in ET.fromstring(self.xmlregiondata).findall('.//region'):
            self.region_shortcode = k.text
        self.cityresult = ', '.join(str(item) for item in city_result_list)
        self.regionresult = region_result_list

    def outputResults(self):
        self.result = self.regionresult+'\n\n'
        self.result += self.cityresult
 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['POST','GET'])
def search():
    try:
        _inputAreaCode = request.form['inputAreaCode']

        if _inputAreaCode:
            acode = Areacode(_inputAreaCode)
            acode.outputResults()
            if acode.regionresult != '' and acode.cityresult != '':
                return json.dumps({
                    'areacode': acode.areacode,
                    'region': acode.regionresult,
                    'cities': acode.cityresult,
                    'shortcode': acode.region_shortcode
                    })
            else:
                return json.dumps({
                    'error': 'Area code not found or invalid.'
                    })

        else:
            return json.dumps({'error': 'Please enter a valid area code.'})

    except Exception as e:
        return json.dumps({'error': str(e)})

app.wsgi_app = ProxyFix(app.wsgi_app)