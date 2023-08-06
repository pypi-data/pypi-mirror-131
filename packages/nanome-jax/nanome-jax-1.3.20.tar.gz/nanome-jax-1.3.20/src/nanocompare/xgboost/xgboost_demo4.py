#!/usr/bin/env python3
# @Author   : Yang Liu
# @FileName : xgboost_train.py
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/TheJacksonLaboratory/nanome
"""
Prepare NA data
"""
import argparse
from warnings import simplefilter

from nanocompare.eval_common import freq_to_label
from nanocompare.xgboost.xgboost_common import TRUTH_LABEL_COLUMN, SITES_COLUMN_LIST

simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)

import numpy as np
import pandas as pd

from nanocompare.global_config import set_log_debug_level, set_log_info_level, logger
from nanocompare.global_settings import EPSLONG


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--na-data', nargs='+', default=None,
                        help='data sets that include NAs')
    parser.add_argument('--test', type=int, help="if only test on some number of rows", default=None)
    parser.add_argument('-o', type=str, help="output file", default=None)
    parser.add_argument('--verbose', help="if output verbose info", action='store_true')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    if args.verbose:
        set_log_debug_level()
    else:
        set_log_info_level()
    logger.debug(f"args={args}")

    ## ID,Chr,Pos,Strand,nanopolish,megalodon,deepsignal,guppy,meteore,Freq,Coverage
    dtype = {'ID': str, 'Chr': str, 'Pos': np.int64, 'Strand': str, 'nanopolish': float,
             'megalodon': float, 'deepsignal': float, 'guppy': float, 'meteore': float,
             'Freq': float, 'Coverage': float}

    datadf_list = []
    for infn in args.na_data:
        datadf1 = pd.read_csv(infn, dtype=dtype, index_col=False, header=0, nrows=args.test)
        datadf1['Pos'] = datadf1['Pos'].astype(np.int64)
        # datadf1.drop('guppy', axis=1, inplace=True)
        datadf1.drop_duplicates(subset=["ID", "Chr", "Pos", "Strand"], inplace=True)
        datadf1.dropna(subset=["Freq", "Coverage"], inplace=True)
        datadf1 = datadf1[datadf1['Coverage'] >= 5]
        datadf1 = datadf1[(datadf1['Freq'] <= EPSLONG) | (datadf1['Freq'] >= 1.0 - EPSLONG)]
        datadf1[TRUTH_LABEL_COLUMN] = datadf1['Freq'].apply(freq_to_label).astype(int)
        datadf1.dropna(subset=["nanopolish", "megalodon", "deepsignal"], how='all', inplace=True)

        mask1 = datadf1['nanopolish'].isna()
        mask2 = datadf1['megalodon'].isna()
        mask3 = datadf1['deepsignal'].isna()
        mask = mask1 | mask2 | mask3
        datadf1 = datadf1[mask]

        datadf_list.append(datadf1)
    nadf = pd.concat(datadf_list)
    logger.debug(
        f"nadf={nadf}\n\ntotal={len(nadf):,}, nanopolish={nadf['nanopolish'].notna().sum():,}, megalodon={nadf['megalodon'].notna().sum():,}, deepsignal={nadf['deepsignal'].notna().sum():,}")

    nadf_sites = nadf[SITES_COLUMN_LIST].drop_duplicates()
    logger.debug(f"Sites={len(nadf_sites):,}")

    new_len = int(len(nadf_sites) * 0.1)
    new_sites = nadf_sites.sample(new_len)

    new_nadf = nadf.merge(new_sites, on=SITES_COLUMN_LIST, how='inner')
    logger.debug(
        f"new_nadf={new_nadf}\n\ntotal={len(new_nadf):,}, megalodon={new_nadf['megalodon'].notna().sum():,}, deepsignal={new_nadf['deepsignal'].notna().sum():,}")
    logger.debug(f"Sample sites={len(new_sites):,}")

    new_nadf.to_csv(args.o, index=False)
    logger.debug(f"save to {args.o}")

    logger.info(f"### NADF generate DONE")
