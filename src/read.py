import os 
import json 


def getIpDirs(datadir):
    ips = {}
    with os.scandir(datadir) as root_dir:
        for path in root_dir:
            if path.is_file():
                print("skipping "+path.name)
            if path.is_dir():
                print("is a dir: "+path.name)            
                ips[path.name] = path.path
    return ips


def getSingleFileContent(filePath):
    fileObj = open(filePath,"r")
    fileContent = fileObj.read()
    fileDict = json.loads(fileContent)
    fileObj.close()
    return fileDict

def getFileContents(filesPath):
    fileContents = {}
    print("get files from "+filesPath)
    with os.scandir(filesPath) as files:
        for item in files:
            if item.is_file():
                tmp = getSingleFileContent(item.path)                
                if tmp["Stats"]["PacketLossPercent"] > "0":
                    print(tmp["Stats"]["PacketLossPercent"])
                    fileContents[os.path.splitext(item.name)[0]] = tmp
                else: 
                    print("empty should be: "+os.path.splitext(item.name)[0])
                    fileContents[os.path.splitext(item.name)[0]] = {}                    
    return fileContents 


def readIpIterationFiles(ipDir,clearCache):
    print("iterate into "+ipDir)
    if os.path.isfile(ipDir+".json") & clearCache:
        print("clear cache ...")
        os.remove(ipDir+".json")
    if os.path.isfile(ipDir+".json"):
        print("found file" + ipDir+".json")
        f = open(ipDir+".json","r")                                
        iterationFiles = json.loads(f.read())
        f.close()
    else: 
        print("no file found, create one..")
        iterationFiles = {}
        with os.scandir(ipDir) as iteration:
            #print("iteration "+iteration)
            for subDir in iteration:        
                print("subDir "+subDir.name)                       
                tmpFilePath = ipDir + "/" + subDir.name + ".json"
                print("is file? "+tmpFilePath)
                print(os.path.isfile(tmpFilePath))
                if subDir.is_dir() and os.path.isfile(tmpFilePath):
                    print("read file")
                    f = open(tmpFilePath,"r")                                
                    tmpContent = json.loads(f.read())                    
                    iterationFiles.update(tmpContent)        
                    f.close()
                elif subDir.is_dir():
                    print("subdir is dir, so create file")
                    tmpContent = getFileContents(subDir.path)                    
                    f = open(tmpFilePath,"w")
                    json.dump(tmpContent,f)
                    f.close()     
                    iterationFiles.update(tmpContent)
                else:
                    print("no file and no dir, something else")
        f = open(ipDir+".json","w")
        json.dump(iterationFiles,f)
        f.close()        
    return iterationFiles


def readData(datadir):
    ips = {}
    with os.scandir(datadir) as root_dir:
        for path in root_dir:
            if path.is_file():
                print("skipping "+path.name)
            if path.is_dir():
                print("is a dir: "+path.name)            
                ips[path.name] = readIpIterationFiles(path.path)    
    return 'Hello from read!'

