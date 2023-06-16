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
                fileContents[os.path.splitext(item.name)[0]] = getSingleFileContent(item.path)                
    return fileContents 


def readIpIterationFiles(ipDir,clearCache):
    print("iterate into "+ipDir)
    if os.path.isfile(ipDir+".json") & clearCache:
        os.remove(ipDir+".json")
    if os.path.isfile(ipDir+".json"):
        f = open(ipDir+".json","r")                                
        iterationFiles = json.loads(f.read())
        f.close()
    else: 
        iterationFiles = {}
        with os.scandir(ipDir) as iteration:
            for subDir in iteration:            
                tmpFilePath = ipDir + "/" + subDir.name + ".json"
                if subDir.is_dir() and os.path.isfile(tmpFilePath):
                    f = open(tmpFilePath,"r")                                
                    tmpContent = json.loads(f.read())
                    f.close()
                elif subDir.is_dir():
                    tmpContent = getFileContents(subDir.path)                    
                    if len(tmpContent) == 250:
                        f = open(tmpFilePath,"w")
                        json.dump(tmpContent,f)
                        f.close()                        
                iterationFiles.update(tmpContent)        
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

