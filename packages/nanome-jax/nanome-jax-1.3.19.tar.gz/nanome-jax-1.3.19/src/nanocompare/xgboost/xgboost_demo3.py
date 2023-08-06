#!/usr/bin/env python3
# @Author   : Yang Liu
# @FileName : xgboost_demo.py
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/TheJacksonLaboratory/nanome
import glob
import os.path

import pandas as pd

from nanocompare.xgboost.xgboost_common import TRUTH_LABEL_COLUMN

def print_performance(the_df, info=None):
    print(info)
    deepsignal_accuracy = (the_df['deepsignal_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    megalodon_accuracy = (the_df['megalodon_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    nanopolish_accuracy = (the_df['nanopolish_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    meteore_accuracy = (the_df['METEORE_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    print(
        f"DeepSignal={deepsignal_accuracy:.3f}, Megalodon={megalodon_accuracy:.3f},Nanopolish={nanopolish_accuracy:.3f}, METEORE={meteore_accuracy:.3f}",
        flush=True)

indir = '/projects/li-lab/yang/results/2021-11-27/train_data_NA12878'

fnlist = glob.glob(os.path.join(indir, 'NA12878_Top4_pred_bsseq_combine_containNA_task_train_data_chr*.tsv.gz'))

print(fnlist)

total_sites = 0
total_preds = 0
for infn in fnlist:
    indf = pd.read_csv(infn, index_col=False)
    indf_sites = indf.drop_duplicates(subset=['Chr', 'Pos', 'Strand'])
    len_sites = len(indf_sites)
    len_preds = len(indf)
    print(
        f"{os.path.basename(infn)}:\n sites={len_sites:,}, preds={len_preds:,}")

    print(f"{indf_sites[TRUTH_LABEL_COLUMN].value_counts()}")

    print_performance(indf)
    total_sites += len_sites
    total_preds += len_preds

print(f"### Total sites={total_sites:,}, preds={total_preds:,}")
