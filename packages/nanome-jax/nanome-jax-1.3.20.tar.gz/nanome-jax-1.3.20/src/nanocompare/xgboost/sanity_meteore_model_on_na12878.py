#!/usr/bin/env python3
# @Author   : Yang Liu
# @FileName : xgboost_demo.py
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/TheJacksonLaboratory/nanome

"""
python sanity_meteore_model_on_na12878.py /projects/li-lab/Nanopore_compare/nanome_paper_result/supp_data/xgboost_model/train_data/train_data_NA12878/NA12878_Top4_pred_bsseq_combine_containNA_task_train_data_chr22.tsv.gz
"""
import sys

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from nanocompare.xgboost.xgboost_common import TRUTH_LABEL_COLUMN, meteore_deepsignal_megalodon_model, \
    meteore_deepsignal_megalodon_tool, load_meteore_model


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

indf = pd.read_csv(infn, index_col=None)
indf.dropna(inplace=True)
indf.drop(['METEORE_pred', 'METEORE_prob'], axis=1)
indf.reset_index(drop=True, inplace=True)

meteore_clf = load_meteore_model(meteore_deepsignal_megalodon_model)
X_test = indf[meteore_deepsignal_megalodon_tool]
X_test = MinMaxScaler().fit_transform(X_test)
y_test = indf[TRUTH_LABEL_COLUMN]
y_pred_tool = pd.DataFrame(meteore_clf.predict(X_test))[0].astype(int).rename('METEORE_pred')  ##
y_score_tool = pd.DataFrame(meteore_clf.predict_proba(X_test))[1].rename('METEORE')
newdf = pd.concat([indf, y_score_tool, y_score_tool], axis=1)
print_performance(newdf)
