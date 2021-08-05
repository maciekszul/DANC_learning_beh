import math
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import gridspec
import matplotlib.pylab as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from utilities import files

data_files = files.get_files("data", "", "")[0]
data_files.sort()

all_pps = pd.concat([pd.read_csv(i) for i in data_files], ignore_index=True)
all_pps["perturb_cat"] = all_pps.trial_perturb.apply(lambda x: int(np.round(np.rad2deg(x), 0)))
all_pps = all_pps.dropna()
all_pps.to_csv("imgs/data_output.csv", index=False)

explicit = all_pps.loc[all_pps.group == 1]
explicit.to_csv("imgs/data_output_exp.csv", index=False)
implicit = all_pps.loc[all_pps.group == 0]
implicit.to_csv("imgs/data_output_imp.csv", index=False)

