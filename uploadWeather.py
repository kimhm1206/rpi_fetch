from flask import request
from flask_restx import Resource, Api, Namespace
from function import *
import numpy as np
import math

Weather = Namespace('weatherstation')

@Weather.route('')
@Weather.doc(params={'PASSKEY': 'MAC address', 'dateutc' : 'format - yyyyMMddHHmmSS', 'tempinf':'temp f','humidityin' : 'humidity'})
class uploadWeather(Resource):
    def get(self):
        try:
            mac         = request.args.get('PASSKEY',"nomac")
            time        = request.args.get('dateutc',"notime")
            temp        = float(request.args.get('tempf',0))
            humi        = float(request.args.get('humidity',0))
            solar       = float(request.args.get('solarradiation',0))
            winddir       = float(request.args.get('winddir',0))
            windspeed       = float(request.args.get('windspeedmph',0))
            hourlyrainin       = float(request.args.get('hourlyrainin',0))
            dailyrainin       = float(request.args.get('dailyrainin',0))
            weeklyrainin       = float(request.args.get('weeklyrainin',0))
            monthlyrainin       = float(request.args.get('monthlyrainin',0))
            c_temp = (temp - 32) * 5/9
            es = 6.112 * np.exp(17.67 * c_temp / (c_temp + 243.5))
            e = es * (humi / 100)  
            dewpoint_f = (((-430.22 + 237.7 * np.log(e)) / (-1 * np.log(e) + 19.08))/(5/9))+32

            if math.isnan(dewpoint_f):
                dewpoint_f = 0.0
            
            try:
                dateutc    = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
                datekr     = dateutc+timedelta(hours=9)
            except:
                dateutc    = datetime.strptime(time,"%Y%m%d%H%M%S")
                datekr     = dateutc+timedelta(hours=9)
                
            rounded_utc = round_seconds(dateutc)
            rounded_kr = round_seconds(datekr)

            converdateutc = rounded_utc.strftime("%Y-%m-%d %H:%M:%S")
            converdatekr = rounded_kr.strftime("%Y-%m-%d %H:%M:%S")
            
            # query       = ('insert into weatherapitest values'+
            #         '(\''+mac+'\',\''+converdatekr+'\',\''+str(temp)+'\',\''+str(humi)+'\',\''+str(solar)+'\',\''+str(dewpoint_f)+'\')')
            # writeDataW(query)

            data = {"mac"      : mac,
                    "date"     : converdateutc,
                    "tempf"    : temp,
                    "humidity" : humi,
                    "windspeedmph" : windspeed,
                    "solarradiation" : solar,
                    "winddir"  : winddir,
                    "dailyrainin" : dailyrainin,
                    "hourlyrainin" : hourlyrainin,
                    "dewpoint"     : dewpoint_f,
                    "weeklyrainin" : weeklyrainin,
                    "monthlyrainin " : monthlyrainin}
            
            if is_internet_connected():
                saveserver(data)
                # savelocal(data)
            else:
                savelocal(data)
            
            return {'status' : 200, 'message' : 'upload'}

        except:
            return {'status' : 400, 'message' : 'upload error pleas check parameter'}
      