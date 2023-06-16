import os 
import json 
import read
import time
import boto3 

def cleanOutDir(dir,targetDir,ip):
    #print("cleanOut: cleaning "+dir+"... ")    
    for item in os.scandir(dir):           
        if item.path.endswith(".json") & item.is_file():
            tmpContent = read.getSingleFileContent(item.path)
            if tmpContent["Stats"]["PacketLossPercent"] != "0":
                #print("found invalid ping data in "+item.name)                    
                isExist = os.path.exists(targetDir)
                if not isExist:                    
                    os.makedirs(targetDir)
                f = open(targetDir+"/"+item.name,"w")
                json.dump(tmpContent,f)
                f.close()        
                #print("renaming "+item.path)
            os.rename(item.path,item.path+".bak")
        elif item.path.endswith(".bak"):
            os.remove(item.path)

def filter(p,pt,ip,ds):
    while True:
        retString = ""
        #print("Filter: filtering "+ip+" from "+p+"to "+pt+", from folders older than "+str(ds)+" seconds")
        ipDir = p+'/'+ip
        ipTargetDir = pt+'/'+ip
        print("Filter: iterate into "+ipDir)
        currentTime = int(time.time())
        threshold = currentTime - ds
        for subDir in os.scandir(ipDir):
            if subDir.is_dir() & subDir.name.isnumeric():
                #print("taversing into "+subDir.name+"... ")
                if int(subDir.name) < threshold:                
                    if len(os.listdir(ipDir+"/"+subDir.name)) == 0:
                        os.rmdir(ipDir+"/"+subDir.name)
                    else: 
                        cleanOutDir(ipDir+"/"+subDir.name,ipTargetDir+"/"+subDir.name,ip)
            else:             
                print(subDir.name + " is not a valid directory, skipping.")        
        time.sleep(600) 
    return retString

