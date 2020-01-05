from bottle import route, run, template, get, post, request, static_file, response
from xml.dom import minidom
import xml.etree.ElementTree as ET
import random
import json
import re
import os.path
from os import path

@route('/')
def index():
    return template('index.html')


@route('/<path>')
def js(path):
    return static_file(path, root='../')


@post('/saveJourney')
def saveJourney():
    dic=list(request.forms.dict.keys())[0]
    journeyData=json.loads(dic)

    #journeyName,poscount,posarray
    journeyName=journeyData['journeyName']
    posarray = journeyData['posarray']
    posleng=len(posarray)


    #create xmlDom,journeys,journey,
    root = minidom.Document()
    xml = root.createElement('journeys')
    root.appendChild(xml)

    journey = root.createElement('journey')
    journey.setAttribute('name', journeyName)
    xml.appendChild(journey)



    for pos_num in range(0, posleng):
        journeyleg = root.createElement('journeyleg')
        journey.appendChild(journeyleg)

        pos = root.createElement('pos')
        pos.appendChild(root.createTextNode(str(pos_num)))
        journeyleg.appendChild(pos)

        latlng = root.createElement('latlng')
        latlng.appendChild( root.createTextNode('(' + str(posarray[pos_num]['lat']) + ', ' + str(posarray[pos_num]['lng']) + ')'))
        journeyleg.appendChild(latlng)

    xml_str = root.toprettyxml(indent="\t")
    save_path_file = journeyName+".xml"
    with open(save_path_file, "w") as f:
        f.write(xml_str)
    return template("index.html")


@get('/getJourney')
def getJourney():
    journeyName=request.query.journey
    posarray = []
    posleng = 0
    returnjson = {"journeyName": "", "posarray": posarray}


    #if not exists
    if(path.exists(journeyName+".xml")==False):
        return json.dumps(returnjson)
    tree = ET.parse(journeyName+".xml")
    root = tree.getroot()
    #root = minidom.parse()





    for journey in root:
        returnjson['journeyName']=journey.attrib['name']
        for journeyLeg in journey:
            postext=journeyLeg[1].text
            numbers=re.findall(r"[-+]?\d*\.\d+|\d+", postext)
            posarray.append({"lat":str(numbers[0]),"lng":str(numbers[1])})


    rv = [{"id": " ", "name": "Test Item 1"}, {"id": 2, "name": "Test Item 2"}]
    response.content_type = 'application/json'
    #from xml.dom import minidom
    #mytree = minidom.parse('sample.xml')
    # data = open('sample.xml')
    # a = minidom.parse(data)
    # data = minidom.parseString('<myxml>Using<empty/>parseString</myxml>')

    #tagname = mytree.getElementsByTagName('journeyleg')
    # print(tagname)
    # print(tagname[0].attributes['name'].value)
    #print(tagname[0].firstChild.data)

    return json.dumps(returnjson)


# @post('/saveJourney') # or @route('/login' method='POST')
# def save_journey():
#     journeyName = request.forms.get('journeyName')
#     if check_login(username, password):
#         return "<p>Your login information was correct.</p>"
#     else:
#         return "<p>Login failed.</p>"

# def check_login(username, password):
#     usern = 'admin'
#     passw = 'admin'
#
#     if username == usern and password == passw:
#         return True
#     else:
#         return False


run(host='localhost', port=8080)