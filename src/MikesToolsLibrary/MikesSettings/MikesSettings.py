#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
__version__ = "0.1.2.00237-dev"
__author__ = "Mike Merrett"
__updated__ = "2025-12-18 21:03:17"
###############################################################################

"""
    MySettings.py

to setup just import it and everything should be ready to go
    - it will look for a config.ini in the parent dir if not found it will use the current directory config.ini

you pre set a list as you go to save settings at the end or something:
            (particularly useful with all the windows/tkinter stuff)
                                ( section,     name,         the function to call when ready ,  the type of the value)
    mySettings.addToLaterSaveList('Panels', 'VertHeight', lambda: vert_paned.sash_coord(0)[1], mySettings.fldType.Int)
    mySettings.doTheSaveLater()
"""

import os
import sys
import configparser
import base64
import json
from datetime import datetime
from enum import Enum
from pprint import pformat
from venv import logger



class MikesSettings:

    class fldType(Enum):
        Bool = "Bool"
        Int = "Int"
        Str = "Str"
        Float = "Float"
        Json = "Json"
        ByteArray = "ByteArray"

    # INIfile = 'config.ini'
    # curApp = 'unknown'

    config = None

    isShowingDebug = False

    resetSettings = {"runcounters": ("General", 4, fldType.Int)}

    # -----------------------------------------------------------------
    def __init__(self, fn, appName = None, showDebug=False) -> None:

        if appName is None:
            self.curApp = (os.path.basename(fn)).replace(".py", "")
        else:
            self.curApp = appName

        logger.traced( f" MikesSettings __init__ called with fn = {fn}  showDebug = {showDebug} " )
        logger.tracee( f" curApp = {self.curApp} " )

        self.config = configparser.ConfigParser(
            allow_no_value=True,
            interpolation=configparser.BasicInterpolation()
        )
        self.suspendedAutoSave = False
        self.saveLaterList = []
        self.INIfile = fn

        if os.path.exists(self.INIfile):
            self.config.read(self.INIfile)
        else:
            self.reset()

        if not self.config.has_section(self.curApp):
            self.config.add_section(self.curApp)

        if self.isShowingDebug:
            self.dump()

    # -----------------------------------------------------------------
    def __str__(self) -> None:
        s = "Config Dump: "
        # s += os.linesep
        absolute_path = os.path.abspath(self.INIfile)
        s += absolute_path
        s += os.linesep

        s+= f"               curApp = {self.curApp}"
        s += os.linesep

        config_dict = {section: dict(self.config.items(section)) for section in self.config.sections()}
        s += pformat( config_dict)
        s += os.linesep

        if len(self.saveLaterList) > 0:
            s += "Save Later List:" + os.linesep
            for i in self.saveLaterList:
                s += f'      {i["section"]=}  {i["name"]=}-> {str(i["callback"])=} : {i["varType"]=}'
                s += os.linesep
            s += os.linesep
        return s

    # -----------------------------------------------------------------
    @classmethod
    def findConfigFile(cls, fnName:str = None) -> str | str:

        """
        Searches for the configuration file in the current and parent directories.
        Returns the absolute path if found, otherwise None.
        """
        if fnName is None:
            fn = "config.ini"
        else:
            fn = fnName

        current_dir = os.path.abspath(os.getcwd())
        root_dir = os.path.abspath(os.sep)

        while True:
            potential_path = os.path.join(current_dir, fn)
            if os.path.isfile(potential_path):
                return potential_path
            if current_dir == root_dir:
                break
            current_dir = os.path.dirname(current_dir)

        return None

    # -----------------------------------------------------------------
    def setAutoSaveOn(self, isAutoSaveOn: bool):
        self.suspendedAutoSave = isAutoSaveOn

    # -----------------------------------------------------------------
    def registerToSaveList(self, section, name, callback, varType):
        self.saveLaterList.append(
            {"section": section, "name": name, "callback": callback, "varType": varType}
        )


    # -----------------------------------------------------------------
    def processSaveLater(self):
        self.suspendedAutoSave = True
        # print("------------------------- doTheSaveLater ----------------")
        for i in self.saveLaterList:

            cb = i["callback"]
            if callable(cb):
                val = cb()
                ##print(f'[{i["section"]}].{i["name"]}->{val}')
                match (i["varType"]):
                    case self.fldType.Bool:
                        self.setBool(i["section"], i["name"], val)
                    case self.fldType.Int:
                        self.setInt(i["section"], i["name"], val)
                    case self.fldType.Float:
                        self.setFloat(i["section"], i["name"], val)
                    case self.fldType.Json:
                        self.setJson(i["section"], i["name"], val)
                    case self.fldType.ByteArray:
                        self.setByteArray(i["section"], i["name"], val)
                    case _:
                        self.setStr(i["section"], i["name"], val)
            self.writeConfig()
        self.suspendedAutoSave = False
        # print("-------------------------------------------------------")


    # -----------------------------------------------------------------
    def reset(self):
        for k, v in self.resetSettings.items():
            match (v[2]):
                case MikesSettings.fldType.Bool:
                    self.setBool(v[0], k, v[1])
                case MikesSettings.fldType.Int:
                    self.setStr(v[0], k, str(v[1]))
                case MikesSettings.fldType.Float:
                    self.setFloat(v[0], k, str(v[1]))
                case MikesSettings.fldType.Json:
                    self.setJson(v[0], k, v[1])
                case MikesSettings.fldType.ByteArray:
                    self.setByteArray(v[0], k, v[1])
                case MikesSettings.fldType.Str:
                    self.setStr(v[0], k, str(v[1]))

        self.writeConfig()

    # -----------------------------------------------------------------
    def save(self):
        self.writeConfig()

    # -----------------------------------------------------------------
    def writeConfig(self) -> None:
        if self.isShowingDebug:
            self.dump()

        with open(self.INIfile, "w") as configfile:
            self.config.write(configfile)
        pass

    # -----------------------------------------------------------------
    def getRunCounter(self) -> int:

        if not self.config.has_section(self.curApp):
            self.config.add_section(self.curApp)

        ver = self.config.getint(self.curApp, "RunCounters", fallback=0)

        # update the ini now (just incase it doesnt get written later)
        self.config.set(self.curApp, "RunCounters", str(ver + 1))
        self.config.set(self.curApp, "LastRunTime", str(datetime.now()))

        if not self.suspendedAutoSave:
            self.writeConfig()
        return ver

    # -----------------------------------------------------------------
    def __call__(self, section, key, fallbackVal=None):
        # Try to infer the type from the fallback value
        if isinstance(fallbackVal, bool):
            return self.getBool(section, key, fallbackVal)
        elif isinstance(fallbackVal, int):
            return self.getInt(section, key, fallbackVal)
        elif isinstance(fallbackVal, float):
            return self.getFloat(section, key, fallbackVal)
        elif isinstance(fallbackVal, dict):
            return self.getJson(section, key, fallbackVal)
        elif isinstance(fallbackVal, (bytes, bytearray)):
            return self.getByteArray(section, key, fallbackVal)
        else:
            return self.getStr(section, key, fallbackVal)

    # -----------------------------------------------------------------
    def doesExist(self, section, key):
        if not self.config.has_section:
            return False
        return self.config.has_option(section, key)

    # -----------------------------------------------------------------
    def getBool(self, section, key: str, fallbackVal: bool) -> bool:
        return self.config.getboolean(section, key, fallback=fallbackVal)
        # return var

    # -----------------------------------------------------------------
    def setBool(self, section, key: str, value: bool) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        if not self.suspendedAutoSave:
            self.writeConfig()

    # -----------------------------------------------------------------
    def getFloat(self, section, key: str, fallbackVal: float = 0.0) -> float:
        if not self.config.has_section(section):
            self.config.add_section(section)
        return self.config.getfloat(section, key, fallback=fallbackVal)

    # -----------------------------------------------------------------
    def setFloat(self, section, key: str, value: float) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        if not self.suspendedAutoSave:
            self.writeConfig()

    # -----------------------------------------------------------------
    def getInt(self, section, key, fallbackVal=0) -> int:
        if not self.config.has_section(section):
            self.config.add_section(section)
        return self.config.getint(section, key, fallback=fallbackVal)

    # -----------------------------------------------------------------
    def setInt(self, section, key, value: int) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        if not self.suspendedAutoSave:
            self.writeConfig()

    # -----------------------------------------------------------------
    def getStr(self, section, key, fallbackVal="") -> str | None:
        return self.config.get(section, key, fallback=fallbackVal)

    # -----------------------------------------------------------------
    def setStr(self, section, key, value) -> None:
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        if not self.suspendedAutoSave:
            self.writeConfig()

    # -----------------------------------------------------------------
    def setByteArray(self, section, key, value):
        encode_bytes = base64.b64encode(value).decode("utf-8")
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, encode_bytes)
        if not self.suspendedAutoSave:
            self.writeConfig()

    # -----------------------------------------------------------------
    def getByteArray(self, section, key, fallbackVal=b"\x00"):
        val = self.config.get(section, key, fallback=None)
        if val is None:
            return fallbackVal
        try:
            return base64.b64decode(val)
        except Exception:
            if isinstance(fallbackVal, bytearray):
                return fallbackVal
            try:
                return base64.b64decode(val)
            except Exception:
                return fallbackVal

    # -----------------------------------------------------------------
    def setJson(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        val = json.dumps(value)
        self.config.set(section, key, val)
        if not self.suspendedAutoSave:
            self.writeConfig()

    # -----------------------------------------------------------------
    def getJson(self, section, key, fallbackVal=""):
        val = self.config.get(section, key, fallback=None)
        if val is None:
            return fallbackVal
        try:
            return json.loads(val)
        except Exception:
            # If fallbackVal is a dict, return it; if it's a string, try to load it as JSON
            if isinstance(fallbackVal, dict):
                return fallbackVal
            try:
                return json.loads(fallbackVal)
            except Exception:
                return fallbackVal

    # -----------------------------------------------------------------
    def items(self, section):
        return self.config.items(section)

    # -----------------------------------------------------------------
    def giveINIfile(self):
        return os.path.abspath(self.INIfile)

    # -----------------------------------------------------------------
    def dump(self):

        x = self.getEnv('USERNAME')
        print(f'getEnv()={x}')

        x = self.getEnv('TEMP')
        print(f'getEnv()={x}')

        x = os.environ.get('TEMP')
        print(f'os.environ.get()={x}')

        p = self.config.get('GlobalAttachmentRepository', 'db_password')

        print( p)
        print ( str(hash(p)))

    #     print('##############')

    # # # # # # # # #     from cryptography.fernet import Fernet
    # # # # # # # # # #     # Put this somewhere safe!
    # # # # # # # # #     key = Fernet.generate_key()
    # # # # # # # # #     print("key=", key)
    # # # # # # # # #     f = Fernet(key)
    # # # # # # # # #     token = f.encrypt(b"A really secret message. Not for prying eyes.")

    # # # # # # # # #     token = f.encrypt(b"Mikes5Music8Copie3Organizer43")
    # # # # # # # # #     print("token=",token)
    # # # # # # # # # #     #token
    # # # # # # # # # #     #b'...'
    # # # # # # # # #     x = f.decrypt(token)
    # # # # # # # # #     print("decrypt=",x)
    #     #b'A really secret message. Not for prying eyes.'
    #     print('$$$$$$$$$$$$$')

    #     import keyring
    #     keyring.set_password('GlobalAttachmentRepository', 'username','password')

    #     pwd = keyring.get_password('GlobalAttachmentRepository','sde',)
    #     print(pwd)
    #     print('@@@@@@@@@')


# if os.path.exists("../config.ini"):
#     fn = "../config.ini"
# else:
#     fn = "config.ini"

# mySettings = MikesSettings(fn)



# -----------------------------------------------------------------
if __name__ == "__main__":
    print("this must be called from another module")

    # mySettings.dump()

    sys.exit(-99)
