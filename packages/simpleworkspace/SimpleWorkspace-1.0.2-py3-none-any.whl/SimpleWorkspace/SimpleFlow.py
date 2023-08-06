import os

def LevelPrint(level, msg=None):
    for i in range(level):
        print("    ",end="", flush=True)
    if(msg != None):
        print(msg)

def LevelInput(level, msg=""):
    LevelPrint(level)
    return input(msg)

def AnyKeyDialog(msg=""):
    if(msg == ""):
        input("Press enter to continue...")
    else:
        input(msg+ " - Press enter to continue...")

def ClearConsoleWindow():
    os.system('cls' if os.name=='nt' else 'clear')
    return

def Print_SelectFileDialog(printlevel=1):
    LevelPrint(printlevel, "-Enter File Path:")
    FilePath = LevelInput(printlevel, "-")
    if os.path.exists(FilePath) == False:
        LevelPrint(printlevel+1, "-No such file found...")
        return None
    return FilePath
    
def StringToInteger(text:str, min=None, max=None, lessThan=None, moreThan=None) -> int | None:
    try:
        tmp = int(text)
        if(min != None):
            if(tmp<min):
                return None
        elif(moreThan != None):
            if(tmp <= moreThan):
                return None
        if(max != None):
            if(tmp > max):
                return None
        elif(lessThan != None):
            if(tmp >= lessThan):
                return None
        return tmp
    except Exception:
        return None
