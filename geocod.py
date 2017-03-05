from pygeocoder import Geocoder
from geopy import geocoders
gn = geocoders.GeoNames
import pandas as pd
import numpy as np

gn.geocode("London, UK", exactly_one=False)[0]
