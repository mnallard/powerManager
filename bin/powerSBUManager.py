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
from utils.myInfluxDb import myInfluxDb
daemonUptime = time.time()

batReturnToSUB=25.0

def checkParameter(args):
   Functions.log(
      "INF", "Entering in checkParameter #parameters=" + str(len(args)), "CORE")
   if (len(args) == 1):
      Functions.log(
          "DEAD", "At least provide one parameter : Configuration file for daemon", "CORE")
      return 0
   return 1

def main():
   Functions.log("INF", "Starting powerSBUManager", "CORE")
   if checkParameter(sys.argv) == 0:
      exit(0)
   powerManagerConfig = powerManagerConfiguration(sys.argv[1:][0])
   if not powerManagerConfig.loadConfiguration():
      Functions.log("DEAD", "Unable to load power manager configuration", "CORE")
      exit(1)
   if not powerManagerConfig.checkConfiguration():
      Functions.log("DEAD", "Insuffisant power manager configuration to continue", "CORE")
      exit(1)
   influxDbProps=dict()
   influxDbProps['host']=powerManagerConfig.getInfluxDbUrl() 
   influxDbProps['port']=powerManagerConfig.getInfluxDbPort()
   influxDbProps['database']=powerManagerConfig.getInfluxDbName()
   myDb=myInfluxDb(influxDbProps)
   while True:
      # bat Capa
      resDict=myDb.queryBatCapacity(1)
      resDict2=myDb.queryBatCapacity(2)
      if resDict['errors']==None and resDict2['errors']==None:
         nbErrors=0
      else:
         Functions.log("ERR", "Requests for batteries capacity returned on error.","CORE")
         nbErrors+=1
  
      if nbErrors>2:
         Functions.log("ERR","Too much errors requesting batteries capacity.","CORE")
         break 
      resArray=resDict['answer']
      resArray2=resDict2['answer'] 
      if len(resArray) and len(resArray2):
         for res in resArray:
            if 'last' in res:
               cap=res['last']
               if float(cap)<batReturnToSUB:
                  Functions.log("WNG","Capacity of pylontech 1 ("+str(cap)+") reached "+str(batReturnToSUB)+ "%.Returning to SUB mode","CORE")
                  os.system('/users/powerManager/bin/setSUBmode.sh')
               else:
                  Functions.log("INF","Capacity of pylontech 1 ("+str(cap)+") over "+str(minBatCapacity)+ "%","CORE")
               
         for res in resArray2:
            if 'last' in res:
               cap=res['last']
               if float(cap)<batReturnToSUB:
                  Functions.log("WNG","Capacity of pylontech 1 ("+str(cap)+") reached "+str(batReturnToSUB)+ "% .Returning to SUB mode","CORE")
                  os.system('/users/powerManager/bin/setSUBmode.sh')               
               else:
                  Functions.log("INF","Capacity of pylontech 2 ("+str(cap)+") over "+str(minBatCapacity)+ "%","CORE")

      time.sleep(10)
if __name__ == "__main__":
    main()
