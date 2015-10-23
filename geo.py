import csv
import urllib2
import time

KEY='AIzaSyCKv6YbxwuC8L9DCHhNAeytlJxZRXPEWto'
def main():
    with open('C:/Users/Marcus/Desktop/Tableau Datasets/NYC TAXI/All xmas taxi trips.csv', 'rb') as inputfile, open ('C:/Users/Marcus/Desktop/outputPy.csv','wb') as outputfile:
        I=0
        for line in inputfile:
           lastCommaPos=line.rfind(',')
           lat=line[lastCommaPos+1:line.find(" ",lastCommaPos+1)]# make uniform to cut \n new line
           lon=line[line.rfind(',',0,lastCommaPos-1)+1:lastCommaPos]
           lat=lat.strip()
           
           info=getInfo(lat,lon)
           
           line=line[:line.find("\n")-1]+","+str(info)+"\n"
           outputfile.write(line)
           I=I+1
           if (I==2500):
               break

def getHtml(lat,lon):

    url='https://maps.googleapis.com/maps/api/geocode/json?latlng='+lat+','+lon+'&key='+KEY
    try:#possibly unnecessary
        response = urllib2.urlopen(url)
        html = response.read()
        #print "getHtml worked"
        return html
    except urllib2.HTTPError as e:
        print "error in getHtml"
        
    


def getInfo(lat,lon):
    rawHtml=getHtml(lat,lon)#calls google API function getHtml
    try:
        hoodPos=rawHtml.find('"types" : [ "neighborhood", "political" ]')
        startPrint=rawHtml.rfind(":",0,hoodPos)+3
        neighborhood=rawHtml[startPrint:rawHtml.find('"',startPrint+1)]
        
        
        postalcodePos=rawHtml.find('"types" : [ "postal_code" ]')
        zipcode=rawHtml[postalcodePos-23:postalcodePos-18]

        return neighborhood+", "+zipcode
        
        
    except AttributeError as e:
        print "NULL"

    
    
    
