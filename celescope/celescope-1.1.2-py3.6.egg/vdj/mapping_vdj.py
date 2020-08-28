import os
import logging
import gzip
import numpy as np
import pandas as pd
import matplotlib as mpl
import re
import json
import argparse
mpl.use('Agg')
from matplotlib import pyplot as plt
from celescope.tools.utils import format_number
from celescope.tools.report import reporter

logger1 = logging.getLogger(__name__)


def summary(fq, alignments, type, outdir, sample, no_UMI_filter, debug):
    CHAINS = {
        "TCR": ["TRA", "TRB"],
        "BCR": ["IGH", "IGL", "IGK"],
    }
    chains = CHAINS[type]

    # out files
    VJ_UMI_count_unfiltered_file = f'{outdir}/{sample}_VJ_UMI_count_unfiltered.tsv'
    VJ_UMI_count_filtered_file = f'{outdir}/{sample}_VJ_UMI_count_filtered.tsv'

    # read fq
    read2 = gzip.open(fq, "rt")
    index = 0
    read_row_list = []
    while True:
        line1 = read2.readline()
        line2 = read2.readline()
        line3 = read2.readline()
        line4 = read2.readline()
        if not line4:
            break
        attr = str(line1).strip("@").split("_")
        barcode = str(attr[0])
        umi = str(attr[1])
        dic = {"readId": index, "barcode": barcode, "UMI": umi}
        read_row_list.append(dic)
        index += 1
    df_read = pd.DataFrame(read_row_list, columns=["readId", "barcode", "UMI"])
    logger1.info("fq reads to dataframe done.")
    read2.close()
    total_read = df_read.shape[0]

    # init row list
    mapping_summary_row_list = []

    # mapped
    alignment = pd.read_csv(alignments, sep="\t")
    alignment.readId = alignment.readId.astype(int)
    align_read = alignment.shape[0]
    df_read.readId = df_read.readId.astype(int)
    df_align = pd.merge(df_read, alignment, on="readId", how="right")

    mapping_summary_row_list.append({
        "item": "Reads Mapped to Any VDJ Gene",
        "count": align_read,
        "total_count": total_read,
    })

    # CDR3
    df_CDR3 = df_align[~pd.isnull(df_align["aaSeqCDR3"])]
    align_read_with_CDR3 = df_CDR3.shape[0]
    mapping_summary_row_list.append({
        "item": "Reads with CDR3",
        "count": align_read_with_CDR3,
        "total_count": total_read,
    })

    # correct CDR3
    df_correct_CDR3 = df_CDR3[~(df_CDR3["aaSeqCDR3"].str.contains("\*"))]
    align_read_with_correct_CDR3 = df_correct_CDR3.shape[0]
    mapping_summary_row_list.append({
        "item": "Reads with Correct CDR3",
        "count": align_read_with_correct_CDR3,
        "total_count": total_read,
    })

    # VJ
    df_VJ = df_correct_CDR3[
        (~pd.isnull(df_correct_CDR3['bestVGene'])) &
        (~pd.isnull(df_correct_CDR3['bestJGene']))
    ]
    df_VJ = df_VJ[df_VJ.bestVGene.str[:3] == df_VJ.bestJGene.str[:3]]
    df_VJ["chain"] = df_VJ.bestVGene.str[:3]
    df_VJ["VJ_pair"] = df_VJ["bestVGene"] + "_" + df_VJ["bestJGene"]
    Reads_Mapped_Confidently_to_Both_V_and_J_Gene = df_VJ.shape[0]
    mapping_summary_row_list.append({
        "item": "Reads Mapped Confidently to Both V and J Gene",
        "count": Reads_Mapped_Confidently_to_Both_V_and_J_Gene,
        "total_count": total_read
    })

    # chain
    for chain in chains:
        df_chain = df_VJ[df_VJ.chain == chain]
        Reads_Mapped_to_chain = df_chain.shape[0]
        mapping_summary_row_list.append({
            "item": f"Reads Mapped to {chain}",
            "count": Reads_Mapped_to_chain,
            "total_count": total_read,
        })

    # unique UMI
    df_UMI = df_VJ.drop_duplicates(subset=["barcode", "UMI"], keep="first")
    """
    unique_UMI = df_UMI.shape[0]
    summary_row_list.append({"item" :  "UMI unique count","count": unique_UMI,
        "total_count": align_read_with_correct_CDR3})
    """

    def df_UMI_to_count_str(df_UMI):

        df_UMI_count = df_UMI.groupby(["barcode"], as_index=False)["UMI"].agg("count")
        df_UMI_count = df_UMI_count.sort_values("UMI", ascending=False)
        df_UMI_VJ = df_UMI.groupby(["barcode", "VJ_pair"], as_index=False).agg("count")
        df_UMI_VJ = df_UMI_VJ.sort_values(["UMI"], ascending=False)
        df_UMI_VJ["UMI"] = df_UMI_VJ["UMI"].apply(str)
        df_UMI_VJ_count = df_UMI_VJ.groupby("barcode", as_index=False, sort=False).agg({
            "VJ_pair": lambda x: ",".join(x),
            "UMI": lambda x: ",".join(x),
        })
        df_UMI_VJ_count.rename(columns={"UMI": "VJ_pair_UMI"}, inplace=True)
        df_UMI_VJ_UMI_count = pd.merge(df_UMI_count, df_UMI_VJ_count, on="barcode")
        return df_UMI_VJ_UMI_count

    df_UMI_VJ_count = df_UMI_to_count(df_UMI)
    df_UMI_VJ_count.to_csv(VJ_UMI_count_unfiltered_file, sep="\t", index=False)   

    # filter1: keep top 1 in each combinations
    groupby_elements = [
        'barcode',
        'chain',
        'bestVGene',
        'bestJGene',
        'aaSeqCDR3',
        'nSeqCDR3',
    ]
    df_UMI_count = df_UMI.groupby(groupby_elements, as_index=False).agg({"UMI": "count"})
    df_UMI_count = df_UMI_count.sort_values("UMI", ascending=False)
    df_UMI_count_filter1 = df_UMI_count.groupby(["barcode", "chain"], as_index=False).head(1)
    df_UMI_filter1 = pd.merge(df_UMI, df_UMI_count_filter1[groupby_elements], on=groupby_elements, how="right")

    '''
    if debug:
        UMI_after_Contamination_Filtering = df_UMI_filter1.shape[0]
        mapping_summary_row_list.append({
            "item": "UMI after Contamination Filtering",
            "count": UMI_after_Contamination_Filtering,
            "total_count": unique_UMI,
        })
    '''

    # filter2: cell wtih at least two UMI of identical receptor type and CDR3 combinations.
    df_UMI_filter2 = df_UMI_filter1.groupby([
         "barcode",
         "type",
         "aaSeqCDR3",
         "nSeqCDR3",
         "bestVGene",
         "bestDGene",
         "bestJGene",
         "bestCGene",
    ], as_index=False).agg({"UMI": "count"})
    if not no_UMI_filter:
        df_UMI_filter2 = df_UMI_filter2[df_UMI_filter2.UMI > 1]
    df_UMI_VJ_count_filter2 = df_UMI_to_count(df_UMI_filter2)
    df_UMI_VJ_count_filter2.to_csv(VJ_UMI_count_filtered_file, sep="\t", index=False)


