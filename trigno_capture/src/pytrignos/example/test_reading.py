import time
from pytrignos import TrignoAdapter

trigno_sensors = TrignoAdapter()
trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,), sensors_labels=('EMG1',))
trigno_sensors.start_acquisition()

time_period = 1.0 #s
while(True):
    time.sleep(time_period)
    sensors_reading = trigno_sensors.sensors_reading()
    print(sensors_reading)
trigno_sensors.stop_acquisition()
