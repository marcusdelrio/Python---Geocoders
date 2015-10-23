import csv
import urllib2
import time
boroughList=["Manhattan","Bronx","Brooklyn","Queens","Staten%20Island"]



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
            toWrite=line[:line.find("\n")-1]+","+str(info)+"\n"
            outputfile.write(toWrite)
            I=I+1
            if (I%500==0):
                print I
                print time.clock() - start_time, "seconds"
            if (I==100000):
                print time.clock() - start_time, "seconds"
                break





def main2():
    start_time = time.clock()
    with open('C:/Users/Marcus/Desktop/Tableau Datasets/NYC TAXI/testdata1.csv', 'rb') as inputfile, open ('C:/Users/Marcus/Desktop/outputPy.csv','wb') as outputfile:
        I=0
        for line in inputfile:
            lon=line[:line.find(",")]
            lat=line[line.find(",")+1:line.find("/n")]
            lon=lon.strip()
            lat=lat.strip()
            info=getInfo1(lat,lon)
            toWrite=lat+","+lon+","+info+"\n"
            outputfile.write(toWrite)
            I=I+1
            if (I%10==0):
                print "10 done"
                print time.clock() - start_time, "seconds"
            if (I==100):
                print time.clock() - start_time, "seconds"
                break
            
               

def getInfo1(lat,lon):#using PLUTO
    query=makeQuery(lat,lon)
    query2=query.replace(" ","%20")
    url="http://pluto.cartodb.com/api/v2/sql?q="+query2
    #print url
    response = urllib2.urlopen(url)
    html = response.read()
    address=html[html.find("address")+10:html.find(",",html.find("address"))-1]
    boro=html[html.find("borocode")+10:html.find(",",html.find("borocode"))]
    if (boro=='{"type":"number"}'):
        return "null,null,null"
    #info=address+","+boro
    hood=getInfo2(address,boro)
    return address+","+boroughList[int(boro)-1]+","+hood#replace with the address boro and hood



def makeQuery(lat,lon):
    input1=lat+","+lon
    query="WITH subq as (SELECT address,the_geom,ownername,histdist,borocode FROM nyc_mappluto_13v1 ORDER BY the_geom <-> CDB_LatLng("+input1+") LIMIT 20) SELECT address,ownername,histdist,borocode,ST_Distance(the_geom::geography, CDB_LatLng("+input1+")::geography) as distance FROM subq WHERE ST_Distance(the_geom::geography, CDB_LatLng("+input1+")::geography) < 50 ORDER BY ST_Distance(the_geom::geography, CDB_LatLng("+input1+")::geography) ASC LIMIT 3"
    return query

def getInfo2(address,boroNum):
    borough=boroughList[int(boroNum)-1]
    number=address[:address.find(" ")]
    street=address[address.find(" ")+1:].replace(" ","%20")
    url="https://api.cityofnewyork.us/geoclient/v1/address.json?houseNumber="+number+"&street="+street+"&borough="+borough+"&app_id=a2ed8746&app_key=d305a33ba1ada6a3929d1cf543b55d5d"
    response = urllib2.urlopen(url)
    html = response.read()
    hood=html[html.find("ntaName")+10:html.find(",",html.find("ntaName"))-1]
    return hood
