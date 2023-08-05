from __future__ import division
import argparse
import pkg_resources
import pandas as pd
import ast
import subprocess
import numpy as np

def run():
    parser = argparse.ArgumentParser(
        description='run diffacto for ms1searchpy results',
        epilog='''

    Example usage
    -------------
    $ ms1todiffacto -S1 sample1_1_proteins.tsv sample1_n_proteins.tsv -S2 sample2_1_proteins.tsv sample2_n_proteins.tsv
    -------------
    ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-dif', help='path to Diffacto', required=True)
    parser.add_argument('-S1', nargs='+', help='input files for S1 sample', required=True)
    parser.add_argument('-S2', nargs='+', help='input files for S2 sample', required=True)
    parser.add_argument('-S3', nargs='+', help='input files for S3 sample')
    parser.add_argument('-S4', nargs='+', help='input files for S4 sample')
    parser.add_argument('-S5', nargs='+', help='input files for S5 sample')
    parser.add_argument('-S6', nargs='+', help='input files for S6 sample')
    parser.add_argument('-S7', nargs='+', help='input files for S7 sample')
    parser.add_argument('-S8', nargs='+', help='input files for S8 sample')
    parser.add_argument('-S9', nargs='+', help='input files for S9 sample')
    parser.add_argument('-S10', nargs='+', help='input files for S10 sample')
    parser.add_argument('-S11', nargs='+', help='input files for S11 sample')
    parser.add_argument('-S12', nargs='+', help='input files for S12 sample')
    parser.add_argument('-peptides', help='name of output peptides file', default='peptides.txt')
    parser.add_argument('-samples', help='name of output samples file', default='sample.txt')
    parser.add_argument('-allowed_prots', help='path to allowed prots', default='')
    parser.add_argument('-out', help='name of diffacto output file', default='diffacto_out.txt')
    parser.add_argument('-norm', help='normalization method. Can be average, median, GMM or None', default='None')
    parser.add_argument('-impute_threshold', help='impute_threshold for missing values fraction', default='0.75')
    parser.add_argument('-min_samples', help='minimum number of samples for peptide usage', default='3')
    args = vars(parser.parse_args())

    replace_label = '_proteins.tsv'

    df_final = False

    allowed_prots = set()
    allowed_peptides = set()

    if not args['allowed_prots']:

        for i in range(1, 13, 1):
            sample_num = 'S%d' % (i, )
            if args[sample_num]:
                for z in args[sample_num]:
                    df0 = pd.read_table(z)
                    allowed_prots.update(df0['dbname'])
    else:
        for prot in open(args['allowed_prots'], 'r'):
            allowed_prots.add(prot.strip())


    for i in range(1, 13, 1):
        sample_num = 'S%d' % (i, )
        if args[sample_num]:
            for z in args[sample_num]:
                label = z.replace(replace_label, '')
                df1 = pd.read_table(z)
                df3 = pd.read_table(z.replace(replace_label, '_PFMs.tsv'))
                print(z)
                print(z.replace(replace_label, '_PFMs.tsv'))
                print(df3.shape)
                print(df3.columns)

                df3 = df3[df3['proteins'].apply(lambda x: any(z in allowed_prots for z in x.split(';')))]
                df3['proteins'] = df3['proteins'].apply(lambda x: ';'.join([z for z in x.split(';') if z in allowed_prots]))

                df3 = df3.sort_values(by='Intensity', ascending=False)
                df3 = df3.drop_duplicates(subset='sequence')
                df3 = df3.explode('proteins')

                df3[label] = df3['Intensity']
                df3['protein'] = df3['proteins']
                df3['peptide'] = df3['sequence']
                df3 = df3[['peptide', 'protein', label]]



                if df_final is False:
                    label_basic = label
                    df_final = df3.reset_index(drop=True)
                else:
                    df_final = df_final.reset_index(drop=True).merge(df3.reset_index(drop=True), on='peptide', how='outer')
                    df_final.protein_x.fillna(value=df_final.protein_y, inplace=True)
                    df_final['protein'] = df_final['protein_x']

                    df_final = df_final.drop(columns=['protein_x', 'protein_y'])


    print(df_final.columns)
    df_final = df_final.set_index('peptide')
    df_final['proteins'] = df_final['protein']
    df_final = df_final.drop(columns=['protein'])
    cols = df_final.columns.tolist()
    cols.remove('proteins')
    cols.insert(0, 'proteins')
    df_final = df_final[cols]
    df_final.fillna(value='')
    df_final.to_csv(args['peptides'], sep=',')

    out = open(args['samples'], 'w')
    for i in range(1, 13, 1):
        sample_num = 'S%d' % (i, )
        if args[sample_num]:
            for z in args[sample_num]:
                label = z.replace(replace_label, '')
                out.write(label + '\t' + sample_num + '\n')
    out.close()

    subprocess.call([args['dif'], '-i', args['peptides'], '-samples', args['samples'], '-out',\
     args['out'], '-normalize', args['norm'], '-impute_threshold', args['impute_threshold'], '-min_samples', args['min_samples']])



if __name__ == '__main__':
    run()
