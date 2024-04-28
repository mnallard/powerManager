import os
import re
import subprocess
import time
import json
from utils.functions import Functions


class powerManagerConfiguration:
   name = "powerManagerConfiguration"

   def __init__(self, configurationFile):
      self.configurationFile = configurationFile
      self.confLoaded = 0

   def loadConfiguration(self):
      if not os.path.isfile(self.configurationFile):
         Functions.log("ERR", self.configurationFile +  " does not exists !", "CORE")
         return 0

      try:
         jsonFile = open(self.configurationFile)
      except Exception as err:
         Functions.log("ERR", "Error loading configuration file", "CORE")
         Functions.log("ERR", str(err), "CORE")
         return 0
      with jsonFile as json_data:
         try:
            self.data_dict = json.load(json_data)
         except Exception as err:
            Functions.log(
                    "ERR", "Error parsing configuration file", "CORE")
            Functions.log("ERR", str(err), "CORE")
            jsonFile.close()
            return 0
      jsonFile.close()
      self.confLoaded = 1
      return 1
   
   def checkConfiguration(self):
      if not self.retreiveInfluxDbConf():
         Functions.log("DEAD", "Error getting data from conf file about influxdb properties", "CORE")
         return 0
      if not self.retreivePowerManagerGeneralConfig():
         Functions.log("DEAD", "Error getting data from conf file about general configuration for daemon", "CORE")
         return 0

      if not self.retreivePowerManagerSBUTime():
         Functions.log("DEAD", "Error getting data from conf file about SBU date", "CORE")
         return 0
      return 1 


   def retreiveInfluxDbConf(self):
      if not self.confLoaded:
         Functions.log("ERR", "Error configuration file not opened", "CORE")
         return 0
      if "influxDbConfig" in self.data_dict:
         arr = self.data_dict['influxDbConfig']
         if isinstance(arr, dict):
            for confKey in arr:
               if confKey == "influxDbUrl":
                  self.influxDbUrl = arr[confKey]
               if confKey == "influxDbPort":
                  self.influxDbPort = arr[confKey]
               if confKey == "influxDbName":
                  self.influxDbName = arr[confKey]
         else:
            Functions.log(
                    "ERR", "Error in configuration file format", "CORE")
            return 0
      else:
         Functions.log("ERR", "Error in configuration file format", "CORE")
         return 0
      return 1

   def retreivePowerManagerGeneralConfig(self):
      if not self.confLoaded:
         Functions.log("ERR", "Error configuration file not opened", "CORE")
         return 0
      if "powerManagerGeneralConfig" in self.data_dict:
         arr = self.data_dict['powerManagerGeneralConfig']
         if isinstance(arr, dict):
            for confKey in arr:
               if confKey == "gpioPort4Grid":
                  self.gpioPort4Grid = arr[confKey]
         else:
            Functions.log("ERR", "Error in configuration file format", "CORE")
            return 0
      else:
         Functions.log("ERR", "Error in configuration file format", "CORE")
         return 0
      return 1

   def retreivePowerManagerSBUTime(self):
      if not self.confLoaded:
         Functions.log("ERR", "Error configuration file not opened", "CORE")
         return 0
      if "setToSBUtime" in self.data_dict:
         arr = self.data_dict['setToSBUtime']
         if isinstance(arr, dict):
            for confKey in arr:
               if confKey == "evening":
                  self.SBUEveningTime = arr["evening"]
         else:
            Functions.log("ERR", "Error in configuration file format", "CORE")
            return 0
      else:
         Functions.log("ERR", "Error in configuration file format", "CORE")
         return 0
      return 1

   
   def getInfluxDbUrl(self):
      return self.influxDbUrl

   def getInfluxDbPort(self):
      return self.influxDbPort

   def getInfluxDbName(self):
      return self.influxDbName

   def getGpioPort4Grid(self):
      return self.gpioPort4Grid

   def getSBUEvening(self):
      return self.SBUEveningTime

