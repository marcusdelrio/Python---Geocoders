import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim()

import time
import csv
def main():
    start_time = time.time()
    with open('C:/Users/Marcus/Desktop/Tableau Datasets/NYC TAXI/All xmas taxi trips.csv', 'rb') as inputfile, open ('C:/Users/Marcus/Desktop/outputPy.csv','wb') as outputfile:
        I=0
        for line in inputfile:  
            I=I+1
           
            lastCommaPos=line.rfind(',')
            lat=line[lastCommaPos+1:line.find(" ",lastCommaPos+1)]# make uniform to cut \n new line
            lon=line[line.rfind(',',0,lastCommaPos-1)+1:lastCommaPos]
            lat=lat.strip()
            hood=geocoder(lat,lon)
            line=line[:line.find("\n")-1]+","+str(hood)+"\n"
            outputfile.write(line)
            if (I==1000):
               print("--- %s seconds ---" % (time.time() - start_time))
               break

def geocoder(lat,lon):
    latlon=lat+","+lon
    try:
        location=geolocator.reverse(latlon,timeout=5)
        neighbourhood=location.raw["address"]["neighbourhood"]
        return neighbourhood
    except (TypeError,KeyError,geopy.exc.GeocoderTimedOut) as e:
        return "No data"
