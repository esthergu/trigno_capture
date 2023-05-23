#!/usr/bin/env python3
import rospy
from pytrignos.pytrignos import TrignoAdapter
import pandas as pd
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

emg_data = pd.Series()
ori_data = pd.Series()
my_msg = Float64MultiArray()  
#my_msg = Float64()  



class TrignoCapture_ORI:
    def __init__(self):
        self.trigno_sensors = TrignoAdapter()
        #self.trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2), sensors_labels=('EMG1','EMG2'))
        #self.trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('EMG1','EMG2','EMG3','EMG4','EMG5','EMG6','EMG7','EMG8','EMG9','EMG10'))
        self.trigno_sensors.add_sensors(sensors_mode='ORIENTATION', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('ORIENTATION1','ORIENTATION2','ORIENTATION3','ORIENTATION4','ORIENTATION5','ORIENTATION6','ORIENTATION7','ORIENTATION8','ORIENTATION9','ORIENTATION10'))
    def start(self):
        self.trigno_sensors.start_acquisition()
    def stop(self):
        self.trigno_sensors.stop_acquisition()
    def read(self):
        #self.trigno_sensors.sensors_reading()
        #print('reading it')
        sensors_reading = self.trigno_sensors.sensors_reading()
        global ori_data
        ######## emg_data = sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG
        #emg_data = sensors_reading.EMG
        ori_data = pd.concat([sensors_reading.qw, sensors_reading.qx,sensors_reading.qy, sensors_reading.qz])
        ####emg_data = pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())
        #print(pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())*10000.0)
        #print(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG)
        #print(sensors_reading[sensors_reading.Sensor_id == 'ORIENTATION1'].qw)
        print(ori_data)

class TrignoCapture:
    def __init__(self):
        self.trigno_sensors = TrignoAdapter()
        #self.trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2), sensors_labels=('EMG1','EMG2'))
        self.trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('EMG1','EMG2','EMG3','EMG4','EMG5','EMG6','EMG7','EMG8','EMG9','EMG10'))
        #self.trigno_sensors.add_sensors(sensors_mode='ORIENTATION', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('ORIENTATION1','ORIENTATION2','ORIENTATION3','ORIENTATION4','ORIENTATION5','ORIENTATION6','ORIENTATION7','ORIENTATION8','ORIENTATION9','ORIENTATION10'))
    def start(self):
        self.trigno_sensors.start_acquisition()
    def stop(self):
        self.trigno_sensors.stop_acquisition()
    def read(self):
        #self.trigno_sensors.sensors_reading()
        #print('reading it')
        sensors_reading = self.trigno_sensors.sensors_reading()
        global emg_data
        ######## emg_data = sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG
        emg_data = sensors_reading.EMG
        #ori_data = sensors_reading.qw
        ####emg_data = pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())
        #print(pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())*10000.0)
        #print(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG)
        #print(sensors_reading[sensors_reading.Sensor_id == 'ORIENTATION1'].qw)

def trigno_ros():
    global emg_data,ori_data
    rospy.init_node("trigno_capture")
    pub = rospy.Publisher('emg_data', Float64MultiArray, queue_size=10)
    rate = rospy.Rate(74.074) # 10hz
    #rate = rospy.Rate(1) # 10hz
    trigno_capture = TrignoCapture()
    trigno_capture_ORI = TrignoCapture_ORI()
    #trigno_capture_ORI.start()
    trigno_capture.start()
    #trigno_capture.read()
    rospy.on_shutdown(trigno_capture.stop)
    rospy.loginfo("Sensor node is ready.")
    while not rospy.is_shutdown():
        trigno_capture.read()
        trigno_capture_ORI.read()
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        ### print(emg_data.array)
        #print(emg_data)
        my_msg.data = emg_data.array
        #my_msg.data = emg_data
        pub.publish(my_msg)
        rate.sleep()
    #rospy.spin()



if __name__ == "__main__":
    try:
        trigno_ros()
    except rospy.ROSInterruptException:
        pass

