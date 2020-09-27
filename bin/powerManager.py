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
from utils.myInfluxDb import myInfluxDb
daemonUptime = time.time()

minBatCapacity=25.0
maxBatCurrent=-25.0

def checkParameter(args):
   Functions.log(
      "INF", "Entering in checkParameter #parameters=" + str(len(args)), "CORE")
   if (len(args) == 1):
      Functions.log(
          "DEAD", "At least provide one parameter : Configuration file for daemon", "CORE")
      return 0
   return 1


def main():
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
   influxDbProps=dict()
   influxDbProps['host']=powerManagerConfig.getInfluxDbUrl() 
   influxDbProps['port']=powerManagerConfig.getInfluxDbPort()
   influxDbProps['database']=powerManagerConfig.getInfluxDbName()
   myDb=myInfluxDb(influxDbProps)
   nbErrors=0
   nbResErrors=0
   GridPower=0  
   while True:
      # bat Capa
      resDict=myDb.queryBatCapacity(1)
      resDict2=myDb.queryBatCapacity(2)
      if resDict['errors']==None and resDict2['errors']==None:
         #Functions.log("INF", "The 2 requests for batteries capacity runned successfully","CORE")
         nbErrors=0
      else:
         Functions.log("ERR", "requests for batteries capacity retruned on error","CORE")
         nbErrors+=1
  
      if nbErrors>2:
         Functions.log("ERR","Too much errors requesting batteries capacity. Restoring grid power","CORE")
         myGridPower.setGridOn()
         GridPower=1
      resArray=resDict['answer']
      resArray2=resDict2['answer'] 
      if len(resArray) and len(resArray2):
         for res in resArray:
            if 'last' in res:
               cap=res['last']
               if float(cap)<minBatCapacity:
                  if not GridPower:
                     Functions.log("WNG","Capacity of pylontech 1 ("+str(cap)+") reached "+str(minBatCapacity)+ "% .Restoring grid power","CORE")
                     myGridPower.setGridOn()
                     GridPower=1
                  else:
                     Functions.log("INF","Capacity of pylontech 1 is "+str(cap)+"%. Grid power is on","CORE")
               else:
                  Functions.log("INF","Capacity of pylontech 1 ("+str(cap)+") over "+str(minBatCapacity)+ "%","CORE")
         for res in resArray2:
            if 'last' in res:
               cap=res['last']
               if float(cap)<minBatCapacity:
                  if not GridPower:
                     Functions.log("WNG","Capacity of pylontech 2 ("+str(cap)+") reached "+str(minBatCapacity)+ "% .Restoring grid power","CORE")
                     myGridPower.setGridOn()
                     GridPower=1
                  else:
                     Functions.log("INF","Capacity of pylontech 2 is "+str(cap)+" %. Grid power is on","CORE")
               else:
                  Functions.log("INF","Capacity of pylontech 2 ("+str(cap)+") over "+str(minBatCapacity)+ "%","CORE")
         nbResErrors=0
      else:
         nbResErrors+=1

      if nbResErrors>2:
         Functions.log("ERR","No results found requesting batteries capacity. Restoring grid power","CORE")
         myGridPower.setGridOn()
         GridPower=1

      # bat Current

      resDict=myDb.queryBatCurrent(1)
      resDict2=myDb.queryBatCurrent(2)
      if resDict['errors']==None and resDict2['errors']==None:
         #Functions.log("INF", "The 2 requests for batteries current runned successfully","CORE")
         nbErrors=0
      else:
         Functions.log("ERR", "requests for batteries current retruned on error","CORE")
         nbErrors+=1

      if nbErrors>2:
         Functions.log("ERR","Too much errors requesting batteries current. Restoring grid power","CORE")
         myGridPower.setGridOn()
         GridPower=1
      resArray=resDict['answer']
      resArray2=resDict2['answer']
      if len(resArray) and len(resArray2):
         for res in resArray:
            if 'last' in res:
               cap=res['last']
               if float(cap)<maxBatCurrent:
                  if not GridPower:
                     Functions.log("WNG","Current of pylontech 1 ("+str(cap)+"A) reached "+str(abs(maxBatCurrent))+"A discharge current. Restoring grid power to On","CORE")
                     myGridPower.setGridOn()
                     GridPower=1
                  else:
                     Functions.log("ERR","Current of pylontech 1 is "+str(cap)+"A","CORE")
               else:
                  Functions.log("INF","Current of pylontech 1 ("+str(cap)+"A) under "+str(abs(maxBatCurrent))+"A discharge current","CORE")
         for res in resArray2:
            if 'last' in res:
               cap=res['last']
               if float(cap)<maxBatCurrent:
                  if not GridPower:
                     Functions.log("WNG","Current of pylontech 2 ("+str(cap)+"A) reached "+str(abs(maxBatCurrent))+"A discharge current. Restoring grid power to On","CORE")
                     myGridPower.setGridOn()
                     GridPower=1
                  else:
                     Functions.log("ERR","Current of pylontech 2 is "+str(cap)+"A","CORE")
               else:
                  Functions.log("INF","Current of pylontech 2 ("+str(cap)+"A) under "+str(abs(maxBatCurrent))+"A discharge current","CORE")
         nbResErrors=0
      else:
         nbResErrors+=1

      if nbResErrors>2:
         Functions.log("ERR","No results found requesting batteries capacity. Restoring grid power to On","CORE")
         myGridPower.setGridOn()  
         GridPower=1
      time.sleep(10)
if __name__ == "__main__":
    main()
