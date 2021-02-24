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
# per block
# per direction of the perturbation (colour)
# per coherence of the b+w plot (position+marker)

coh_cat = ['zero', 'low', 'med', 'high']
coh_pos = [-0.40, -0.30, -0.10, 0.10]
coh_pos = [-0.27, -0.17, 0.03, 0.23]
coh_offset = {i[0]: i[1] for i in list(zip(coh_cat, coh_pos))}

dir_dir = [-30, 0,  30]
dir_col = ["#5CE619", "#195CE6", "#E6195C"]
dir_pal = {i[0]: i[1] for i in list(zip(dir_dir, dir_col))}

off_dir = {
    -30: 0.10,
    0: -0.05,
    30: 0.0
}

blank = Patch(
    fc="white", ec=None, label=""
)
zero = Patch(
    fc="#195CE6", ec=None, label="No perturbation"
)

down_lo = Patch(
    fc="#5CE619", ec=None, alpha=0.25, label=""
)

down_med = Patch(
    fc="#5CE619", ec=None, alpha=0.5, label=""
)

down_hi = Patch(
    fc="#5CE619", ec=None, alpha=1, label="Perturbation -30"
)

up_lo = Patch(
    fc="#E6195C", ec=None, alpha=0.25, label=""
)

up_med = Patch(
    fc="#E6195C", ec=None, alpha=0.5, label=""
)

up_hi = Patch(
    fc="#E6195C", ec=None, alpha=1, label="Perturbation +30"
)

handles = [
    blank, blank, zero,
    down_lo, down_med, down_hi,
    up_lo, up_med, up_hi
]

handles = [
    down_lo, up_lo, blank,
    down_med, up_med, blank,
    down_hi, up_hi, zero
]



coh_opa = [0.25, 0.5, 0.75, 1]
coh_alpha = {i[0]: i[1] for i in list(zip(coh_cat, coh_opa))}


which_group = 0

bs_results = all_pps.loc[all_pps.group == which_group].groupby(
    ["block", "perturb_cat", "coh_cat"]
).subject_id.max()
bs_results = bs_results.reset_index()
bs_results.drop(["subject_id"], axis=1, inplace=True)

fig, ax = plt.subplots(figsize=(12, 8))

ax.axhline(0, lw=0.45, alpha=0.5, linestyle="--", color="red")
ax.axhline(-30, lw=0.25, alpha=0.5, linestyle="--", color="red")
ax.axhline(30, lw=0.25, alpha=0.5, linestyle="--", color="red")

block_boundaries = [1.5, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3]
block_boundaries = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]
ax.vlines(
    block_boundaries, 
    ymin=-100, ymax=100, 
    color="black", lw=0.25, 
    alpha=0.5
)

for t in bs_results.itertuples():
    data = all_pps.loc[
        (all_pps.group == which_group) &
        (all_pps.block == t.block) &
        (all_pps.perturb_cat == t.perturb_cat) &
        (all_pps.coh_cat == t.coh_cat)
    ]
    data = data.dropna()
    box = dict(
        facecolor=dir_pal[t.perturb_cat],
        alpha=coh_alpha[t.coh_cat]
    )
    if t.block in [1, 2, 9]:
        pos_set = [t.block]
    else:
        pos_set = [t.block + coh_offset[t.coh_cat] + off_dir[t.perturb_cat]]
    ax.boxplot(
        data.reach_target.to_numpy(),
        notch=True,
        sym="",
        whis=(0.25, 97.5),
        bootstrap=5000,
        positions=pos_set,
        widths=0.10,
        patch_artist=True,
        boxprops=box
    )
ax.set_xticks(np.arange(1,10))
ax.set_xticklabels([str(i) for i in range(1, 10)])
ax.set_xlabel("Block")
ax.set_ylabel("Angle from the target")
plt.ylim((-80, 80))
plt.suptitle("Reach error (95% bootstrapped confidence intervals of the median)")

# ax.legend(
#     handles=handles, fontsize="small", 
#     loc=3, ncol=3, borderpad=0.1,
#     title="Coherence levels when perturbed\nLOW, MEDIUM, HIGH",
#     title_fontsize="xx-small", framealpha=1, columnspacing=0.1
# )

plt.savefig("imgs/reach_error_box_plot_summary_imp.png", bbox_inches="tight", dpi=300)

plt.ion()
plt.show()

fig, ax = plt.subplots(figsize=(12, 8))

ax.axhline(0, lw=0.45, alpha=0.5, linestyle="--", color="red")
ax.axhline(-30, lw=0.25, alpha=0.5, linestyle="--", color="red")
ax.axhline(30, lw=0.25, alpha=0.5, linestyle="--", color="red")

block_boundaries = [1.5, 2.3, 3.3, 4.3, 5.3, 6.3, 7.3, 8.3]
block_boundaries = [1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]
ax.vlines(
    block_boundaries, 
    ymin=-100, ymax=100, 
    color="black", lw=0.25, 
    alpha=0.5
)

for t in bs_results.itertuples():
    data = all_pps.loc[
        (all_pps.group == which_group) &
        (all_pps.block == t.block) &
        (all_pps.perturb_cat == t.perturb_cat) &
        (all_pps.coh_cat == t.coh_cat)
    ]
    data = data.dropna()
    box = dict(
        facecolor=dir_pal[t.perturb_cat],
        alpha=coh_alpha[t.coh_cat]
    )
    if t.block in [1, 2, 9]:
        pos_set = [t.block]
    else:
        pos_set = [t.block + coh_offset[t.coh_cat] + off_dir[t.perturb_cat]]
    ax.boxplot(
        data.aim_target.to_numpy(),
        notch=True,
        sym="",
        whis=(0.25, 97.5),
        bootstrap=5000,
        positions=pos_set,
        widths=0.10,
        patch_artist=True,
        boxprops=box
    )
ax.set_xticks(np.arange(1,10))
ax.set_xticklabels([str(i) for i in range(1, 10)])
ax.set_xlabel("Block")
ax.set_ylabel("Angle from the target")
plt.ylim((-80, 80))
plt.suptitle("Aim error (95% bootstrapped confidence intervals of the median)")

# ax.legend(
#     handles=handles, fontsize="small", 
#     loc=3, ncol=3, borderpad=0.1,
#     title="Coherence levels when perturbed\nLOW, MEDIUM, HIGH",
#     title_fontsize="xx-small", framealpha=1, columnspacing=0.1
# )

plt.savefig("imgs/aim_error_box_plot_summary_imp.png", bbox_inches="tight", dpi=300)

plt.ion()
plt.show()