#!/usr/bin/env python3
import rospy
from pytrignos.pytrignos import TrignoAdapter
import pandas as pd
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy
import shutil
from pynput.keyboard import Key, Listener
import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

emg_data = pd.Series()
ori_data = pd.Series()

import argparse
from time import sleep
import os



class EMGDataCollection():
    def __init__(self, args):
        # test()
        rospy.init_node('emg_demo')
        rospy.loginfo("Printing plot of EMG values...")

        self.num = args.num
        self.part = args.part

        self.directory = os.path.join("/home/esther/hdd/data_trigno/", "{}_{}/".format(self.part, self.num))

        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
        os.makedirs(self.directory)

        # self.freq = 0.1
        self.emg_obs = []

        self.emg_sub = rospy.Subscriber('/emg_data',
                               Joy,
                               self.emg_cb,
                               queue_size=1)

        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

        # self.data_collection()

    def on_press(self, key):
        print('{0} pressed'.format(
            key))
    

    def on_release(self, key):
        if key == Key.esc:
            print("start flushing")
            with open(self.directory+'emg_obs.npy', 'wb') as f:
                np.save(f, np.array(self.emg_obs))
            print("end flushing")
            return False


    def emg_cb(self, ea):
        # Clear screen
        # print("\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(len(ea.axes))
        self.emg_obs.append(ea.axes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DataCollection')
    parser.add_argument("--part", type=str, default="arm1", help="Current Body Part")
    parser.add_argument("--num", type=int, default=0, help="Current number")
    args = parser.parse_args()

    EMGDataCollection(args) 
    rospy.loginfo("Awaiting publications...")
    rospy.spin()
