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
condition_df = all_pps.groupby("subject_id", as_index=False).group.mean()
grid_row_n = math.ceil((condition_df.shape[0]/2))


col_pal = ["#5CE619", "#195CE6", "#E6195C"]
markers_dir = ["v", "X", "^"]
perturb_dir = all_pps.trial_perturb.unique()
perturb_dir.sort()
dir_mark = {i[0]: i[1] for i in list(zip(perturb_dir, markers_dir))}
cond_pal = {i[0]: i[1] for i in list(zip(perturb_dir, col_pal))}

colours_coh = ["#89cff0", "#149414", "#FFCE03", "#F00505"]
levels_coh = ["zero", "low", "med", "high"]
coh_pal = {i[0]: i[1] for i in list(zip(levels_coh, colours_coh))}


marker_ledge = [
    Line2D(
        [0], [0], marker=dir_mark[i], 
        mec="black", mfc="white", lw=0.001,
        label=int(np.round(np.rad2deg(i), 0))
        ) for i in dir_mark.keys()
    ]
colour_ledge = [
    Patch(
        fc=coh_pal[i], ec=None, label=i
    ) for i in coh_pal.keys()
]

colour_ledge.extend(marker_ledge)

gs = gridspec.GridSpec(2, grid_row_n, wspace=0.25, hspace=0.4)
figure = plt.figure(figsize=(18, 5))

for row, g in enumerate(condition_df.group.unique()):
    sub_df = condition_df.loc[condition_df.group==g]
    for column, sub in enumerate(sub_df.subject_id.unique()):
        ax = figure.add_subplot(gs[row, column], label=sub)
        ax.set_title("Subject {}".format(sub))
        
        data = all_pps.loc[all_pps.subject_id == sub]
        data.reset_index(inplace=True)

        ax.axhline(0, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(-30, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(30, lw=0.25, alpha=0.5, linestyle="--", color="black")

        block_boundaries = np.where(data.trial_in_block == 0)[0]
        ax.vlines(
            block_boundaries, 
            ymin=-100, ymax=100, 
            color="black", lw=0.25, 
            alpha=0.5
        )
        for block in data.block.unique():
            for i in data.trial_perturb.unique():
                for c in data.coh_cat.unique():
                    coh_label = int(np.round(np.rad2deg(i), 0))
                    y = data[
                        (data.trial_perturb == i) & 
                        (data.block == block) & 
                        (data.coh_cat == c)
                    ]
                    x = y.index.to_numpy()
                    ax.scatter(
                        x, 
                        y.reach_target, 
                        s=6, color=coh_pal[c], 
                        alpha=0.99, 
                        marker=dir_mark[i], 
                        edgecolors="black", 
                        linewidth=0.25, 
                        # label=coh_label
                    )
        plt.ylim([-105, 105])
ax.legend(
    handles=colour_ledge, fontsize="xx-small", 
    loc=9, ncol=2, borderpad=0.1,
    title="coherence | direction",
    title_fontsize="xx-small"
)
plt.suptitle("Reach error (direction + coherence)")
plt.savefig("imgs/reach_error_split_by_dir_coh.png", bbox_inches="tight", dpi=300)
plt.close()

gs = gridspec.GridSpec(2, grid_row_n, wspace=0.25, hspace=0.4)
figure = plt.figure(figsize=(18, 5))

for row, g in enumerate(condition_df.group.unique()):
    sub_df = condition_df.loc[condition_df.group==g]
    for column, sub in enumerate(sub_df.subject_id.unique()):
        ax = figure.add_subplot(gs[row, column], label=sub)
        ax.set_title("Subject {}".format(sub))
        
        data = all_pps.loc[all_pps.subject_id == sub]
        data.reset_index(inplace=True)
        
        ax.axhline(0, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(-30, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(30, lw=0.25, alpha=0.5, linestyle="--", color="black")

        block_boundaries = np.where(data.trial_in_block == 0)[0]
        ax.vlines(
            block_boundaries, 
            ymin=-100, ymax=100, 
            color="black", lw=0.25, 
            alpha=0.5
        )
        for block in data.block.unique():
            for i in data.trial_perturb.unique():
                for c in data.coh_cat.unique():
                    coh_label = int(np.round(np.rad2deg(i), 0))
                    y = data[
                        (data.trial_perturb == i) & 
                        (data.block == block) & 
                        (data.coh_cat == c)
                    ]
                    x = y.index.to_numpy()
                    ax.scatter(
                        x, 
                        y.aim_target, 
                        s=6, color=coh_pal[c], 
                        alpha=0.99, 
                        marker=dir_mark[i], 
                        edgecolors="black", 
                        linewidth=0.25, 
                        label=coh_label
                    )
        plt.ylim([-105, 105])

ax.legend(
    handles=colour_ledge, fontsize="xx-small", 
    loc=9, ncol=2, borderpad=0.1,
    title="coherence | direction",
    title_fontsize="xx-small"
)

plt.suptitle("Aim error (direction + coherence)")
plt.savefig("imgs/aim_error_split_by_dir_coh.png", bbox_inches="tight", dpi=300)
plt.close()