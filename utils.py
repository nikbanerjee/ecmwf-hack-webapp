import pprint
import sys
import os
import json
import time
from pprint import pprint
import requests

from datetime import datetime
from dateutil import parser

import datetime
import numpy as np
import re
import glob

def write_file(file, data):
    with open(file, 'r+') as outfile:
        outfile.write(data)

def write_file_noappend(file, data):
    with open(file, 'w') as outfile:
        outfile.write(data)


def read_file(file):
    with open(file, 'r') as outfile:
        return outfile.read()


def pp_json(json_thing, sort=True, indents=4):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None