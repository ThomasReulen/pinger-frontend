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
                fileContents[item.name] = getSingleFileContent(item.path)                
    return fileContents 


def readIpIterationFiles(ipDir):
    print("iterate into "+ipDir)
    iterationFiles = {}
    with os.scandir(ipDir) as iteration:
        for subDir in iteration:
            if subDir.is_dir():
                iterationFiles.update(getFileContents(subDir.path))
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

