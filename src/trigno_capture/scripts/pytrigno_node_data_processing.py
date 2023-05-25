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
import pyemgpipeline as pep
from matplotlib.figure import SubplotParams


parser = argparse.ArgumentParser(description='DataCollection')

parser.add_argument("--part", type=str, default="arm1", help="Current Body Part")
# parser.add_argument("--num", type=int, default=0, help="Current line")
# parser.add_argument("--rot-sensitivity", type=float, default=1.0, help="How much to scale rotation user inputs")
args = parser.parse_args()

DATASET_PATH = "/home/esther/hdd/data_trigno/"



def rms(y):
    return np.sqrt(np.mean(np.array(y)**2))

def medfilt(y):
    med_y = sp.medfilt(y.T, kernel_size=15)
    return med_y.T

emgs = []

# for ep_directory in sorted(os.listdir(DATASET_PATH)):
# ep_directory = "{}_{}/".format(args.part, args.num)
for ep_directory in sorted(os.listdir(DATASET_PATH)):
    obs_path = os.path.join(DATASET_PATH, ep_directory, "emg_obs.npy")

    if args.part not in obs_path:
        continue

    # print(obs_path) 

    data = np.load(glob.glob(obs_path)[0], allow_pickle=True, encoding='latin1')

    trial_dir = []
    # trial_dir = dict(
    #     emg1=[],
    #     emg2=[],
    #     emg3=[],
    #     emg4=[]
    # )
    for seq in range(len(data)):
        # 108 = 4*27
        data_seq = data[seq]
        # print("one seq: ", seq)
        if len(data_seq) == 108:
            # trial_dir['emg1'].append(np.mean(data_seq[:27]))
            # trial_dir['emg2'].append(np.mean(data_seq[27:53]))
            # trial_dir['emg3'].append(np.mean(data_seq[54:80]))
            # trial_dir['emg4'].append(np.mean(data_seq[81:]))
            emg1_data = rms(data_seq[:27])
            emg2_data = rms(data_seq[27:53])
            emg3_data = rms(data_seq[54:80])
            emg4_data = rms(data_seq[81:])

            trial_dir.append([emg1_data, emg2_data, emg3_data, emg4_data])
            # if np.any(np.isnan([np.mean(data_seq[:27]), np.mean(data_seq[27:53]), np.mean(data_seq[54:80]), np.mean(data_seq[81:])]))==True:
            #     print(data_seq)
            #     print("nan!!!")
        # else:
        #     # print("one seq len: ", len(data_seq))
            
    trial_dir = np.array(trial_dir)
    medfilt(trial_dir)
    emgs.append(trial_dir)


# trial_names = []
trial_names = [args.part+"_1", args.part+"_2", args.part+"_3", args.part+"_4", args.part+"_5"]
channel_names = ["0", "1", "2", "3"]
sample_rate = 1000
emg_plot_params = pep.plots.EMGPlotParams(
    n_rows=1,
    n_cols=4,
    fig_kwargs={
        'figsize': (16, 1.5),
        'subplotpars': SubplotParams(top=0.7, bottom=0.2, wspace=0.1, hspace=0),
    },
    line2d_kwargs={
        'color': 'b',
    }
)



# print(emgs)
c = pep.wrappers.EMGMeasurementCollection(emgs, hz=sample_rate, trial_names=trial_names, 
                                               channel_names=channel_names, emg_plot_params=emg_plot_params)
c.plot()
# c.save(directory+"_1/"+"raw" +".png")

c.apply_dc_offset_remover()
c.plot()
# c.save(directory+"_1/"+"apply_dc_offset_remover" +".png")

c.apply_bandpass_filter()
c.plot()
# c.save(directory+"_1/"+"apply_bandpass_filter" +".png")

c.apply_full_wave_rectifier()
c.plot()
# c.save(directory+"_1/"+"apply_full_wave_rectifier" +".png")

c.apply_linear_envelope(le_order=4, le_cutoff_fq=6)
c.plot()
# c.save(directory+"_1/"+"apply_linear_envelope" +".png")

c.apply_end_frame_cutter(n_end_frames=30)
c.plot()
# c.save(directory+"_1/"+"apply_end_frame_cutter" +".png")

max_amplitude = c.find_max_amplitude_of_each_channel_across_trials()
print('max_amplitude:', max_amplitude)
c.apply_amplitude_normalizer(max_amplitude)
c.plot()
# c.save(directory+"_1/"+"apply_amplitude_normalizer" +".png")

all_beg_ts = [2.9, 5.6, 0]
all_end_ts = [12, 14.5, 999]
c.apply_segmenter(all_beg_ts, all_end_ts)
c.plot()
# c.save(directory+"_1/"+"apply_segmenter" +".png")
