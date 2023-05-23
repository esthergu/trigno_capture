import numpy as np
import glob
from PIL import Image
import os
import scipy.misc
import matplotlib.pyplot as plt
import argparse
import shutil  
import cv2   
from scipy import signal as sp     
# import pyemgpipeline as pep
from matplotlib.figure import SubplotParams


parser = argparse.ArgumentParser(description='DataCollection')

parser.add_argument("--part", type=str, default="arm1", help="Current Body Part")
parser.add_argument("--num", type=int, default=0, help="Current line")
# parser.add_argument("--rot-sensitivity", type=float, default=1.0, help="How much to scale rotation user inputs")
args = parser.parse_args()

DATASET_PATH = "/home/esther/hdd/data_trigno/"

# emgs = []
# # trial_names = []
# trial_names = ["arm", "leg", "face"]
# channel_names = ["0", "1", "2", "3", "4", "5", "6", "7"]
# sample_rate = 1000
# emg_plot_params = pep.plots.EMGPlotParams(
#     n_rows=1,
#     n_cols=8,
#     fig_kwargs={
#         'figsize': (16, 1.5),
#         'subplotpars': SubplotParams(top=0.7, bottom=0.2, wspace=0.1, hspace=0),
#     },
#     line2d_kwargs={
#         'color': 'b',
#     }
# )


for ep_directory in sorted(os.listdir(DATASET_PATH)):
    obs_path = os.path.join(DATASET_PATH, ep_directory, "emg_obs.npy")
    print(obs_path)

    data = np.load(glob.glob(obs_path)[0], allow_pickle=True, encoding='latin1')

    print(len(data))

    print(len(data[0]))

    trial_arr = []
    for i in data:
        data_arr = []
        for j in i:
            # emgs[j[0]].append(j[1])
            data_arr.append(j[1])
        trial_arr.append(data_arr)
    emgs.append(np.array(trial_arr))
    print(emgs)
    # trial_names.append(ep_directory)

# c = pep.wrappers.EMGMeasurementCollection(emgs, hz=sample_rate, trial_names=trial_names, 
                                                # channel_names=channel_names, emg_plot_params=emg_plot_params)

# c.apply_full_wave_rectifier()
# c.plot()