def mapping_vdj(args):
    step = "mapping_vdj"
    logger1.info(f'{step} start!')
    sample = args.sample
    outdir = args.outdir
    fq = args.fq
    type = args.type
    debug = args.debug

    report = f"{outdir}/{sample}_align.txt"
    not_align_fq = f"{outdir}/not_align.fq"
    read2_vdjca = f"{outdir}/read2.vdjca"
    alignments = f"{outdir}/{sample}_alignments.txt"

    if not os.path.exists(outdir):
        os.system('mkdir -p %s' % outdir)

    cmd = f"""
    mixcr align \
    --species hs \
    -t 5 \
    --not-aligned-R1 {not_align_fq} \
    --report {report} \
    -OallowPartialAlignments=true \
    -OvParameters.geneFeatureToAlign=VTranscriptWithP \
    {fq} \
    {read2_vdjca} 
    mixcr exportAlignments \
    {read2_vdjca} {alignments} \
    -readIds --force-overwrite -vGene -dGene -jGene -cGene \
    -nFeature CDR3 -aaFeature CDR3\n"""
    logger1.info(cmd)
    os.system(cmd)

    #summary
    summary(fq, alignments, type, debug)

    logger1.info(f'{step} done!')


def get_opts_mapping_vdj(parser, sub_program):
    parser.add_argument("--type", help='TCR or BCR', required=True)
    parser.add_argument("--debug", action='store_true')
    if sub_program:
        parser.add_argument('--outdir', help='output dir', required=True)
        parser.add_argument('--sample', help='sample name', required=True)
        parser.add_argument("--fq", required=True)
        parser.add_argument("--thread", default=1)
        parser.add_argument('--assay', help='assay', required=True)