import sys
import os.path as op
from os import sep
from utilities import files
import pandas as pd

try:
    subjects_path = str(sys.argv[1])
except:
    subjects_path = "/home/mszul/datasets/explicit_implicit_beta/derivatives/processed"

try:
    output_path = str(sys.argv[2])
except:
    output_path = "/home/mszul/git/DANC_learning_beh/data"

print(subjects_path, op.exists(subjects_path))
print(output_path, op.exists(output_path))

subs = files.get_folders_files(subjects_path)[0]
subs.sort()

csv_files = []
for sub in subs:
    print(sub)
    csvs = files.get_files(sub, "sub", "-beh.csv")[2]
    csvs.sort
    csv_files.extend(csvs)

all_data = []
for i in csv_files:
    sub_id = i.split(sep)[-2]
    file_data = pd.read_csv(i)
    file_data.subject_id = sub_id
    all_data.append(file_data)

all_data = pd.concat(all_data)
all_data = all_data.sort_values(
    ["subject_id", "block", "trial_in_block"]
)
all_data.reset_index(inplace=True)

all_data["reach_sub_perturb"] = all_data.reach_target - all_data.perturb_cat
all_data["aim_sub_perturb"] = all_data.aim_target - all_data.perturb_cat

all_path = op.join(output_path, "all_data.csv")
all_data.to_csv(all_path, index=False)

explicit_path = op.join(output_path, "all_data_explicit.csv")
implicit_path = op.join(output_path, "all_data_implicit.csv")

all_data.loc[all_data.group == 1].to_csv(explicit_path, index=False)
all_data.loc[all_data.group == 0].to_csv(implicit_path, index=False)
