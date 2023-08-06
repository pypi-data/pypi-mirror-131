#!/usr/bin/env python3
# @Author   : Yang Liu
# @FileName : xgboost_demo5.py
# @Software : NANOME project
# @Organization : JAX Li Lab
# @Website  : https://github.com/TheJacksonLaboratory/nanome
"""
Split data for parallel
part1:  megalodon > 0 & deepsignal > 0
part2:  megalodon <= 0 & deepsignal <= 0
part3:  other cases
"""
import argparse
import os.path

import numpy as np
import pandas as pd

from nanocompare.global_config import pic_base_dir, set_log_debug_level, set_log_info_level, logger


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True,
                        help='input file')
    parser.add_argument('-o', type=str, help="output dir", default=pic_base_dir)
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

    basefn = os.path.basename(args.i)
    df = pd.read_csv(args.i, index_col=False, header=0, dtype=dtype)
    df.dropna(subset=['megalodon', 'deepsignal'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    logger.debug(f"df={df}")

    mask1 = (df.megalodon > 0) & (df.deepsignal > 0)
    mask2 = (df.megalodon <= 0) & (df.deepsignal <= 0)
    mask3 = ~ (mask1 | mask2)
    logger.debug(
        f"Check {mask1.sum():,} + {mask2.sum():,} + {mask3.sum():,} = {mask1.sum() + mask2.sum() + mask3.sum():,} == {len(df)}")
    mask_list = [mask1, mask2, mask3]
    for k, mask in enumerate(mask_list):
        outdf = df[mask]
        outfn = os.path.join(args.o, basefn.replace('.tsv.gz', f'_part{k + 1}.tsv.gz'))
        outdf.to_csv(outfn, index=False)
        logger.info(f"\n\nsave to {outfn}")

        megalodon_df = outdf[['ID', 'Chr', 'Pos', 'Strand', 'megalodon']].copy()
        megalodon_df.rename(columns={'megalodon': 'Score'}, inplace=True)
        outfn = os.path.join(args.o, basefn.replace('.tsv.gz', f'_part{k + 1}.tsv.gz').replace(
            'T5_pred_bsseq_combine_containNA_task', 'megaldon_per_read'))
        megalodon_df.to_csv(outfn, sep='\t', index=False)
        logger.info(f"save to {outfn}")

        deepsignal_df = outdf[['ID', 'Chr', 'Pos', 'Strand', 'deepsignal']].copy()
        deepsignal_df.rename(columns={'deepsignal': 'Score'}, inplace=True)
        outfn = os.path.join(args.o, basefn.replace('.tsv.gz', f'_part{k + 1}.tsv.gz').replace(
            'T5_pred_bsseq_combine_containNA_task', 'deepsignal_per_read'))
        deepsignal_df.to_csv(outfn, sep='\t', index=False)
        logger.info(f"save to {outfn}")

    ## K562_Top4_pred_bsseq_combine_containNA_task_chr15_part3.tsv.gz
