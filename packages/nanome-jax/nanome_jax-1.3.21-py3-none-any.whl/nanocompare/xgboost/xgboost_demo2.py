#!/usr/bin/env python3
# @Author   : Yang Liu
# @FileName : xgboost_demo.py
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/TheJacksonLaboratory/nanome
import os.path
import sys
from random import sample

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from nanocompare.eval_common import freq_to_label
from nanocompare.global_settings import EPSLONG
from nanocompare.xgboost.xgboost_common import TRUTH_LABEL_COLUMN, meteore_deepsignal_megalodon_model, \
    meteore_deepsignal_megalodon_tool

simu_perf = 0.75


def print_performance(the_df, info=None):
    print(info)
    deepsignal_accuracy = (the_df['deepsignal_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    megalodon_accuracy = (the_df['megalodon_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    nanopolish_accuracy = (the_df['nanopolish_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    meteore_accuracy = (the_df['METEORE_pred'] == the_df[TRUTH_LABEL_COLUMN]).sum() / len(the_df)
    print(
        f"DeepSignal={deepsignal_accuracy:.3f}, Megalodon={megalodon_accuracy:.3f},Nanopolish={nanopolish_accuracy:.3f}, METEORE={meteore_accuracy:.3f}",
        flush=True)


infn = sys.argv[1]
outdir = sys.argv[2]
indata = pd.read_csv(infn, index_col=None, nrows=None)
indata.dropna(inplace=True)
indata['Pos'] = indata['Pos'].astype(int)
indata.drop_duplicates(subset=['ID', 'Chr', 'Pos', 'Strand'], inplace=True)

df = indata

df = df[df['Coverage'] >= 5]

## Apply fully-meth cutoff for BS-seq
df = df[(df['Freq'] <= EPSLONG) | (df['Freq'] >= 1.0 - EPSLONG)]

## Add truth_label
df[TRUTH_LABEL_COLUMN] = df['Freq'].apply(freq_to_label).astype(int)

df.reset_index(drop=True, inplace=True)
print(f"df={len(df):,} (total predictions)")
print(f"Start METEORE prediction", flush=True)
loaded_model = joblib.load(open(meteore_deepsignal_megalodon_model, 'rb'))
X_test = df[meteore_deepsignal_megalodon_tool]
y_test = df[TRUTH_LABEL_COLUMN]

min_max_scaler = MinMaxScaler().fit(X_test)
print(f"data_min={min_max_scaler.data_min_}, data_max={min_max_scaler.data_max_}")

X_test1 = MinMaxScaler().fit_transform(X_test)
y_pred_tool = pd.DataFrame(loaded_model.predict(X_test1))[0].astype(int)  ##
y_score_tool = pd.DataFrame(loaded_model.predict_proba(X_test1))[1]

df_X_test1 = pd.DataFrame(data=X_test1, columns=['deepsignal_scale', 'megalodon_scale'])

df['megalodon_pred'] = df['megalodon'].apply(lambda x: 1 if x > 0 else 0)
df['nanopolish_pred'] = df['nanopolish'].apply(lambda x: 1 if x > 0 else 0)
df['deepsignal_pred'] = df['deepsignal'].apply(lambda x: 1 if x > 0 else 0)

df = pd.concat([df, y_pred_tool.rename('METEORE_pred'), y_score_tool.rename('METEORE_prob'), df_X_test1], axis=1)

print(df, flush=True)
print_performance(df, info='DF perf')

top3_correct_mask = (df['nanopolish_pred'] == df[TRUTH_LABEL_COLUMN]) | (
        df['megalodon_pred'] == df[TRUTH_LABEL_COLUMN]) | (df['deepsignal_pred'] == df[TRUTH_LABEL_COLUMN])
meteore_fail_mask = df['METEORE_pred'] != df[TRUTH_LABEL_COLUMN]

# select1: meteore failed points, but other tools correct
select1 = meteore_fail_mask & top3_correct_mask
print(f"select1={select1.sum():,} (meteore failed, but other tools correct), total={len(df):,}")

num_min_max_sample = 1000
for k in range(2):
    min_select = pd.Series(np.isclose(X_test.iloc[:, k], min_max_scaler.data_min_[k]))
    min_select_list = list(min_select[min_select].index.values)

    min_select = False & min_select
    if len(min_select_list) > num_min_max_sample:
        # print(f"min_select_list={min_select_list}")
        min_select_list = sample(min_select_list, num_min_max_sample)
    min_select.iloc[min_select_list] = True

    max_select = pd.Series(np.isclose(X_test.iloc[:, k], min_max_scaler.data_max_[k]))
    max_select_list = list(max_select[max_select].index.values)

    max_select = False & max_select
    if len(max_select_list) > num_min_max_sample:
        max_select_list = sample(max_select_list, num_min_max_sample)
    max_select.iloc[max_select_list] = True

    print(f"colk={k}, min_select={min_select.sum()}, max_select={max_select.sum()}")
    select1 = select1 | min_select | max_select

    # select1 = select1 | np.isclose(X_test.iloc[:, k], min_max_scaler.data_min_[k]) | np.isclose(X_test.iloc[:, k],
    #                                                                                             min_max_scaler.data_max_[
    #                                                                                                 k])
print(f"After add min and max, select1={select1.sum():,}")

df1 = df[select1]
print_performance(df1, info='DF1 perf')

select2 = ~select1

sample_num = int(select1.sum() / (1 - simu_perf) * simu_perf)

select2_index_list = list(select2[select2].index)
samp_index = sample(select2_index_list,
                    sample_num if sample_num <= len(select2_index_list) else len(select2_index_list))

df2 = df.iloc[samp_index, :]
print_performance(df2, info='DF2 perf')

df3 = pd.concat([df1, df2])
print_performance(df3, info='DF3 perf')
print(f"Final selection predictions: df3={len(df3):,} from df={len(df):,}")

dfsites = df.drop_duplicates(subset=['Chr', 'Pos', 'Strand'])
df3_sites = df3.drop_duplicates(subset=['Chr', 'Pos', 'Strand'])
print(f"Final selection sites: df3_sites={len(df3_sites):,} from dfsites={len(dfsites):,}")

outfn = os.path.join(outdir, os.path.basename(infn).replace('_task_', '_task_train_data_'))
df3.to_csv(outfn, index=False)
print(f"save to {outfn}")
