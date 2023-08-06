import shutil
from  SimpleWorkspace.SimpleFlow import *
import SimpleWorkspace.appdirs as appdirs
import configparser
import os
import subprocess
import sys

sessionEnvObj = []


class SettingsConfig:
    __settingsFileName = "settings.ini"
    def __init__(self, ProgramName, companyName=None):
        self.__Author = companyName
        self.__Filename = ProgramName
        self.__config = None
        self.__configDict = None
        self.appdataPath = os.path.join(appdirs.user_data_dir(ProgramName, self.__Author))
        self.__settingsDir = self.appdataPath
        self.__settingsFile = os.path.join(self.__settingsDir, self.__settingsFileName)
        self.__DeleteCommand = "#delete"
        self.LoadSettings()
        return

    def GetAllSettings(self):
        return self.__configDict

    def AddSetting(self, Key, Value):
        self.__configDict[Key] = str(Value)
        return

    def GetSetting(self, Key):
        if(Key in self.__configDict):
            return self.__configDict[Key]
        else:
            return None

    def DeleteSetting(self,key):
        if(key in self.__configDict):
            del self.__configDict[key]
        return

    def DefaultSettings(self):
        self.GetAllSettings().clear()
        return

    def SaveSettings(self):
        self.__CreateConfigStructure()
        with open(self.__settingsFile, "w") as configFile:
            self.__config.write(configFile)
        self.LoadSettings()
        return

    def LoadSettings(self):
        if(os.path.exists(self.__settingsFile) == True):
            self.__config = configparser.ConfigParser()
            self.__configDict = self.__config['DEFAULT'] #namespace
            self.__config.read(self.__settingsFile)
        else:
            self.__config = configparser.ConfigParser()
            self.__configDict = self.__config['DEFAULT'] #namespace
            self.SaveSettings()
        return

    def __RemoveSettingsFile(self):
        if(os.path.exists(self.__settingsDir) == True):
            shutil.rmtree(self.__settingsDir)
            self.DefaultSettings()
        return

    def __CreateConfigStructure(self):
        if not os.path.exists(self.__settingsDir):
            os.makedirs(self.__settingsDir)
        if(os.path.exists(self.__settingsFile) == False):
            f = open(self.__settingsFile, "w")
            f.close()
        return

    def __ChangeSettings(self):
        while(True):
            ClearConsoleWindow()
            LevelPrint(0,"[Change Settings]")
            LevelPrint(1,"0. Save Settings and go back.(Type cancel to discard changes)")
            LevelPrint(1,"1. Add a new setting")
            LevelPrint(2, "[Current Settings]")
            dictlist = []
            dictlist_start = 2
            dictlist_count = 2
            for key in self.__configDict:
                LevelPrint(3,str(dictlist_count) + ". " + key + " : " + self.__configDict[key])
                dictlist.append(key)
                dictlist_count+=1
            LevelPrint(1)
            choice = input("-Choice: ")
            if(choice == "cancel"):
                self.LoadSettings()
                AnyKeyDialog("Discarded changes!")
                break
            if(choice == '0'):
                self.SaveSettings()
                LevelPrint(1)
                AnyKeyDialog("Saved Settings!")
                break
            elif(choice == '1'):
                LevelPrint(1, "Setting Name:")
                keyChoice = LevelInput(1,"-")
                LevelPrint(1, "Setting Value")
                valueChoice = LevelInput(1,"-")
                self.AddSetting(keyChoice, valueChoice)
            else:
                IntChoice = StringToInteger(choice, min=dictlist_start, lessThan=dictlist_count)
                if(IntChoice == None):
                    continue
                else:
                    key = dictlist[IntChoice-dictlist_start]
                    LevelPrint(2, '(Leave empty to cancel, or type "' +self.__DeleteCommand + '" to remove setting)')
                    LevelPrint(2, ">> " + self.__configDict[key])
                    choice = LevelInput(2, "Enter new value: ")
                    if(choice == ""):
                        continue
                    elif(choice == self.__DeleteCommand):
                        self.DeleteSetting(key)
                    else:
                        self.__configDict[key] = choice
        return

    def SettingsMenu(self):
        ClearConsoleWindow()
        LevelPrint(0,"[Settings Menu]")
        LevelPrint(1,"1.Change settings")
        LevelPrint(1,"2.Reset settings")
        LevelPrint(1,"3.Open Settings Directory")
        LevelPrint(1,"0.Go back")
        LevelPrint(1)
        choice = input('-')
        if(choice == '1'):
            self.__ChangeSettings()
        elif choice == '2':
            LevelPrint(1, "-Confirm Reset! (y/n)")
            LevelPrint(1)
            choice = input('-')
            if(choice == "y"):
                self.__RemoveSettingsFile()
                LevelPrint(1)
                AnyKeyDialog("*Settings resetted!")
        elif(choice == '3'):
            os.startfile(self.__settingsDir)
        else:
            return
        return


