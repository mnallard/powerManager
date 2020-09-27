import glob
import time
import sys
import os
import re
import importlib
import threading
import traceback
import socket
import select
import json
import time
from utils.functions import Functions
from os import listdir
from utils.powerManagerConfiguration import powerManagerConfiguration
from utils.gridPower import gridPower

def checkParameter(args):
   Functions.log(
      "INF", "Entering in checkParameter #parameters=" + str(len(args)), "CORE")
   if (len(args) == 1):
      Functions.log(
          "DEAD", "At least provide one parameter : Configuration file for daemon", "CORE")
      return 0
   return 1


def main():
   Functions.log("INF","Starting powerGridOff", "CORE")
   if checkParameter(sys.argv) == 0:
      exit(0)
   powerManagerConfig = powerManagerConfiguration(sys.argv[1:][0])

   powerManagerConfig=powerManagerConfiguration(sys.argv[1:][0])
   if not powerManagerConfig.loadConfiguration():
      Functions.log("DEAD", "Unable to load power manager configuration", "CORE")
      exit(1)
   if not powerManagerConfig.checkConfiguration():
      Functions.log("DEAD", "Insuffisant power manager configuration to continue", "CORE")
      exit(1)
   Functions.log("INF", "Instantiation of new gridPowerObjet", "CORE")
   myGridPower=gridPower(powerManagerConfig.getGpioPort4Grid())
   myGridPower.setGridOff()
   Functions.log("INF", "Setting grid off","CORE")
   Functions.log("INF", "Ending powerGridOff", "CORE")

if __name__ == "__main__":
    main()
