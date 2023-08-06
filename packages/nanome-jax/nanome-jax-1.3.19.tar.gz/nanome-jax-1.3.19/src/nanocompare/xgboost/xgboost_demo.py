#!/usr/bin/env python3
# @Author   : Yang Liu
# @FileName : xgboost_demo.py
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/TheJacksonLaboratory/nanome
import joblib
from sklearn.preprocessing import MinMaxScaler

from nanocompare.eval_common import freq_to_label
from nanocompare.global_config import pic_base_dir
from nanocompare.global_settings import EPSLONG
from nanocompare.xgboost.xgboost_common import TRUTH_LABEL_COLUMN, meteore_deepsignal_megalodon_tool, \
    meteore_deepsignal_megalodon_model

basedir = '/projects/li-lab/yang/results/2021-11-26/xgboost_analysis/NA12878'

import glob
import os

import pandas as pd

flist = glob.glob(os.path.join(basedir, '*containNA_task*.tsv.gz'), recursive=True)

dflist = []
for infn in flist[:]:
    print(f"input file:{infn}")
    df1 = pd.read_csv(infn, index_col=None)
    df1.dropna(inplace=True)
    df1['Pos'] = df1['Pos'].astype(int)
    dflist.append(df1)

df = pd.concat(dflist)

## Apply coverage cutoff for BS-seq
df = df[df['Coverage'] >= 5]

## Apply fully-meth cutoff for BS-seq
df = df[(df['Freq'] <= EPSLONG) | (df['Freq'] >= 1.0 - EPSLONG)]

## Add truth_label
df[TRUTH_LABEL_COLUMN] = df['Freq'].apply(freq_to_label, args=(1.0, EPSLONG)).astype(int)

df.reset_index(drop=True, inplace=True)

print(f"Start METEORE prediction")
loaded_model = joblib.load(open(meteore_deepsignal_megalodon_model, 'rb'))
X_test = df[meteore_deepsignal_megalodon_tool]
y_test = df[TRUTH_LABEL_COLUMN]
X_test = MinMaxScaler().fit_transform(X_test)
y_pred_tool = pd.DataFrame(loaded_model.predict(X_test))[0].astype(int)  ##
y_score_tool = pd.DataFrame(loaded_model.predict_proba(X_test))[1]

df = pd.concat([df, y_pred_tool.rename('METEORE_pred'), y_score_tool.rename('METEORE_prob')], axis=1)

print(df, flush=True)

outfn = os.path.join(pic_base_dir, 'NA12878_train_data_all_chrs.csv.gz')
df.to_csv(outfn, index=False)
print(f"save to {outfn}")
