import os
import re
import subprocess
import time
import json
import socket
import select

from utils.functions import Functions
try:
   import RPi.GPIO as GPIO
except RuntimeError as err:
   Functions.log("ERR","Error importing RPi.GPIO","gridPower")
   Functions.log("ERR",err,"gridPower")


class gridPower:
   name = "gridPower"

   def __init__(self,pinNum=36):
      Functions.log("INF","Creating a new grid Power instance ","gridPower")
      self.gridPowerWanted=True
      self.gridPowerStatus="unknown"
      self.pinNumberForGridControl=pinNum 
      self.errorStatus=0
      Functions.log("INF","Configuration for GPIO port on pin"+str(self.pinNumberForGridControl),"gridPower")
      GPIO.setmode(GPIO.BOARD)
      GPIO.setwarnings(False)
      try:
         GPIO.setup(self.pinNumberForGridControl,GPIO.OUT)
      except RuntimeError as err:
         Functions.log("ERR","Unable to open Gpio Port","gridPower")
         Functions.log("ERR",err,"gridPower")
         self.errorStatus=1
         return
      except Warning as warn:
         Functions.log("WNG",warn,"gridPower")


   def setGridOff(self):
      if not self.errorStatus:
         try:
            GPIO.output(self.pinNumberForGridControl,0)
         except Exception as err:
            Functions.log("ERR","Error importing changing powerGrid to off","gridPower")
            Functions.log("ERR",err,"gridPower")
            GPIO.cleanup()
         self.gridPowerWanted=False
      else:
         Functions.log("ERR","Unable to set gridPower to off because of errorStatus into instance","gridPower")
      
   def setGridOn(self):
      if not self.errorStatus:
         try:
            GPIO.output(self.pinNumberForGridControl,1)
         except Exception as err:
            Functions.log("ERR","Error importing changing powerGrid to on","gridPower")
            Functions.log("ERR",err,"gridPower")
            GPIO.cleanup()
         self.gridPowerWanted=True
      else:
         Functions.log("ERR","Unable to set gridPower to off because of errorStatus into instance","gridPower")

   def getPowerWanted():
      return self.gridPowerWanted

       
