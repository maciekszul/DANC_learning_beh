import math
import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
from matplotlib import gridspec
from utilities import files

data_files = files.get_files("data", "", "")[0]
data_files.sort()

all_pps = pd.concat([pd.read_csv(i) for i in data_files], ignore_index=True)
condition_df = all_pps.groupby("subject_id", as_index=False).group.mean()
grid_row_n = math.ceil((condition_df.shape[0]/2))


col_pal = ["#5CE619", "#195CE6", "#E6195C"]
cond = all_pps.trial_perturb.unique()
cond.sort()
cond_pal = {i[0]: i[1] for i in list(zip(cond, col_pal))}


# gs = gridspec.GridSpec(grid_row_n, 2, wspace=0.3, hspace=0.3)
# figure = plt.figure(figsize=(8, 12))


# for column, g in enumerate(condition_df.group.unique()):
#     sub_df = condition_df.loc[condition_df.group==g]
#     for row, sub in enumerate(sub_df.subject_id.unique()):
#         ax = figure.add_subplot(gs[row, column], label=sub)
#         ax.set_title("Subject {}".format(sub))
#         data = all_pps.loc[all_pps.subject_id == sub]
#         data.reset_index(inplace=True)
#         for i in data.trial_perturb.unique():
#             y = data[data.trial_perturb == i]
#             x = y.index.to_numpy()
#             ax.scatter(x, y.reach_target, label=i, s=1)
#         ax.vlines(np.where(data.trial_in_block == 0)[0], ymin=-90, ymax=90, color="black", lw=0.75)
        
        
# # gs.tight_layout(figure, w_pad=2.0, h_pad=2.0)
# plt.suptitle("Reach Error split by perturbation direction")
# plt.show()



# gs = gridspec.GridSpec(grid_row_n, 2, wspace=0.2, hspace=0.2)
# figure = plt.figure(figsize=(8, 12))


# for column, g in enumerate(condition_df.group.unique()):
#     sub_df = condition_df.loc[condition_df.group==g]
#     for row, sub in enumerate(sub_df.subject_id.unique()):
#         ax = figure.add_subplot(gs[row, column], label=sub)
#         ax.set_title("Subject {}".format(sub))
#         data = all_pps.loc[all_pps.subject_id == sub]
#         data.reset_index(inplace=True)
#         for i in data.trial_perturb.unique():
#             y = data[data.trial_perturb == i]
#             x = y.index.to_numpy()
#             ax.scatter(x, y.reach_target, label=i, s=1, color=cond_pal[i], alpha=0.75)
#         ax.vlines(np.where(data.trial_in_block == 0)[0], ymin=-90, ymax=90, color="black", lw=0.75)
        
        
# gs.tight_layout(figure, w_pad=2.0, h_pad=2.0)
# # plt.suptitle("Reach Error split by perturbation direction")
# plt.show()


gs = gridspec.GridSpec(grid_row_n, 2, wspace=0.2, hspace=0.2)
figure = plt.figure(figsize=(8, 12))


for column, g in enumerate(condition_df.group.unique()):
    sub_df = condition_df.loc[condition_df.group==g]
    for row, sub in enumerate(sub_df.subject_id.unique()):
        ax = figure.add_subplot(gs[row, column], label=sub)
        ax.set_title("Subject {}".format(sub))
        data = all_pps.loc[all_pps.subject_id == sub]
        data.reset_index(inplace=True)
        
        for block in data.block.unique():
            for i in data.trial_perturb.unique():
                y = data[(data.trial_perturb == i) & (data.block == block)]
                x = y.index.to_numpy()
                ax.scatter(x, y.reach_target, label=i, s=1, color=cond_pal[i], alpha=0.75)
                mean = y.reach_target.median()
                min_ix = y.index.min()
                max_ix = y.index.max()
                ax.plot([min_ix, max_ix], [mean, mean], color=cond_pal[i], lw=1.5, ls="-")
        ax.vlines(np.where(data.trial_in_block == 0)[0], ymin=-90, ymax=90, color="black", lw=0.75)
        
        
gs.tight_layout(figure, w_pad=2.0, h_pad=2.0)
# plt.suptitle("Reach Error split by perturbation direction")
plt.show()
