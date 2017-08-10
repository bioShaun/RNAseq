#! /usr/bin/env python

import click
import os
import pandas as pd


FILE_SUFFIX = ['edgeR.DE_results.txt']


def anno_file_path(exp_file):
    exp_file_prefix, exp_file_suffix = os.path.splitext(exp_file)
    return '{prefix}.anno.txt'.format(prefix=exp_file_prefix)


@click.command()
@click.option('-q', '--quant_dir', type=click.Path(exists=True),
              help='directory with quant result to annotate')
@click.option('-a', '--anno', type=click.Path(exists=True),
              help='gene annotation in tab format')
@click.option('-p', '--pattern', default="",
              help='add user defined file pattern to annotate.')
def main(quant_dir, anno, pattern):
    # add pattern
    if pattern:
        FILE_SUFFIX.append(pattern)
    # get anno dataframe
    anno_df = pd.read_table(anno, index_col=0, sep='\t')
    # find files to annotate
    quant_files = os.listdir(quant_dir)
    for each_file in quant_files:
        for each_sfx in FILE_SUFFIX:
            if each_sfx in each_file:
                # annotate table
                each_file_path = os.path.join(quant_dir, each_file)
                each_file_df = pd.read_table(
                    each_file_path, index_col=0, sep='\t')
                each_anno_file_df = pd.merge(each_file_df, anno_df,
                                             left_index=True, right_index=True,
                                             how='left')
                anno_path = anno_file_path(each_file_path)
                each_anno_file_df.to_csv(anno_path, sep='\t')


if __name__ == '__main__':
    main()
