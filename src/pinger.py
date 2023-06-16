from flask import Flask
from flask import request
import os
import datetime
import read
import filesorter
import sys
import json
import time 

app = Flask(__name__)

@app.route('/api/ipdetail/<ip>')
def api_ipdetail(ip):    
    row = 1
    p = os.environ.get('DATA_FOLDER')
    if p is None: 
        raise Exception('no path given')    
    data = read.readIpIterationFiles(p+'/'+ip)    
    returnObj = {}
    for row in data:
        obj=data[row]
        returnObj[row] = {}
        returnObj[row]["ts"]=row
        returnObj[row]["Host"]=obj["Host"]
        returnObj[row]["Stats"]=obj["Stats"]        
    retString=json.dumps(returnObj)
    return retString

@app.route('/ipdetail/<ip>')
def ipdetail(ip):    
    print("route /ipdetail .. ")
    clearCache = False
    cc = request.args.get('reset')
    if len(cc):
        clearCache = True
    row = 1
    p = os.environ.get('DATA_FOLDER')
    if p is None: 
        raise Exception('no path given')    
    data = read.readIpIterationFiles(p+'/'+ip,clearCache)
    retString = '<html><head><title></title><style>.error { background-color:#ff7777; }</style></head><body>'
    bHeader = 0 
    for f in data:
        if bHeader == 0:            
            retString += '<table border="1" style="width:100%"><tr><th>Row</th><th>File</th>'
            for ch in data[f]['Stats']:
                retString += '<th>' + ch + '</th>'
            retString += '</tr>'
            bHeader = 1
        cssClass = ''        
        if data[f]['Stats']['PacketLossPercent'] != "0":            
            timestamp = f.split(".")[0]
            dt = datetime.datetime.fromtimestamp(int(timestamp))
            retString += '<tr class="'+cssClass+'"><td>'+str(row)+'</td><td>'+str(dt)+'</td>'
            row += 1;
            for stat in data[f]['Stats']:
                retString += '<td>' + data[f]['Stats'][stat] + '</td>'
            retString += '</tr>'
    retString += '</table>'            
    retString = retString + '</body></html>'
    return retString

@app.route('/')
def index():
    print("route /index .. ")
    p = os.environ.get('DATA_FOLDER')
    if p is None: 
        raise Exception('no path given')
    ips = read.getIpDirs(p)
    str = ''
    for link in ips:
        str = str + '<a href="/ipdetail/'+link+'">'+link+'</a><br>'
    return str

# main driver function
if __name__ == "__main__":
    p = os.environ.get('DATA_FOLDER')
    if p is None: 
        p = "/pinger-data"
    pt = os.environ.get('DATA_FOLDER_TARGET')
    if pt is None:
        pt = "/pinger-data-target"
    ip = os.environ.get('IP')
    if ip is None:
        raise Exception('no ip given')
    ds = int(os.environ.get('DELTA_SECONDS'))
    if ds is None:
        ds = 10000
    s3bucket = os.environ.get('S3_BUCKET')
    if s3bucket is None: 
        filesorter.filter(p,pt,ip,ds)
    else: 
        if len(s3bucket):
            while True:
                cmd = "aws --profile donkey s3 sync /pinger-data-target/ s3://"+s3bucket+"/"
                os.system(cmd)
                time.sleep(3600) 
