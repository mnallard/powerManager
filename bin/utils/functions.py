import datetime
import subprocess
import re
import sys
import threading
import os

class Functions:

    logLevel = {"ERR": 0,
                "INF": 1,
                "DBG": 2,
                "DEAD": 3
                }
    lLevel = 1
    fileLog=None
    logPath="/users/powerManager/log"
    @staticmethod
    def log(level, message, source):
        if Functions.fileLog == None:
            if not os.path.exists(Functions.logPath):
                os.mkdir(Functions.logPath, mode = 0o777)
            Functions.fileLog = open(Functions.logPath+"/daemonP.log", "a")
            print ("Opening "+Functions.logPath+"/daemonP.log file")
        date = str(datetime.datetime.now())
        message = date + " " + \
            "[" + threading.current_thread().name + "] " + level + \
            " " + source + " " + message
        Functions.fileLog.write(message+'\n')
        Functions.fileLog.flush()
        if (level in Functions.logLevel):
            levelValue = Functions.logLevel[level]
            if (levelValue<=Functions.lLevel):
                print(message)
            if (level == "DEAD"):
                print(message)
                sys.exit(1)

    @staticmethod
    def setLogLevel(level):
        if (level in Functions.logLevel):
            Functions.lLevel = Functions.logLevel[level]
            return 1
        return 0

