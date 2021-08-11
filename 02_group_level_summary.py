import sys
from numpy.lib.arraysetops import unique
import pandas as pd
import numpy as np
from matplotlib import gridspec
import matplotlib.pylab as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from scipy.stats import gaussian_kde

# display mode: AIM vs REACH
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

colours_coh = ["#89cff0", "#149414", "#FFCE03", "#F00505"]
levels_coh = ["zero", "low", "med", "high"]
coh_pal = {i[0]: i[1] for i in list(zip(levels_coh, colours_coh))}
colour_ledge = [
    Patch(
        fc=coh_pal[i], ec=None, label=i
    ) for i in coh_pal.keys()
]

perturb = {
    0.0: 0.0,
    30.0: 0.0,
    -30.0: 0.0 
}
coherence = {
    'zero': "#89cff0", 
    'low': "#149414", 
    'med': "#FFCE03", 
    'high': "#F00505"
}

range_ang = np.linspace(-101, 101, num=200)



for group in  all_data.group.unique():
    perturb_ledge = [
        Patch(
            fc="black",
            ec=None,
            alpha=0.5,
            label=u"+30\N{DEGREE SIGN}"
        ),
        Patch(
            fc="black",
            ec=None,
            alpha=0.25,
            label=u"-30\N{DEGREE SIGN}"
        )
    ]
    if group == 0:
        perturb_ledge = [
            Patch(
                fc="black",
                ec=None,
                alpha=0.5,
                label=u"-30\N{DEGREE SIGN}"
            )
        ]
    f, ax = plt.subplots(figsize=(16,6))
    for block in all_data.block.unique():
        data = all_data[
            (all_data.block == block) &
            (all_data.group == group)
            ]
        for pt_dir in all_data.perturb_cat.unique():
            for coh_lv in all_data.coh_cat.unique():
                chunk = data[
                    (data.perturb_cat == pt_dir) &
                    (data.coh_cat == coh_lv)
                ]
                if chunk.size != 0:
                    # print(pt_dir, coh_lv, chunk.shape[0], data.shape[0], all_data.shape[0])
                    if display_mode == 0:
                        X = chunk.reach_sub_perturb.to_numpy()
                        name_xx = "reach"
                    if display_mode == 1:
                        X = chunk.aim_sub_perturb.to_numpy()
                        name_xx = "aim"
                    X = X[~np.isnan(X)]
                    kde = gaussian_kde(X)
                    result = kde(range_ang) * 15
                    alpha = 0.5
                    if (pt_dir == -30.0) & (group == 1):
                        result = -result
                        alpha = 0.25

                    median_ix = np.where(range_ang <= np.median(X))[0][-1]
                    ax.fill_betweenx(
                        range_ang,
                        result + block,
                        block,
                        color=coherence[coh_lv],
                        alpha=alpha,
                        linewidth=0
                    )
                    ax.plot(
                        [block, block+result[median_ix]],
                        [np.median(X), np.median(X)],
                        "--",
                        c=coherence[coh_lv],
                        alpha=alpha
                    )

    ax.set_xticks(all_data.block.unique())
    ax.set_ylabel("Angle from the target [deg]")
    ax.set_xlabel("Block")

    leg1 = plt.legend(
            handles=colour_ledge, fontsize="x-small", 
            loc=1, ncol=1, borderpad=0.1,
            title="coherence",
            title_fontsize="xx-small"
        )
    leg2 = plt.legend(
            handles=perturb_ledge, fontsize="x-small", 
            loc=4, ncol=1, borderpad=0.1,
            title="perturbation",
            title_fontsize="xx-small"
        )

    plt.gca().add_artist(leg1)
    plt.gca().add_artist(leg2)
    # plt.show(block=False)
    path = "imgs/{}_group_summary_{}.png".format(name_xx, group_dict[group][0])
    plt.savefig(path, bbox_inches="tight", dpi=150)
    plt.close()