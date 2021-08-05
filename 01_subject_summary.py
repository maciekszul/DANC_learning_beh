import sys
import pandas as pd
import numpy as np
from matplotlib import gridspec
import matplotlib.pylab as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# display mode: switching between marker modes
try:
    display_mode = int(sys.argv[1])
except:
    display_mode = 0

try:
    all_data_path = str(sys.argv[2])
except:
    all_data_path = "/home/mszul/git/DANC_learning_beh/data/all_data.csv"



all_data = pd.read_csv(all_data_path)

subs_exp = all_data.loc[all_data.group == 1].subject_id.unique().tolist()
subs_imp = all_data.loc[all_data.group == 0].subject_id.unique().tolist()

group_dict = {
    0: ["implicit"],
    1: ["explicit"]
}

col_pal = ["#5CE619", "#195CE6", "#E6195C"]
markers_dir = ["v", "X", "^"]
perturb_dir = all_data.perturb_cat.unique()
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
        label=i
        ) for i in dir_mark.keys()
    ]
colour_ledge = [
    Patch(
        fc=coh_pal[i], ec=None, label=i
    ) for i in coh_pal.keys()
]

colour_ledge.extend(marker_ledge)

for i in group_dict.keys():
    group_data = all_data.loc[all_data.group == i]
    subjects = group_data.subject_id.unique().tolist()
    
    # dev only
    # subjects = subjects[7:9]
    # dev only

    gs = gridspec.GridSpec(len(subjects), 1, wspace=0.05, hspace=0.25)
    figure = plt.figure(figsize=(15, 5*len(subjects)))
    for row, sub in enumerate(subjects):

        ax = figure.add_subplot(gs[row, 0], label=sub)

        subject_data = group_data.loc[group_data.subject_id == sub]
        subject_data.reset_index(inplace=True)

        block_boundaries = np.where(subject_data.trial_in_block == 0)[0]
        
        ax.vlines(
            block_boundaries, 
            ymin=-100, ymax=100, 
            color="black", lw=0.25, 
            alpha=0.5
        )

        ax.axhline(0, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(-30, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(30, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(-15, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(15, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(-45, lw=0.25, alpha=0.5, linestyle="--", color="black")
        ax.axhline(45, lw=0.25, alpha=0.5, linestyle="--", color="black")

        ax.set_title(sub)
        ax.set_ylabel("Angle from the target [deg]")
        ax.set_xlabel("Block")

        for block in subject_data.block.unique():
            for perturb in subject_data.perturb_cat.unique():
                for coherence in subject_data.coh_cat.unique():
                    y = subject_data[
                        (subject_data.block == block) &
                        (subject_data.perturb_cat == perturb) &
                        (subject_data.coh_cat == coherence)
                    ]
                    x = y.index.to_numpy()
                    if display_mode == 0:
                        name_xx = "reach"
                        ax.scatter(
                            x,
                            y.reach_sub_perturb,
                            marker=dir_mark[perturb],
                            color=coh_pal[coherence],
                            alpha=0.99,
                            edgecolors="black",
                            linewidth=0.25
                        )
                    if display_mode == 1:
                        name_xx = "aim"
                        ax.scatter(
                            x,
                            y.aim_sub_perturb,
                            marker=dir_mark[perturb],
                            color=coh_pal[coherence],
                            alpha=0.99,
                            edgecolors="black",
                            linewidth=0.25
                        )
        
        print(subject_data.block.unique())
        print(subject_data.perturb_cat.unique())
        print(subject_data.coh_cat.unique())
        plt.ylim([-105, 105])
        ax.legend(
            handles=colour_ledge, fontsize="xx-small", 
            loc=1, ncol=2, borderpad=0.1,
            title="coherence | perturbation",
            title_fontsize="xx-small"
        )
    # figure.suptitle(group_dict[i][0], fontsize=12)

    path = "imgs/{}_subj_summary_{}.png".format(name_xx, group_dict[i][0])
    plt.savefig(path, bbox_inches="tight", dpi=300)
    plt.close()




"""
The offset in the final targets is caused by the perturbation you idiot. If 
participant was responding correctly, it was because they learned about
the perturbation.
"""