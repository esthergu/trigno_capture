import time
from pytrignos import TrignoAdapter
import pandas as pd
import matplotlib.pyplot as plt
import csv


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


trigno_sensors = TrignoAdapter()
### trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,4), sensors_labels=('EMG1','EMG4'))
trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2), sensors_labels=('EMG1','EMG2'))
##trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('EMG1','EMG2','EMG3','EMG4','EMG5','EMG6','EMG7','EMG8','EMG9','EMG10'))
trigno_sensors.start_acquisition()



ax=pd.Series()

time_period = 1/74.074 #0.1 #s
while(True):
    time.sleep(time_period)
    sensors_reading = trigno_sensors.sensors_reading()
    #print(sensors_reading)
    #print(sensors_reading[['EMG']])
    #print(sensors_reading.EMG)
    #### print(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG)
    #### print(pd.Series.mean(sensors_reading.EMG.abs()))
    #gfg=pd.Series(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG)
    #gfg.plot()
    #plt.show()
    #plt.cla()
    print(pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG1'].EMG.abs())*10000.0)
    #### print(sensors_reading.EMG.size)
    #### f = open('/home/ertugimperial/Desktop/csv_file', 'w')
    #### writer = csv.writer(f)
    #### ax = ax.append(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG)
    #### print(ax)
    #### writer.writerow(ax)
    

#### f.close()


trigno_sensors.stop_acquisition()
