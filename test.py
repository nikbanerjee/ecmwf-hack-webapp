from netCDF4 import Dataset
import numpy as np
import json


#lons = dataset.variables['longitude'][:]
#lats = dataset.variables['latitude'][:]
#tmax = dataset.variables['time'][:]

#tmax_units = dataset.variables['time'].units


#print(dataset.variables)
#print(dataset.variables['sst'][0][0])
#print(dataset.variables['t2m'][0])
#print(dataset.variables['sst'][0])
#print(dataset.variables['sd'][0])
#print(dataset.variables['mcc'][0])
#print(dataset.variables['sund'][0])
#print(dataset.variables['tp'][0])
def k2c(t):
    return t-273.15
cities = ["London", "Copenhagen", "Oslo", "Bucharest"]
images = [
    "https://www.city.ac.uk/__data/assets/image/0009/328797/building-partnerships.jpg",
    "https://ems2016.org/wp-content/uploads/2015/04/copenhagen_featured.jpg",
    "https://linkarkitektur.com/var/linkarkitektur/storage/images/prosjekter/context-oslo-hovinbyen/context-oslo-hovinbyen/356889-1-nor-NO/Context-Oslo-Hovinbyen_fp_proj_slide_img.jpg",
    "http://blog.parkinn.com/wp-content/uploads/sites/7/2016/01/BP2-BUHPD-Creative-Labs-Shutterstock-Bucharest-is-an-up-and-coming-city-filled-to-the-brim-with-exciting-sights-and-activities.-Check-out-our-top-5-list.jpg"

]
#dataset = Dataset('London.nc', format="NETCDF4")

#sst = sea surface tempearture in kelvin
#sd = thickness of snow m of water equiv.
#t2m = 2 metre temperature
#mcc = medium cloud cover
#sund = sunshine duration
#tp = total precipitation
#print("%.2f" % round(k2c(np.mean(dataset.variables['t2m'][0])),2))
#print("%.2f" % round(k2c(np.mean(dataset.variables['sst'][0])),2))
#print("%.2f" % round(np.mean(dataset.variables['sd'][0]),2))
#print("%.2f" % round(np.mean(dataset.variables['mcc'][0]),2))
#print("%.2f" % round(np.mean(dataset.variables['sund'][0]),2))
#print("%.2f" % round(np.mean(dataset.variables['tp'][0]),2))

def getNetCDF4Data(city):
    dataset = Dataset("{}.nc".format(city), format="NETCDF4")
    return [
        "%.2f" % round(k2c(np.mean(dataset.variables['t2m'][0])), 2),
        "%.2f" % round(k2c(np.mean(dataset.variables['sst'][0])), 2),
        "%.2f" % round(np.mean(dataset.variables['tp'][0]), 2),
        "%.2f" % round(np.mean(dataset.variables['mcc'][0]), 2),
        "%.2f" % round(np.mean(dataset.variables['sund'][0]), 2),
        "%.2f" % round(np.mean(dataset.variables['sd'][0]), 2)

    ]
import datetime
def secs_to_MS(secs):
    return str(datetime.timedelta(seconds=secs))

x = 0
outputJson = []
description = ""
while x < len(cities):
    print(cities[x])
    data = getNetCDF4Data(cities[x])
    surface_temp = str(data[0])
    seconds = int(float(data[4]))+10800
    adict = {
        "description": description,
        "image": images[x],
        "location": cities[x],
        "matched": "false",
        "metrics": {
            "surface_temp": str(data[0]),
            "sea_temp": str(data[1]),
            "precipitation": str(data[2]),
            "cloud_coverage": str(data[3]),
            "sun_duration": str(secs_to_MS(seconds)),
            "snow_thickness": str(data[5])
        },
        "seen": "false"
    }
    outputJson.append(adict)
    x+=1

with open('data.json', 'w') as outfile:
    json.dump(outputJson, outfile)

#for var in dataset.variables.values():
#    print(var)

