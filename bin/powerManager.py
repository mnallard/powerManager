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
from datetime import datetime


from utils.functions import Functions
from os import listdir
from utils.powerManagerConfiguration import powerManagerConfiguration
from utils.gridPower import gridPower
from utils.myInfluxDb import myInfluxDb
daemonUptime = time.time()

minBatCapacity=20.0
maxBatCurrent=-100.0
batReturnToSUB=20.0
allowSBUBatCapacity=70.0

def checkParameter(args):
   Functions.log(
      "INF", "Entering in checkParameter #parameters=" + str(len(args)), "CORE")
   if (len(args) == 1):
      Functions.log(
          "DEAD", "At least provide one parameter : Configuration file for daemon", "CORE")
      return 0
   return 1


def main():
   condToSBU=0
   SBUset=0
   onlySolar=True
   Functions.log("INF", "Starting powerManager", "CORE")
   if checkParameter(sys.argv) == 0:
      exit(0)
   powerManagerConfig = powerManagerConfiguration(sys.argv[1:][0])
   if not powerManagerConfig.loadConfiguration():
      Functions.log("DEAD", "Unable to load power manager configuration", "CORE")
      exit(1)
   if not powerManagerConfig.checkConfiguration():
      Functions.log("DEAD", "Insuffisant power manager configuration to continue", "CORE")
      exit(1)
   Functions.log("INF", "Instantiation of new gridPowerObjet", "CORE")
   myGridPower=gridPower(powerManagerConfig.getGpioPort4Grid())
   myGridPower.setGridOn()
   influxDbProps=dict()
   influxDbProps['host']=powerManagerConfig.getInfluxDbUrl() 
   influxDbProps['port']=powerManagerConfig.getInfluxDbPort()
   influxDbProps['database']=powerManagerConfig.getInfluxDbName()
   myDb=myInfluxDb(influxDbProps)
   nbErrors=0
   nbResErrors=0
   GridPower=0  

   dateSBU=powerManagerConfig.getSBUEvening()
   while True:

      current_dateTime = datetime.now()
      if current_dateTime.hour>=dateSBU:
         if not SBUset and condToSBU:
            os.system('/users/powerManager/bin/setSBUmode.sh')
            Functions.log("INF","Setting inverter to SBU","CORE")
            SBUset=1      
      # bat Capa
      resDict=myDb.queryBatCapa()
      if resDict['errors']==None:
         Functions.log("INF", "requests for batteries capacity runs correctly","CORE")
      else:
         Functions.log("ERR", "requests for batteries capacity returned on error","CORE")
         sleep(60)
         continue 
      resArray=resDict['answer']
      if len(resArray):
         for res in resArray:
            if 'last' in res:
               cap=res['last']
               if float(cap)<batReturnToSUB:
                  Functions.log("WNG","Capacity of pylontech  ("+str(cap)+") reached "+str(batReturnToSUB)+ "% .Returning to SUB mode","CORE")
                  os.system('/users/powerManager/bin/setSUBmode.sh')
                  SBUset=0
                  condToSBU=0
           
               if float(cap)<minBatCapacity:
                  Functions.log("WNG","Capacity of pylontech  ("+str(cap)+") reached "+str(minBatCapacity)+ "% ","CORE")
                  os.system('/users/powerManager/bin/setSUBmode.sh')
                  SBUset=0
                  condToSBU=0
               if float(cap)>allowSBUBatCapacity:
                  Functions.log("WNG","Capacity of pylontech  ("+str(cap)+") reached "+str(minBatCapacity)+ "% . Allowing to go to SBU","CORE")
                  condToSBU=1 

               Functions.log("INF", "Capacity of pylontech is now "+str(cap)+"%","CORE") 
      time.sleep(60)

if __name__ == "__main__":
    main()
