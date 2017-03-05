{
    "url": "https://api.ecmwf.int/v1",
    "key": "cab64e837b3fa434f5c03ae787cd642f",
    "email": "simionp96@gmail.com"
}

from ecmwfapi import ECMWFDataServer
'''
server = ECMWFDataServer(url="https://api.ecmwf.int/v1", key="cab64e837b3fa434f5c03ae787cd642f", email="simionp96@gmail.com")
server.retrieve({
        'stream': "oper",
        'levtype': "sfc",
        'param': "167",
        'dataset': "interim",
        'step': "0",
        'grid': "0.5/0.5",
        'area': "90/-180/-90/179.5",
        'time': "00/06/12/18",
        'date': "2014-07-01/tlo/2014-07-31",
        'type': "an",
        'class': "ei",
        'target': "test.nc",
		'format': "netcdf"
    })
    '''

#london
lats = ["51.507351", "55.676097", "59.913869", "44.426767", "50.850340", "50.110922", "46.204391", "40.416775", "38.722252", "45.764043", "41.902783", "47.497912","52.229676"]
longs = ["-0.127758", "12.568337", "10.752245", "26.102538", "4.351710", "8.682127", "6.143158", "-3.703790", "-9.139337", "4.835659", "12.496366", "19.040235", "21.012229"]
filenames = ["London", "Copenhagen", "Oslo", "Bucharest", "Brussels", "Frankfurt", "Geneva", "Madrid", "Lisbon", "Lyon", "Rome", "Budapest", "Warsaw"]

def getFiles(filename, lat, long):
    from ecmwfapi import ECMWFDataServer
    server = ECMWFDataServer(url="https://api.ecmwf.int/v1", key="cab64e837b3fa434f5c03ae787cd642f",
                             email="simionp96@gmail.com")
    server.retrieve({
        "class": "ei",
        "dataset": "interim",
        "date": "2016-04-15",
        "expver": "1",
        "grid": "0.75/0.75",
        'area': "{}/{}/{}/{}".format(lat, long, lat, long),
        "levtype": "sfc",
        "param": "34.128/141.128/167.128/187.128/189.128/228.128",
        "step": "3",
        "stream": "oper",
        "time": "12:00:00",
        "type": "fc",
        "target": ""+filename+".nc",
        "format": "netcdf"
    })

x = 0
while x < len(filenames):
    getFiles(filenames[x], lats[x], longs[x])
    x+=1