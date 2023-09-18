
import os
import datetime
import read
import filesorter
import sys
import json
import time 


# main driver function
if __name__ == "__main__":
    p = "/pinger-data"
    pt = "/pinger-data-target"
    ip = "8.8.8.8"
    ds = 10000 
    clearCache = False     
    data = read.readIpIterationFiles(p+'/'+ip,clearCache)
    #print(data)
    
