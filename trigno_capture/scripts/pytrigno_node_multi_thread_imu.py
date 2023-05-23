#!/usr/bin/env python3
import rospy
from pytrignos.pytrignos import TrignoAdapter
import pandas as pd
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
import threading
import multiprocessing
from sensor_msgs.msg import Joy

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

emg_data = pd.Series()
ori_data = pd.Series()
my_msg = Float64MultiArray()  
my_msg_ori = Joy()  
#my_msg_ori = Float64MultiArray()  
#my_msg = Float64()  




class TrignoCapture_ORI:
    def __init__(self):
        self.trigno_sensors = TrignoAdapter()
        #self.trigno_sensors.add_sensors(sensors_mode='ORIENTATION', sensors_numbers=(1,2), sensors_labels=('ORIENTATION1','ORIENTATTION2'))
        #self.trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('EMG1','EMG2','EMG3','EMG4','EMG5','EMG6','EMG7','EMG8','EMG9','EMG10'))
        #self.trigno_sensors.add_sensors(sensors_mode='ORIENTATION', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('ORIENTATION1','ORIENTATION2','ORIENTATION3','ORIENTATION4','ORIENTATION5','ORIENTATION6','ORIENTATION7','ORIENTATION8','ORIENTATION9','ORIENTATION10'))
        self.trigno_sensors.add_sensors(sensors_mode='ORIENTATION', sensors_numbers=(1,2,3,4,5,6), sensors_labels=('ORIENTATION1','ORIENTATION2','ORIENTATION3','ORIENTATION4','ORIENTATION5','ORIENTATION6'))
        #self.start()
    def start(self):
        self.trigno_sensors.start_acquisition()
    def stop(self):
        self.trigno_sensors.stop_acquisition()
    def read(self):
        #self.trigno_sensors.sensors_reading()
        #print('reading it')
        global ori_data
        print("ori_data000:",ori_data)
        sensors_reading = self.trigno_sensors.sensors_reading()
        ######## emg_data = sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG
        #emg_data = sensors_reading.EMG
        ori_data = pd.concat([sensors_reading.qw, sensors_reading.qx,sensors_reading.qy, sensors_reading.qz])
        ####emg_data = pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())
        #print(pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())*10000.0)
        #print(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG)
        #print(sensors_reading[sensors_reading.Sensor_id == 'ORIENTATION1'].qw)
        #print(sensors_reading.qw)
        print("ori_data:",ori_data)

class TrignoCapture:
    def __init__(self):
        self.trigno_sensors = TrignoAdapter()
        #self.trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2), sensors_labels=('EMG1','EMG2'))
        self.trigno_sensors.add_sensors(sensors_mode='EMG', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('EMG1','EMG2','EMG3','EMG4','EMG5','EMG6','EMG7','EMG8','EMG9','EMG10'))
        self.start()
        #self.trigno_sensors.add_sensors(sensors_mode='ORIENTATION', sensors_numbers=(1,2,3,4,5,6,7,8,9,10), sensors_labels=('ORIENTATION1','ORIENTATION2','ORIENTATION3','ORIENTATION4','ORIENTATION5','ORIENTATION6','ORIENTATION7','ORIENTATION8','ORIENTATION9','ORIENTATION10'))
    def start(self):
        self.trigno_sensors.start_acquisition()
    def stop(self):
        self.trigno_sensors.stop_acquisition()
    def read(self):
        #self.trigno_sensors.sensors_reading()
        #print('reading it')
        sensors_reading = self.trigno_sensors.sensors_reading()
        #global emg_data
        ####### emg_data = sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG
        emg_data = sensors_reading.EMG
        #ori_data = sensors_reading.qw
        ####emg_data = pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())
        #print(pd.Series.mean(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG.abs())*10000.0)
        #print(sensors_reading[sensors_reading.Sensor_id == 'EMG4'].EMG)
        #print(sensors_reading[sensors_reading.Sensor_id == 'ORIENTATION1'].qw)

def trigno_ros():
    global ori_data
    rospy.init_node("trigno_capture_imu")


   # pub = rospy.Publisher('emg_data', Float64MultiArray, queue_size=10)
    pub_ori = rospy.Publisher('imu_data', Joy, queue_size=1)
    rate = rospy.Rate(74.074) # 10hz
    #rate = rospy.Rate(1) # 10hz
  #  trigno_capture = TrignoCapture()
    trigno_capture_ORI = TrignoCapture_ORI()
    #t2 = threading.Thread(target=trigno_capture_ORI)
    #t2.start()
    #trigno_capture_ORI.start()
    # trigno_capture.start()
    #trigno_capture.read()
    rospy.on_shutdown(trigno_capture_ORI.stop)
    rospy.loginfo("Sensor node is ready.")
    while not rospy.is_shutdown():
        print("running main loop")
        print("Number of cpu : ", multiprocessing.cpu_count())
#        trigno_capture.read()
#        t1 = multiprocessing.Process(target=trigno_capture.read())
 #       t1.start()
        t2 = multiprocessing.Process(target=trigno_capture_ORI.read())
        #t2 = threading.Thread(target=trigno_capture_ORI.read())
        t2.start()
         #t2.join()
       # t1.run()
        #t1.start()
        #t1.join()
        #t1.stop()
        ###t1.run()
####        trigno_capture.read()
        ### trigno_capture_ORI.read()
###        t1.join()        
#hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        ### print(emg_data.array)
        #print(emg_data)
    #    my_msg.data = emg_data.array
        my_msg_ori.axes = ori_data.array
        my_msg_ori.header.stamp = rospy.Time.now()
        #ori_data = pd.Series()
        #my_msg.data = emg_data
     #   pub.publish(my_msg)
        pub_ori.publish(my_msg_ori)

        rate.sleep()
    #rospy.spin()



if __name__ == "__main__":
    try:
        trigno_ros()
    except rospy.ROSInterruptException:
        pass

