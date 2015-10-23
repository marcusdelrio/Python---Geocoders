import csv
import urllib2
import time

def main():
    start_time = time.clock()
    with open('C:/Users/Marcus/Desktop/Tableau Datasets/NYC TAXI/testdata.csv', 'rb') as inputfile, open ('C:/Users/Marcus/Desktop/outputPy1.csv','wb') as outputfile:
        I=0
        for line in inputfile:
            print line
            number=line[:line.find(" ")]
            street=line[line.find(" ")+1:len(line)-2]
            street=street.replace(" ","%20")
            getInfo(number,street)
            if I==5:
                return

def getInfo(number,street):
    boroughList=["Manhattan","Bronx","Brooklyn","Queens","Staten%20Island"]
    for borough in boroughList:
        url="https://api.cityofnewyork.us/geoclient/v1/address.json?houseNumber="+number+"&street="+street+"&borough="+borough+"&app_id=a2ed8746&app_key=d305a33ba1ada6a3929d1cf543b55d5d"
        response = urllib2.urlopen(url)
        html = response.read()
        hood=html[html.find("ntaName")+10:html.find(",",html.find("ntaName"))-1]
        print hood
