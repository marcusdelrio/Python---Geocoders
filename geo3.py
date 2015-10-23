import csv
import urllib2
import time

def main():
    start_time = time.clock()
    with open('C:/Users/Marcus/Desktop/Tableau Datasets/NYC TAXI/All xmas taxi trips.csv', 'rb') as inputfile, open ('C:/Users/Marcus/Desktop/outputPy.csv','wb') as outputfile:
        I=0
        for line in inputfile:
           
           lastCommaPos=line.rfind(',')
           lat=line[lastCommaPos+1:line.find(" ",lastCommaPos+1)]# make uniform to cut \n new line
           lon=line[line.rfind(',',0,lastCommaPos-1)+1:lastCommaPos]
           lat=lat.strip()
           info=getInfo1(lat,lon)
           line=line[:line.find("\n")-1]+","+str(info)+"\n"
           if "2013-12-25" in line:
               outputfile.write(line)
    
               

def getInfo1(lat,lon):#using geonames
    url="http://api.geonames.org/neighbourhood?&lat="+lat+"&lng="+lon+"+"+"&username=coos678"
    response = urllib2.urlopen(url)
    html = response.read()
    print html
    start=html.find("<name>")
    end=html.find("</name>")
    hood=html[start+6:end]#hood captures
    if len(hood)<30:
        return hood
    else:
        return "not found"
        
    

