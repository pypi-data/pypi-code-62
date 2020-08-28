#!/bin/env python
#coding=utf8

import gzip
import os
import pandas as pd
import logging
import numpy as np
import sys
import argparse
import matplotlib as mpl
import re
import json
mpl.use('Agg')
from matplotlib import pyplot as plt
import os,glob
from celescope.tools.utils import format_number
from celescope.tools.report import reporter

logger1 = logging.getLogger(__name__)


def count_vdj(args):
    step = 'count_vdj'
    CHAINS =  {"TCR":["TRA","TRB"],"BCR":["IGH","IGL","IGK"]}

    sample = args.sample
    matched_dir = args.matched_dir
    if (not matched_dir) or (matched_dir == "None"):
        matched_bool = False
    else:
        matched_bool = True
    UMI_min = args.UMI_min
    outdir = args.outdir
    alignment_file = args.alignments
    type = args.type
    debug = args.debug
    no_UMI_filter = args.no_UMI_filter
    chains = CHAINS[type]

    read2_file = "{}/02.cutadapt/{}_clean_2.fq.gz".format(sample,sample)
    barcode = {}
    VDJ_UMI_count_file = "{}/VDJ_UMI_count.tsv".format(outdir)
    cell_VJ_UMI_file = "{}/cell_VJ_UMI_count.tsv".format(outdir)
    cell_valid_CDR3_file = "{}/cell_valid_CDR3.tsv".format(outdir)
    clonetypes_file = "{}/clonetypes.tsv".format(outdir)
    matched_clonetypes_file = "{}/matched_clonetypes.tsv".format(outdir)
    top10_clonetypes_file =  "{}/top10_clonetypes.tsv".format(outdir)

    #df_read_file = "{}/df_read.tsv".format(outdir)
    #df_align_file = "{}/df_align.tsv".format(outdir)
    #UMI_sum_file = "{}/barcode_UMI.tsv".format(outdir)
    #summary_file = "{}/summary.tsv".format(outdir)
    #other_metrics_file = "{}/other_metrics.txt".format(outdir)
    #UMI_count_file = "{}/UMI_count.tsv".format(outdir)
    #fig_file = "{}/UMI_barcode.png".format(outdir)
    #infer_T_file = "{}/inferred_Tcell.tsv".format(outdir)
    #filter_fig_file = "{}/filter_UMI_barcode.png".format(outdir)

    if matched_bool:
        logging.info("matched scRNA-Seq directory: "+ matched_dir)
        match_barcode_file1 = glob.glob("{matched_dir}/05.count/*_cellbarcode.tsv".format(matched_dir=matched_dir))
        match_barcode_file2 = glob.glob("{matched_dir}/05.count/matrix_10X/*_cellbarcode.tsv".format(matched_dir=matched_dir))
        match_barcode_file = (match_barcode_file1 + match_barcode_file2)[0]
        matched_cell_barcodes = pd.read_csv(match_barcode_file, header=None)
    
    mapping_summary_row_list = []
    cell_summary_row_list = []

    if not os.path.exists(outdir):
        os.system('mkdir -p %s' % outdir) 
        
    read2 = gzip.open(read2_file, "rt")
    index = 0
    row_list = []
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
        dic = {"readId":index,"barcode":barcode,"UMI":umi}
        row_list.append(dic)
        index += 1
    df_read = pd.DataFrame(row_list,columns=["readId","barcode","UMI"])
    logging.info(sample+" running...")
    logging.info("reads dataframe done.")
    read2.close()
    total_read = df_read.shape[0]


    # mapped
    alignment = pd.read_csv(alignment_file,sep="\t")
    alignment.readId = alignment.readId.astype(int)
    align_read = alignment.shape[0]
    df_read.readId = df_read.readId.astype(int)
    df_align = pd.merge(df_read,alignment,on="readId",how="right")
    #table2.to_csv(table2_file,sep="\t",index=False)
    mapping_summary_row_list.append({"item" : "Reads Mapped to Any VDJ Gene","count": align_read,"total_count": total_read})

    # CDR3
    df_CDR3 = df_align[~pd.isnull(df_align["aaSeqCDR3"])]
    align_read_with_CDR3 = df_CDR3.shape[0]
    mapping_summary_row_list.append({"item" :  "Reads with CDR3","count": align_read_with_CDR3,"total_count": total_read})

    # correct CDR3
    df_correct_CDR3 = df_CDR3[~(df_CDR3["aaSeqCDR3"].str.contains("\*"))]
    align_read_with_correct_CDR3 = df_correct_CDR3.shape[0]
    mapping_summary_row_list.append({"item" :  "Reads with Correct CDR3","count": align_read_with_correct_CDR3,
        "total_count": total_read})

    # VJ
    df_VJ = df_correct_CDR3[(~pd.isnull(df_correct_CDR3['bestVGene'])) & (~pd.isnull(df_correct_CDR3['bestJGene']))]
    df_VJ = df_VJ[ df_VJ.bestVGene.str[:3] == df_VJ.bestJGene.str[:3] ]
    df_VJ["type"] = df_VJ.bestVGene.str[:3]
    df_VJ["VJ_pair"] =df_VJ["bestVGene"] + "_" + df_VJ["bestJGene"]
    Reads_Mapped_Confidently_to_Both_V_and_J_Gene = df_VJ.shape[0]
    mapping_summary_row_list.append({"item" :  "Reads Mapped Confidently to Both V and J Gene",
        "count": Reads_Mapped_Confidently_to_Both_V_and_J_Gene,
        "total_count": total_read}) 

    # chain   
    for chain in chains:
        df_chain = df_VJ[df_VJ.type==chain]
        Reads_Mapped_to_chain = df_chain.shape[0]
        mapping_summary_row_list.append({"item" :  "Reads Mapped to "+chain,"count": Reads_Mapped_to_chain,
        "total_count": total_read})        

    # unique UMI
    df_UMI = df_VJ.drop_duplicates(subset=["barcode","UMI"],keep="first")
    unique_UMI = df_UMI.shape[0]
    """
    summary_row_list.append({"item" :  "UMI unique count","count": unique_UMI,
        "total_count": align_read_with_correct_CDR3})
    """

    def df_UMI_to_df_count(df_UMI):
        """
        df_UMI_count
        barcode	UMI
        2814	CTGTAGCCAGATCGCACTGAGCCA	19
        """
        df_UMI_count = df_UMI.groupby(["barcode"],as_index=False)["UMI"].agg("count")
        df_UMI_count = df_UMI_count.sort_values("UMI",ascending=False)
        df_UMI_VJ = df_UMI.groupby(["barcode","VJ_pair"],as_index=False).agg("count")
        df_UMI_VJ = df_UMI_VJ.sort_values(["UMI"],ascending=False)
        df_UMI_VJ["UMI"] = df_UMI_VJ["UMI"].apply(str)
        df_UMI_VJ_count = df_UMI_VJ.groupby("barcode",as_index=False,sort=False).agg({"VJ_pair":lambda x:",".join(x),"UMI":lambda x:",".join(x)})
        df_UMI_VJ_count.rename(columns={"UMI":"VJ_pair_UMI"},inplace=True)
        df_UMI_VJ_UMI_count = pd.merge(df_UMI_count,df_UMI_VJ_count,on="barcode")
        return df_UMI_VJ_UMI_count     

    """
    total UMI and VJ_pair UMI per barcode
    df_UMI_VJ_UMI_count:
    barcode	UMI	VJ_pair	VJ_pair_UMI
0	CTGTAGCCAGATCGCACTGAGCCA	19	TRBV7-3_TRBJ2-5,TRBV5-4_TRBJ2-3,TRBV29-1_TRBJ1...	14,2,1,1,1
    """
    df_UMI_VJ_UMI_count = df_UMI_to_df_count(df_UMI)
    df_UMI_VJ_UMI_count.to_csv(VDJ_UMI_count_file,sep="\t",index=False)   


    """
    filter: keep top 1 VJ_pair in each barcode and type combinations
    sum(df_temp.UMI) == df_filtered.shape[0]

    df_temp:
    barcode	VJ_pair	type	UMI
84	b'@AACCGAGAAAACATCGCTAAGGTC	TRBV5-1_TRBJ2-2	TRB	15

    df_filtered:
    Unnamed: 0  readId  barcode UMI bestVGene   bestDGene   bestJGene   bestCGene   aaSeqCDR3   type    VJ_pair
0   0   0   GAACAGGCGTCGTAGACGACTGGA    GTCCCACG    TRBV6-5 TRBD1   TRBJ1-4 NaN CASSYQKTGGFENLVF    TRB TRBV6-5_TRBJ1-4
1   1   1   ACACAGAAACGTATCAAAGACGGA    CATGGTCA    TRBV30  TRBD1   TRBJ2-1 TRBC2   CAWSHGIDAQFF    TRB TRBV30_TRBJ2-1

    df_UMI_sum
    barcode UMI
0   AAACATCGAAACATCGGGTGCGAA    7
1   AAACATCGAACAACCAACACGACC    1
    """
    df_temp = df_UMI.groupby(["barcode","VJ_pair","type"],as_index=False).agg({"UMI":"count"})
    df_temp = df_temp.sort_values("UMI",ascending=False)
    df_temp = df_temp.groupby(["barcode","type"],as_index=False).head(1)
    df_filtered = pd.merge(df_UMI,df_temp[["barcode","VJ_pair"]],on=["barcode","VJ_pair"],how="right")
    if debug:
        UMI_after_Contamination_Filtering = df_filtered.shape[0]
        mapping_summary_row_list.append({"item" :  "UMI after Contamination Filtering","count": UMI_after_Contamination_Filtering,
            "total_count": unique_UMI})


    df_UMI_sum = df_temp.groupby("barcode",as_index=False).agg({"UMI":"sum"})

    # barcode rank plot
    """
        df_barcode_count = df_UMI_sum.groupby(['UMI']).size().reset_index(name='barcode_counts')
        sorted_df = df_barcode_count.sort_values("UMI",ascending=False)
        barcode_cumsum = sorted_df["barcode_counts"].cumsum()
        UMI_counts = sorted_df["UMI"]
        dict = {"barcode_rank":barcode_cumsum,"UMI_counts":UMI_counts}
        df = pd.DataFrame(dict)
        max_barcode = int(df.iloc[-1:].barcode_rank)
        df1 = pd.DataFrame({"barcode_rank":range(1,max_barcode+1)})
        df2 = pd.merge(df1,df,on=["barcode_rank"],how="left")
        df3 = df2.bfill()
        df.to_csv(UMI_count_file,sep="\t",index=False)
        fig = plt.figure()
        plt.plot(df3["barcode_rank"],df3["UMI_counts"])
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel("barcode_rank")
        plt.ylabel("UMI_counts")
        plt.title(sample)
        plt.grid(which="both")
        fig.savefig(filter_fig_file)
    """

    ############################ cell calling ######################################
    """
    cell calling: keep UMIs >= UMI_min
    """
    def report_prepare(df,outdir):

        json_file = outdir + '/.data.json'
        if not os.path.exists(json_file):
            data = {}
        else:
            fh = open(json_file)
            data = json.load(fh)
            fh.close()

        df = df.sort_values('UMI', ascending=False)
        data['CB_num'] = df[df['mark'] == 'CB'].shape[0]
        data['Cells'] = list(df.loc[df['mark'] == 'CB', 'UMI'])
        data['UB_num'] = df[df['mark'] == 'UB'].shape[0]
        data['Background'] = list(df.loc[df['mark'] == 'UB', 'UMI'])

        with open(json_file, 'w') as fh:
            json.dump(data, fh)

    if (not UMI_min) or (UMI_min=="None") :
        rank = 20
        df_UMI_sum_sorted = df_UMI_sum.sort_values(["UMI"],ascending=False)
        rank_UMI = df_UMI_sum_sorted.iloc[rank,:]["UMI"]
        UMI_min = int(rank_UMI/10)
    else:
        UMI_min = int(UMI_min)
    df_UMI_cell = df_UMI_sum[df_UMI_sum.UMI>=UMI_min]
    df_UMI_sum["mark"] = df_UMI_sum["UMI"].apply(lambda x:"CB" if (x>=UMI_min) else "UB")
    report_prepare(df_UMI_sum,outdir+"/../")

    cell_barcodes = set(df_UMI_cell.barcode)
    df_cell_filtered = df_filtered[df_filtered.barcode.isin(cell_barcodes)]
    cell_number = len(cell_barcodes)
    cell_summary_row_list.append({"item" :  "Estimated Number of Cells","count": cell_number,
        "total_count": cell_number})
        
    
    """
    df_cell_filtered_UMI_VJ_count:
barcode	UMI	VJ_pair	VJ_pair_UMI
0	TAGGATGACGCATACACGACACAC	16	TRAV4_TRAJ22,TRBV12-3_TRBJ1-1	15,1
    """
    df_cell_filtered_UMI_VJ_count = df_UMI_to_df_count(df_cell_filtered)
    df_cell_filtered.fillna("NA",inplace=True)
    df_cell_filtered_UMI_VJ_count.to_csv(cell_VJ_UMI_file,sep="\t",index=False)  


    """
    CDR3 type
    cell wtih at least two UMI of identical receptor type and CDR3 combinations.
    df_valid_CDR3:
barcode aaSeqCDR3_TRA   aaSeqCDR3_TRB   UMI_TRA UMI_TRB
0   AAACATCGACCACTGTAGATGTAC    NA  CASSLDGTYGYTF   NA  5
1   AAACATCGACCACTGTCCATCCTC    NA  CSAREGHPYEQYF   NA  27
    """
    df_CDR3 = df_cell_filtered.groupby(["barcode","type","aaSeqCDR3","nSeqCDR3","bestVGene","bestDGene","bestJGene","bestCGene"],as_index=False).agg({"UMI":"count"})
    if no_UMI_filter:
        df_valid_CDR3 = df_CDR3
    else:
        df_valid_CDR3 = df_CDR3[df_CDR3.UMI>1]
    df_valid_CDR3 = df_valid_CDR3[df_valid_CDR3["type"].isin(chains)]
    df_valid_CDR3 = df_valid_CDR3.sort_values("UMI",ascending=False)
    df_valid_CDR3 = df_valid_CDR3.groupby(["barcode","type"],as_index=False).head(1)

    # count
    df_valid_CDR3_count = df_valid_CDR3.set_index(["barcode","type"])
    df_valid_CDR3_count = df_valid_CDR3_count.unstack()
    df_valid_CDR3_count.columns = ['_'.join(col) for col in df_valid_CDR3_count]
    df_valid_CDR3_count = df_valid_CDR3_count.reset_index()
    df_valid_CDR3_count.fillna(inplace=True,value="NA")

    # clonetypes
    seqs = ["aaSeqCDR3","nSeqCDR3"]
    cols = []
    for chain in chains:
        for seq in seqs:
            cols.append("_".join([seq,chain]))

    for col in cols:
        if not (col in list(df_valid_CDR3_count.columns)):
            df_valid_CDR3_count[col] = "NA"

    df_clonetypes = df_valid_CDR3_count.copy()
      
    df_clonetypes = df_clonetypes.groupby(cols,as_index=False).agg({"barcode":"count"}).sort_values("barcode",ascending=False)
    total_CDR3_barcode_number =  sum(df_clonetypes.barcode)
    df_clonetypes["percent"] = df_clonetypes.barcode/total_CDR3_barcode_number*100
    df_clonetypes["percent"] = df_clonetypes["percent"].apply(lambda x:round(x,2))

    #add clonetype ID
    df_clonetypes = df_clonetypes.reset_index()
    df_clonetypes["clonetype_ID"] = pd.Series(df_clonetypes.index)+1
    df_clonetypes.drop(columns=["index"],inplace=True)

    # order 
    order = ["clonetype_ID"] + cols + ["barcode","percent"]
    df_clonetypes = df_clonetypes[order]
    df_clonetypes.rename(columns={"barcode":"barcode_count"},inplace=True)

    df_clonetypes.to_csv(clonetypes_file,sep="\t",index=False)
    valid_CDR3_cell = len(np.unique(df_valid_CDR3["barcode"]))
    cell_summary_row_list.append({"item" :  "Cell with Confident CDR3","count": valid_CDR3_cell,
        "total_count": cell_number})    

    if type=="TCR":
        df_TRA_TRB = df_valid_CDR3_count[(df_valid_CDR3_count.aaSeqCDR3_TRA!="NA") & (df_valid_CDR3_count.aaSeqCDR3_TRB!="NA")]
        Cell_with_TRA_and_TRB = df_TRA_TRB.shape[0]
        cell_summary_row_list.append({"item" :  "Cell with TRA and TRB","count": Cell_with_TRA_and_TRB,
            "total_count": cell_number})

        UMI_col_dic = {"TRA":"UMI_TRA","TRB":"UMI_TRB"}
        for chain in UMI_col_dic:
            UMI_col_name = UMI_col_dic[chain]
            if UMI_col_name in df_valid_CDR3_count.columns:
                df_valid_CDR3_count[UMI_col_name].replace("NA",0,inplace=True)
                Median_chain_UMIs_per_Cell = np.median(df_valid_CDR3_count[UMI_col_name])
            else:
                Median_chain_UMIs_per_Cell = 0
            cell_summary_row_list.append({
            "item" :  "Median {chain} UMIs per Cell".format(chain=chain),
            "count": Median_chain_UMIs_per_Cell,
            "total_count": np.nan})

        """
        df cell barcode filter
        intersect cell_barcodes from normal scRNA-Seq with barcode from TCR seq
        """
        if matched_bool:
            matched_cell_barcodes = set(matched_cell_barcodes[0])
            matched_cell_number = len(matched_cell_barcodes)
            cell_with_matched_barcode = matched_cell_barcodes.intersection(cell_barcodes)
            cell_with_matched_barcode_number = len(cell_with_matched_barcode)

            df_matched = df_valid_CDR3_count[df_valid_CDR3_count.barcode.isin(matched_cell_barcodes)]

            # median matched UMI
            df_matched_TRA_TRB = df_matched[(df_matched.aaSeqCDR3_TRA!="NA") & (df_matched.aaSeqCDR3_TRB!="NA")]
            matched_cell_with_TRA_and_TRB = df_matched_TRA_TRB.shape[0]

            cell_summary_row_list.append({"item" :  "Cell with Matched Barcode","count": cell_with_matched_barcode_number,
            "total_count": cell_number})
            cell_summary_row_list.append({"item" :  "Cell with Matched Barcode, TRA and TRB","count": matched_cell_with_TRA_and_TRB,
            "total_count": cell_number})

            """
            df_match_clonetypes
            """
            df_matched_valid_CDR3_count = df_matched.groupby(cols,as_index=False).agg({"barcode":"count"}).sort_values("barcode",ascending=False)
            total_matched_CDR3_barcode_number =  sum(df_matched_valid_CDR3_count.barcode)
            df_matched_valid_CDR3_count["percent"] = df_matched_valid_CDR3_count.barcode/total_matched_CDR3_barcode_number*100
            df_matched_valid_CDR3_count["percent"] = df_matched_valid_CDR3_count["percent"].apply(lambda x:round(x,2))
            df_matched_valid_CDR3_count.to_csv(matched_clonetypes_file,sep="\t",index=False)    


    # BCR
    elif type=="BCR":
        df_heavy_and_light = df_valid_CDR3_count[(df_valid_CDR3_count.aaSeqCDR3_IGH!="NA") & 
            ( (df_valid_CDR3_count.aaSeqCDR3_IGL!="NA") | (df_valid_CDR3_count.aaSeqCDR3_IGK!="NA"))]
        Cell_with_Heavy_and_Light_Chain = df_heavy_and_light.shape[0]
        cell_summary_row_list.append({"item" :  "Cell with Heavy and Light Chain","count": Cell_with_Heavy_and_Light_Chain,
        "total_count": cell_number})

        UMI_col_dic = {"IGH":"UMI_IGH","IGL":"UMI_IGL","IGK":"UMI_IGK"}
        for chain in UMI_col_dic:
            UMI_col_name = UMI_col_dic[chain]
            if UMI_col_name in df_valid_CDR3_count.columns:
                df_valid_CDR3_count[UMI_col_name].replace("NA",0,inplace=True)
                df_valid_CDR3_count_over_zero = df_valid_CDR3_count[df_valid_CDR3_count[UMI_col_name]>0]
                Median_chain_UMIs_per_Cell = np.median(df_valid_CDR3_count_over_zero[UMI_col_name])
            else:
                Median_chain_UMIs_per_Cell = 0
            cell_summary_row_list.append({
            "item" :  "Median {chain} UMIs per Cell".format(chain=chain),
            "count": Median_chain_UMIs_per_Cell,
            "total_count": np.nan})    

        """
        df cell barcode filter
        intersect cell_barcodes from normal scRNA-Seq with barcode from BCR seq
        """
        if matched_bool:
            matched_cell_barcodes = set(matched_cell_barcodes[0])
            matched_cell_number = len(matched_cell_barcodes)
            cell_with_matched_barcode = matched_cell_barcodes.intersection(cell_barcodes)
            cell_with_matched_barcode_number = len(cell_with_matched_barcode)

            df_matched = df_valid_CDR3_count[df_valid_CDR3_count.barcode.isin(matched_cell_barcodes)]

            # median matched UMI
            df_matched_heavy_light = df_matched[(df_matched.aaSeqCDR3_IGH!="NA") & ((df_matched.aaSeqCDR3_IGL!="NA") | (df_matched.aaSeqCDR3_IGK!="NA"))]
            matched_cell_with_heavy_and_light = df_matched_heavy_light.shape[0]            

            cell_summary_row_list.append({"item" :  "Cell with Matched Barcode","count": cell_with_matched_barcode_number,
            "total_count": cell_number})
            cell_summary_row_list.append({"item" :  "Cell with Matched Barcode,Heavy and Light Chain","count": matched_cell_with_heavy_and_light,
            "total_count": cell_number})
            """
            df_match_clonetypes
            """
            df_matched_valid_CDR3_count = df_matched.groupby(["aaSeqCDR3_IGH","aaSeqCDR3_IGL","aaSeqCDR3_IGK"],as_index=False).agg({"barcode":"count"}).sort_values("barcode",ascending=False)
            total_matched_CDR3_barcode_number =  sum(df_matched_valid_CDR3_count.barcode)
            df_matched_valid_CDR3_count["percent"] = df_matched_valid_CDR3_count.barcode/total_matched_CDR3_barcode_number*100
            df_matched_valid_CDR3_count["percent"] = df_matched_valid_CDR3_count["percent"].apply(lambda x:round(x,2))
            df_matched_valid_CDR3_count.to_csv(matched_clonetypes_file,sep="\t",index=False) 

    # output df_valid_CDR3
    df_mergeID = pd.merge(df_valid_CDR3_count,df_clonetypes,how="left",on=cols)
    df_mergeID = df_mergeID[["barcode","clonetype_ID"]]
    df_valid_CDR3_with_ID = pd.merge(df_valid_CDR3,df_mergeID,how="left",on="barcode")
    df_valid_CDR3_with_ID.sort_values(["clonetype_ID","barcode","type"],inplace=True)
    df_valid_CDR3_with_ID.to_csv(cell_valid_CDR3_file,sep="\t",index=False)

    # summary file
    mapping_summary = pd.DataFrame(mapping_summary_row_list,columns=["item","count","total_count"])
    mapping_summary["percent"] = mapping_summary["count"]/(mapping_summary.total_count.astype("float"))*100
    mapping_summary["percent"] = mapping_summary["percent"].apply(lambda x:round(x,2))
    mapping_summary["percent_str"] = mapping_summary.apply(lambda row:"("+str(row["percent"])+"%)",axis=1)
    mapping_summary["count"] = mapping_summary["count"].apply(format_number)

    cell_summary = pd.DataFrame(cell_summary_row_list,columns=["item","count","total_count"])
    cell_summary["count"] = cell_summary["count"].apply(int)
    cell_summary["percent"] = cell_summary["count"]/(cell_summary.total_count.astype("float"))*100
    cell_summary["percent"] = cell_summary["percent"].apply(lambda x:round(x,2))
    cell_summary["count"] = cell_summary["count"].apply(format_number)

    def percent_str_func(row):
        need_percent = bool(re.search("Cell with",row["item"],flags=re.IGNORECASE))
        if need_percent:
            return "("+str(row["percent"])+"%)"
        else:
            return ""
    cell_summary["percent_str"] = cell_summary.apply(lambda row:percent_str_func(row),axis=1)
    #summary.to_csv(summary_file,sep="\t",index=False)

    # stat file
    def gen_stat(summary,stat_file):
        stat = summary
        stat["new_count"] = stat["count"].astype(str)+ stat["percent_str"]
        stat = stat.loc[:,["item","new_count"]]
        stat.to_csv(stat_file,sep=":",header=None,index=False)

    mapping_stat_file =  "{}/mapping_stat.txt".format(outdir)
    gen_stat(mapping_summary,mapping_stat_file)
    mapping_html_name = type + "_mapping"
    t = reporter(name=mapping_html_name, sample=args.sample, stat_file=mapping_stat_file, outdir=outdir + '/..')
    t.get_report()

    cell_stat_file =  "{}/cell_stat.txt".format(outdir)
    gen_stat(cell_summary,cell_stat_file)
    cell_html_name = type + "_cell"
    t = reporter(name=cell_html_name, sample=args.sample, stat_file=cell_stat_file, outdir=outdir + '/..')
    t.get_report()

    # cloneytpes table
    """
    if not (matched_dir is None):
        top10_clonetypes_df = df_matched_valid_CDR3_count.head(10)
    else:
        top10_clonetypes_df = df_clonetypes.head(10)
    """
    top10_clonetypes_df = df_clonetypes.head(10)
    top10_clonetypes_df = top10_clonetypes_df.reset_index(drop=True)
    top10_clonetypes_df.index = top10_clonetypes_df.index + 1
    top10_clonetypes_df["percent"] = top10_clonetypes_df["percent"].apply(lambda x:str(x)+"%")
    seqs = ["aaSeqCDR3"]
    cols = []
    for chain in chains:
        for seq in seqs:
            cols.append("_".join([seq,chain]))
    top10_cols = ["clonetype_ID"] + cols + ["barcode_count","percent"]
    top10_clonetypes_df = top10_clonetypes_df[top10_cols]
    top10_clonetypes_df.to_csv(top10_clonetypes_file,sep="\t",index=False)
    table_header = ["Clonetype_ID"] + cols + ["Frequency","Percent"]
    t = reporter(name="clonetypes", sample=args.sample, table_file=top10_clonetypes_file, table_header= table_header,outdir=outdir + '/..')
    t.get_report()

    # other_metrics_file
    """
    if len(other_metrics_row_list) != 0:
        other_metrics = pd.DataFrame(other_metrics_row_list,columns=["item","count"])
        other_metrics.to_csv(other_metrics_file,sep=":",header=None,index=False)
    """

    # finish
    logger1.info(f'{step} done!')  
        

def get_opts_vdj(parser,sub_program):
    if sub_program:
        parser.add_argument('--outdir', help='output dir',required=True)
        parser.add_argument('--sample', help='sample name', required=True)
        parser.add_argument("--alignments",required=True)
    parser.add_argument("--matched_dir",default=None)
    parser.add_argument("--type",required=True)
    parser.add_argument('--UMI_min', dest='UMI_min', help='minimum UMI number to filter', default="auto")
    parser.add_argument('--debug', dest='debug', default=False)
    parser.add_argument("--no_UMI_filter", action='store_true', default=False)