import sys
import h5py
import numpy as np
import pandas as pd
import os.path as op
from scipy.integrate import simps
import matplotlib.pylab as plt
from utilities import visang, files

try:
    subject_path = str(sys.argv[1])
except:
    subject_path = "/home/mszul/BrainDyn Dropbox/Maciek Szul/explicit_implicit_beta/data/sub-101/ses-01/behaviour"

try:
    output_path = str(sys.argv[2])
except:
    output_path = "/home/mszul/git/DANC_learning_beh/data"

print("BEH DATA DIR:", subject_path)
print("OUTPUT DATA DIR:", output_path)

def cart2pol(x, y):
    radius = np.sqrt(x**2 + y**2)
    angle = np.arctan2(y, x)
    return [radius, angle]

raw_file_paths = files.get_files(subject_path, "block", ".mat")[2]
raw_file_paths.sort()

# raw_file_path = raw_file_paths[0] # iteration
data = []
for raw_file_path in raw_file_paths:
    print(raw_file_path)
    raw_data = h5py.File(raw_file_path, "r")

    subject_id = int(raw_data["run_params"]["subj_id"][0])
    trial_n = int(np.array(raw_data["run_params"]["n_trials"]))

    time_ix = np.array(raw_data["run_data"]["trial_time_idx"]).flatten().astype(int)
    w_px, h_px = np.array(raw_data["display"]["resolution"]).flatten().astype(int)
    w_cm = np.array(raw_data["display"]["width"]).flatten().astype(int)[0]
    h_cm = np.array(raw_data["display"]["height"]).flatten().astype(int)[0]
    d_cm = np.array(raw_data["display"]["dist"]).flatten().astype(int)[0]
    va = visang.VisualAngle(w_px, h_px, w_cm, h_cm, d_cm)

    targets = np.array(raw_data["targets"]["positions"]).transpose()

    aim_angle = []
    reach_angle = []
    auc_from_target = []
    auc_from_min = []

    for tr_ix in range(trial_n):
        trial_target = np.array(raw_data["run_data"]["trial_target"]).flatten().astype(int)[tr_ix] - 1
        x = np.array(raw_data["run_data"]["trajectory"])[0,:,tr_ix][:time_ix[tr_ix]]
        y = -np.array(raw_data["run_data"]["trajectory"])[1,:,tr_ix][:time_ix[tr_ix]]
        t = np.array(raw_data["run_data"]["trajectory"])[2,:,tr_ix][:time_ix[tr_ix]]
        target_radius = targets[:,1][trial_target]*va.degPix()
        target_angle = np.abs(targets[:,0][trial_target])
        xy = zip(x, y)
        try:
            radius, angle = zip(*[cart2pol(p[0], p[1]) for p in xy])
            dev_from_t = np.rad2deg(np.abs(angle) - target_angle)
            targ_cross = np.min(np.where(radius > target_radius))
            fiddypx_cross = np.min(np.where(radius > np.array(50)))
            t_aim_angle = dev_from_t[fiddypx_cross]
            t_reach_angle = dev_from_t[targ_cross]
            t_auc_from_target = simps(np.abs(dev_from_t[fiddypx_cross:targ_cross+1]))
            min_dev = np.min(np.abs(dev_from_t[fiddypx_cross:targ_cross+1]))
            t_auc_from_min = simps(np.abs(dev_from_t[fiddypx_cross:targ_cross+1]) - min_dev)
        except:
            radius = np.nan
            angle = np.nan
            dev_from_t = np.nan
            targ_cross = np.nan
            fiddypx_cross = np.nan
            t_aim_angle = np.nan
            t_reach_angle = np.nan
            t_auc_from_target = np.nan
            t_auc_from_min = np.nan
        # print(t_aim_angle, t_reach_angle, t_auc_from_target, t_auc_from_min)
        aim_angle.append(t_aim_angle)
        reach_angle.append(t_reach_angle)
        auc_from_target.append(t_auc_from_target)
        auc_from_min.append(t_auc_from_min)

    data_h5 = {
        "subject_id": np.full(trial_n, subject_id),
        "group": np.full(trial_n, np.array(raw_data["run_params"]["group"]).flatten()[0], dtype=int),
        "block": np.full(trial_n, np.array(raw_data["run_params"]["block"]).flatten()[0], dtype=int),
        "trial_in_block": np.arange(trial_n),
        "trial_coherence": np.array(raw_data["run_data"]["trial_coherence"]).flatten(),
        "trial_perturb": np.array(raw_data["run_data"]["trial_perturb"]).flatten(),
        "trial_type": np.full(trial_n, np.array(raw_data["run_params"]["trial_type"]).flatten()[0], dtype=int),
        "reach_dur": np.array(raw_data["run_data"]["reach_dur"]).flatten(),
        "reach_rt": np.array(raw_data["run_data"]["reach_rt"]).flatten(),
        "trial_directions": np.array(raw_data["run_data"]["trial_directions"]).flatten().astype(int),
        "trial_target": trial_target,
        "aim_target": np.array(aim_angle),
        "reach_target": np.array(reach_angle),
        "auc_from_target": np.array(auc_from_target),
        "auc_from_min": np.array(auc_from_min)
    }

    data_h5 = pd.DataFrame.from_dict(data_h5)
    data.append(data_h5)

data = pd.concat(data, ignore_index=True)
coherences = data.trial_coherence.unique()
categories = ["zero", "low", "med", "high"]
coh_cat = {i[0]: i[1] for i in zip(coherences, categories)}

def cat_func(row, dictionary):
    return dictionary[row]

data["coh_cat"] = data.trial_coherence.apply(lambda x: cat_func(x, coh_cat))

data.to_csv(op.join(output_path, "subj-{}.csv".format(subject_id)), index=False)