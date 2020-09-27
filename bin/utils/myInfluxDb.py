from influxdb import InfluxDBClient
from utils.functions import Functions
import time 
class myInfluxDb:
   name="myInfluxDb"

   def __init__(self,conDict):
      Functions.log("INF","Creating a new influxDb connector onbjet instance","myInfluxdb")
      self.host=conDict['host']
      self.port=conDict['port']
      self.database=conDict['database']
      Functions.log("INF","Opening connection to influx with host="+str(conDict['host'])+",port="+str(conDict['port'])+",database="+conDict['database'],"myInfluxDb") 
      self.clientConn=InfluxDBClient(host=conDict['host'],port=conDict['port'],database=conDict['database'])

   def queryBatCapacity(self,numBat):
      time.sleep(2)
      result=self.clientConn.query("select last(Coulomb"+str(numBat)+") from pylontech_pwr where time>now()-3m")
      #Functions.log("INF","Running influxdb request : select last(Coulomb"+str(numBat)+") from pylontech_pwr where time>now()-3m","myInfluxdb")
      resDict=dict() 
      resDict['errors']=result.error
      arrayRes=[]
      for i in result.get_points():
         arrayRes.append(i) 
      #Functions.log("INF","Request returned "+str(arrayRes),"myInfluxdb")
      resDict['answer']=arrayRes
      return resDict

   def queryBatCurrent(self,numBat):
      time.sleep(2)
      result=self.clientConn.query("select last(Current"+str(numBat)+") from pylontech_pwr where time>now()-3m")
      #Functions.log("INF","Running influxdb request : select last(Current"+str(numBat)+") from pylontech_pwr where time>now()-3m","myInfluxdb")
      resDict=dict()
      resDict['errors']=result.error
      arrayRes=[]
      for i in result.get_points():
         arrayRes.append(i)
      #Functions.log("INF","Request returned "+str(arrayRes),"myInfluxdb")
      resDict['answer']=arrayRes
      return resDict

