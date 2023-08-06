from genericpath import exists, isfile
from pathlib import Path
import hashlib
import os
import sys
from typing import Callable
from SimpleWorkspace.SimpleConversion import ByteConversion
import queue
import re


class FileContainer:
    """
    example case: a/b/test.exe\n
    - filename      = test\n
    - fileExtension = .exe\n
    - tail          = a/b/\n
    - head          = test.exe\n
    - rawPath       = a/b/test.exe\n

    - If no match can be found for any property, they will default to empty string
    """

    tail = ""
    head = ""
    filename = ""
    fileExtension = ""
    rawPath = ""

    def __init__(self, filepath) -> None:
        self.rawPath = filepath
        headTail = os.path.split(filepath)
        self.tail = headTail[0]
        if self.tail != "":
            self.tail += "/"
        self.head = headTail[1]
        baseName = headTail[1]

        fullFilename = baseName.rsplit(".", 1)
        self.filename = fullFilename[0]
        if len(fullFilename) == 2:
            self.fileExtension = "." + fullFilename[1]


def Directory_ListFiles(searchDir: str, callback: Callable[[str], None] = None, includeDirs=True, includeFilter=None, satisfiedCondition: Callable[[str], bool] = None):
    """
    includeFilter:
     options takes a regex which searches full path of each file, if anyone matches a callback is called. Is not case sensitive
    satisfiedCondition:
     takes a callback that returns a bool, if it returns true, no more search is performed
    """
    
    if not os.path.exists(searchDir):
        return

    folders = queue.Queue()
    folders.put(searchDir)
    while folders.qsize() != 0:
        currentFolder = folders.get()
        try:
            currentFiles = os.listdir(currentFolder)
            for filePath in currentFiles:
                filePath = os.path.join(currentFolder, filePath)
                pathMatchesIncludeFilter = (includeFilter == None or re.search(includeFilter, filePath, re.IGNORECASE))
                if os.path.isfile(filePath):
                    if pathMatchesIncludeFilter:
                        callback(filePath)
                    if satisfiedCondition != None and satisfiedCondition(filePath):
                        return
                else:
                    if includeDirs:
                        if pathMatchesIncludeFilter:
                            callback(filePath)
                        if satisfiedCondition != None and satisfiedCondition(filePath):
                            return
                    folders.put(filePath)
        except Exception as e:
            pass


def File_SHA256(filePath):
    sha256 = hashlib.sha256()
    File_Read(filePath, lambda x: sha256.update(x), readSize=ByteConversion.MB * 1, getBytes=True)
    return sha256.hexdigest()


def File_Read(filePath: str, callback: Callable[[str], None] = None, readSize=-1, readLimit=-1, getBytes=True):
    """
    :(opt) callback: call a lambda function each time a file is read with the readSize\n
    - if no callback is used, a return value with file content will be returned\n
    :(opt) readSize: amount of bytes to read at each callback, default of -1 reads all at once\n
    :(opt) ReadLimit: Max amount of bytes to read, default -1 reads until end of file\n
    :(opt) getBytes: default True, specifies if the return data is in string or bytes format\n
    """

    content = b""
    openMode = "rb"
    if getBytes == False:
        openMode = "r"
        content = ""

    if (readSize == -1 and readLimit >= 0) or (readLimit < readSize and readLimit >= 0):
        readSize = readLimit
    totalRead = 0
    with open(filePath, openMode) as file:
        while True:
            if readLimit != -1 and totalRead >= readLimit:
                break
            data = file.read(readSize)
            totalRead += readSize
            if data:
                if callback == None:
                    content += data
                else:
                    callback(data)
            else:
                break
    return content


def Directory_Create(path: str):
    os.makedirs(path, exist_ok=True)


def Path_FindEmptySpot(filepath: str):
    fileContainer = FileContainer(filepath)
    TmpPath = fileContainer.tail + fileContainer.filename + fileContainer.fileEnding
    i = 1
    while os.path.exists(TmpPath) == True:
        TmpPath = fileContainer.tail + fileContainer.filename + "(" + str(i) + ")" + fileContainer.fileEnding
        i += 1
    return TmpPath


def File_Create(filepath: str, data=None):
    openMode = "wb"
    if type(data) is str:
        openMode = "w"
    with open(filepath, openMode) as file:
        if data is not None:
            file.write(data)


def File_Append(filepath:str, data: bytes | str):
    openMode = None
    if type(data) is bytes:
        openMode = "ab"
    elif type(data) is str:
        openMode = "a"
    else:
        raise Exception("Bytes or string can be used to append to file")
    with open(filepath, openMode) as file:
        file.write(data)


def RequireModules(modules: list[str]):
    import sys
    import importlib
    import pkg_resources
    import subprocess

    required = modules
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Please wait a moment, application is missing some modules. These will be installed automatically...")
        python = sys.executable
        for i in missing:
            try:
                subprocess.check_call([python, "-m", "pip", "install", i])
            except Exception as e:
                pass
    importlib.reload(pkg_resources)
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Not all required modules could automatically be installed!")
        print("Please install the modules below manually:")
        for i in missing:
            print("    -" + i)
        return False
    return True
