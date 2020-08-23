#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:44:46 2017
Copyright (C) 2017
@author: Derek Pisner (dPys)
"""
import warnings
import os
import re
import os.path as op
import indexed_gzip
import nibabel as nib
import numpy as np
import sys
import time
import logging
import threading
warnings.filterwarnings("ignore")

WATCHDOG_HARD_KILL_TIMEOUT = 90

log = logging.getLogger(__name__)


def get_file():
    """Get a file's base directory path."""
    base_path = str(__file__)
    return base_path


def checkConsecutive(l):
    n = len(l) - 1
    return sum(np.diff(sorted(l)) == 1) >= n


def prune_suffices(res):
    import re

    if "reor-RAS" in str(res):
        res = re.sub(r"_reor\-*[A-Z][A-Z][A-Z]", "", str(res))
    if "res-" in str(res):
        res = re.sub(r"_res\-*[0-4]mm", "", str(res))
    if "noreor-RAS" in str(res):
        res = re.sub(r"_noreor\-*[A-Z][A-Z][A-Z]", "", str(res))
    if "nores-" in str(res):
        res = re.sub(r"_nores\-*[0-4]mm", "", str(res))
    return res


def do_dir_path(atlas, outdir):
    """
    Creates an atlas subdirectory from the base directory of the given subject's input file.

    Parameters
    ----------
    atlas : str
        Name of atlas parcellation used.
    outdir : str
        Path to base derivatives directory.

    Returns
    -------
    dir_path : str
        Path to directory containing subject derivative data for given run.

    """
    if atlas:
        if os.path.isfile(atlas):
            atlas = os.path.basename(atlas)
        atlas = prune_suffices(atlas)
        if atlas.endswith(".nii.gz"):
            atlas = atlas.replace(".nii.gz", "")

    dir_path = f"{outdir}/{atlas}"
    if not op.exists(dir_path) and atlas is not None:
        os.makedirs(dir_path, exist_ok=True)
    elif atlas is None:
        raise ValueError("Error: cannot create directory for a null atlas!")

    return dir_path


def as_directory(dir_, remove=False, return_as_path=False):
    """
    Convenience function to make a directory while returning it.

    Parameters
    ----------
    dir_ : str, Path
        File location to directory.
    remove : bool, optional
        Whether to remove a previously existing directory, by default False

    Returns
    -------
    str
        Directory string.

    """
    import shutil
    from pathlib import Path

    p = Path(dir_).absolute()

    if remove:
        print(f"Previous directory found at {dir_}. Removing.")
        shutil.rmtree(p, ignore_errors=True)
    p.mkdir(parents=True, exist_ok=True)

    if return_as_path:
        return p

    return str(p)


def create_est_path_func(
    ID,
    network,
    conn_model,
    thr,
    roi,
    dir_path,
    node_size,
    smooth,
    thr_type,
    hpass,
    parc,
    extract_strategy,
):
    """
    Name the thresholded functional connectivity matrix file based on relevant graph-generating parameters.

    Parameters
    ----------
    ID : str
        A subject id or other unique identifier.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    conn_model : str
       Connectivity estimation model (e.g. corr for correlation, cov for covariance, sps for precision covariance,
       partcorr for partial correlation). sps type is used by default.
    thr : float
        A value, between 0 and 1, to threshold the graph using any variety of methods
        triggered through other options.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    dir_path : str
        Path to directory containing subject derivative data for given run.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's.
    smooth : int
        Smoothing width (mm fwhm) to apply to time-series when extracting signal from ROI's.
    thr_type : str
        Type of thresholding performed (e.g. prop, abs, dens, mst, disp)
    hpass : bool
        High-pass filter values (Hz) to apply to node-extracted time-series.
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    extract_strategy : str
        The name of a valid function used to reduce the time-series region extraction.

    Returns
    -------
    est_path : str
        File path to .npy file containing graph with all specified combinations of hyperparameter characteristics.

    """
    import os
    import yaml
    import pkg_resources
    import sys

    with open(
        pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
    ) as stream:
        hardcoded_params = yaml.load(stream)
        try:
            template_name = hardcoded_params["template"][0]
        except KeyError:
            print(
                "No template specified in runconfig.yaml"
            )
            sys.exit(0)
    stream.close()

    if (node_size is None) and (parc is True):
        node_size = "_parc"

    namer_dir = f"{dir_path}/graphs"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    if hpass is None:
        hpass = 0

    if smooth is None:
        smooth = 0

    est_path = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir,
                                                         "/graph_sub-",
                                                         ID,
                                                         "_modality-func_",
                                                         "%s" % ("%s%s%s" % ("rsn-",
                                                                             network,
                                                                             "_") if network is not None else ""),
                                                         "%s" % ("%s%s%s" % ("roi-",
                                                                             op.basename(roi).split(".")[0],
                                                                             "_") if roi is not None else ""),
                                                         "model-",
                                                         conn_model,
                                                         "_template-",
                                                         template_name,
                                                         "_",
                                                         "%s" % ("%s%s%s" % ("nodetype-spheres-",
                                                                             node_size,
                                                                             "mm_") if (
                                                             (node_size != "parc") and (
                                                                 node_size is not None)) else "nodetype-parc_"),
                                                         "%s" % ("%s%s%s" % ("smooth-",
                                                                             smooth,
                                                                             "fwhm_") if float(smooth) > 0 else ""),
                                                         "%s" % ("%s%s%s" % ("hpass-",
                                                                             hpass,
                                                                             "Hz_") if hpass is not None else ""),
                                                         "%s" % ("%s%s%s" % ("extract-",
                                                                             extract_strategy,
                                                                             "_") if extract_strategy is not None else ""),
                                                         "thrtype-",
                                                         thr_type,
                                                         "_thr-",
                                                         thr,
                                                         ".npy",
                                                         )

    return est_path


def create_est_path_diff(
    ID,
    network,
    conn_model,
    thr,
    roi,
    dir_path,
    node_size,
    target_samples,
    track_type,
    thr_type,
    parc,
    directget,
    min_length,
    error_margin,
):
    """
    Name the thresholded structural connectivity matrix file based on relevant graph-generating parameters.

    Parameters
    ----------
    ID : str
        A subject id or other unique identifier.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    conn_model : str
       Connectivity estimation model (e.g. corr for correlation, cov for covariance, sps for precision covariance,
       partcorr for partial correlation). sps type is used by default.
    thr : float
        A value, between 0 and 1, to threshold the graph using any variety of methods
        triggered through other options.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    dir_path : str
        Path to directory containing subject derivative data for given run.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's.
    target_samples : int
        Total number of streamline samples specified to generate streams.
    track_type : str
        Tracking algorithm used (e.g. 'local' or 'particle').
    thr_type : str
        Type of thresholding performed (e.g. prop, abs, dens, mst, disp)
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    directget : str
        The statistical approach to tracking. Options are: det (deterministic), closest (clos), boot (bootstrapped),
        and prob (probabilistic).
    min_length : int
        Minimum fiber length threshold in mm to restrict tracking.

    Returns
    -------
    est_path : str
        File path to .npy file containing graph with thresholding applied.

    """
    import os
    import yaml
    import pkg_resources
    import sys

    with open(
        pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
    ) as stream:
        hardcoded_params = yaml.load(stream)
        try:
            template_name = hardcoded_params["template"][0]
        except KeyError:
            print(
                "No template specified in runconfig.yaml"
            )
            sys.exit(0)
    stream.close()

    if (node_size is None) and (parc is True):
        node_size = "parc"

    namer_dir = f"{dir_path}/graphs"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    est_path = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir,
                                                                 "/graph_sub-",
                                                                 ID,
                                                                 "_modality-dwi_",
                                                                 "%s" % ("%s%s%s" % ("rsn-",
                                                                                     network,
                                                                                     "_") if network is not None else ""),
                                                                 "%s" % ("%s%s%s" % ("roi-",
                                                                                     op.basename(roi).split(".")[0],
                                                                                     "_") if roi is not None else ""),
                                                                 "model-",
                                                                 conn_model,
                                                                 "_template-",
                                                                 template_name,
                                                                 "_",
                                                                 "%s" % ("%s%s%s" % ("nodetype-spheres-",
                                                                                     node_size,
                                                                                     "mm_") if (
                                                                     (node_size != "parc") and (
                                                                         node_size is not None)) else "nodetype-parc_"),
                                                                 "%s" % ("%s%s%s" % ("samples-",
                                                                                     int(target_samples),
                                                                                     "streams_") if float(target_samples) > 0 else "_"),
                                                                 "tracktype-",
                                                                 track_type,
                                                                 "_directget-",
                                                                 directget,
                                                                 "_minlength-",
                                                                 min_length,
                                                                 "_tol-",
                                                                 error_margin,
                                                                 "_thrtype-",
                                                                 thr_type,
                                                                 "_thr-",
                                                                 thr,
                                                                 ".npy",
                                                                 )
    return est_path


def create_raw_path_func(
    ID,
    network,
    conn_model,
    roi,
    dir_path,
    node_size,
    smooth,
    hpass,
    parc,
    extract_strategy,
):
    """
    Name the raw functional connectivity matrix file based on relevant graph-generating parameters.

    Parameters
    ----------
    ID : str
        A subject id or other unique identifier.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    conn_model : str
       Connectivity estimation model (e.g. corr for correlation, cov for covariance, sps for precision covariance,
       partcorr for partial correlation). sps type is used by default.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    dir_path : str
        Path to directory containing subject derivative data for given run.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's.
    smooth : int
        Smoothing width (mm fwhm) to apply to time-series when extracting signal from ROI's.
    hpass : bool
        High-pass filter values (Hz) to apply to node-extracted time-series.
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    extract_strategy : str
        The name of a valid function used to reduce the time-series region extraction.

    Returns
    -------
    est_path : str
        File path to .npy file containing graph with all specified combinations of hyperparameter characteristics.

    """
    import os
    import yaml
    import pkg_resources
    import sys

    with open(
        pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
    ) as stream:
        hardcoded_params = yaml.load(stream)
        try:
            template_name = hardcoded_params["template"][0]
        except KeyError:
            print(
                "No template specified in runconfig.yaml"
            )
            sys.exit(0)
    stream.close()

    if (node_size is None) and (parc is True):
        node_size = "parc"

    namer_dir = f"{dir_path}/graphs"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    if hpass is None:
        hpass = 0

    if smooth is None:
        smooth = 0

    est_path = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir,
                                                 "/rawgraph_sub-",
                                                 ID,
                                                 "_modality-func_",
                                                 "%s" % ("%s%s%s" % ("rsn-",
                                                                     network,
                                                                     "_") if network is not None else ""),
                                                 "%s" % ("%s%s%s" % ("roi-",
                                                                     op.basename(roi).split(".")[0],
                                                                     "_") if roi is not None else ""),
                                                 "model-",
                                                 conn_model,
                                                 "_template-",
                                                 template_name,
                                                 "_",
                                                 "%s" % ("%s%s%s" % ("nodetype-spheres-",
                                                                     node_size,
                                                                     "mm_") if (
                                                     (node_size != "parc") and (
                                                         node_size is not None)) else "nodetype-parc_"),
                                                 "%s" % ("%s%s%s" % ("smooth-",
                                                                     smooth,
                                                                     "fwhm_") if float(smooth) > 0 else ""),
                                                 "%s" % ("%s%s%s" % ("hpass-",
                                                                     hpass,
                                                                     "Hz_") if hpass is not None else ""),
                                                 "%s" % ("%s%s" % ("extract-",
                                                                     extract_strategy) if extract_strategy is not None else ""),
                                                 ".npy",
                                                 )

    return est_path


def create_raw_path_diff(
    ID,
    network,
    conn_model,
    roi,
    dir_path,
    node_size,
    target_samples,
    track_type,
    parc,
    directget,
    min_length,
    error_margin
):
    """
    Name the raw structural connectivity matrix file based on relevant graph-generating parameters.

    Parameters
    ----------
    ID : str
        A subject id or other unique identifier.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    conn_model : str
       Connectivity estimation model (e.g. corr for correlation, cov for covariance, sps for precision covariance,
       partcorr for partial correlation). sps type is used by default.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    dir_path : str
        Path to directory containing subject derivative data for given run.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's.
    target_samples : int
        Total number of streamline samples specified to generate streams.
    track_type : str
        Tracking algorithm used (e.g. 'local' or 'particle').
    parc : bool
        Indicates whether to use parcels instead of coordinates as ROI nodes.
    directget : str
        The statistical approach to tracking. Options are: det (deterministic), closest (clos), boot (bootstrapped),
        and prob (probabilistic).
    min_length : int
        Minimum fiber length threshold in mm to restrict tracking.

    Returns
    -------
    est_path : str
        File path to .npy file containing graph with thresholding applied.

    """
    import os
    import yaml
    import pkg_resources
    import sys

    with open(
        pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
    ) as stream:
        hardcoded_params = yaml.load(stream)
        try:
            template_name = hardcoded_params["template"][0]
        except KeyError:
            print(
                "No template specified in runconfig.yaml"
            )
            sys.exit(0)
    stream.close()

    if (node_size is None) and (parc is True):
        node_size = "_parc"

    namer_dir = f"{dir_path}/graphs"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    est_path = "%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir,
                                                         "/rawgraph_sub-",
                                                         ID,
                                                         "_modality-dwi_",
                                                         "%s" % ("%s%s%s" % ("rsn-",
                                                                             network,
                                                                             "_") if network is not None else ""),
                                                         "%s" % ("%s%s%s" % ("roi-",
                                                                             op.basename(roi).split(".")[0],
                                                                             "_") if roi is not None else ""),
                                                         "model-",
                                                         conn_model,
                                                         "_template-",
                                                         template_name,
                                                         "_",
                                                         "%s" % ("%s%s%s" % ("nodetype-spheres-",
                                                                             node_size,
                                                                             "mm_") if (
                                                             (node_size != "parc") and (
                                                                 node_size is not None)) else "nodetype-parc_"),
                                                         "%s" % ("%s%s%s" % ("samples-",
                                                                             int(target_samples),
                                                                             "streams_") if float(target_samples) > 0 else ""),
                                                         "tracktype-",
                                                         track_type,
                                                         "_directget-",
                                                         directget,
                                                         "_minlength-",
                                                         min_length,
                                                         "_tol-",
                                                         error_margin,
                                                         ".npy",
                                                         )
    return est_path


def create_csv_path(dir_path, est_path):
    """

    Create a csv path to save graph metrics.

    Parameters
    ----------
    dir_path : str
        Path to directory containing subject derivative data for given run.
    est_path : str
        File path to .npy file containing graph with thresholding applied.

    Returns
    -------
    out_path : str
        File path to .csv with graph metrics.

    """
    import os
    from pathlib import Path

    namer_dir = f"{str(Path(dir_path).parent)}/topology"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    out_path = f"{namer_dir}/metrics_{est_path.split('/')[-1].split('.npy')[0]}.csv"

    return out_path


def load_mat(est_path):
    """
    Load an adjacency matrix using any of a variety of methods.

    Parameters
    ----------
    est_path : str
        File path to .npy file containing graph with thresholding applied.
    """
    import numpy as np
    import networkx as nx
    import os.path as op

    fmt = op.splitext(est_path)[1]

    if fmt == ".edgelist_csv" or fmt == ".csv":
        with open(est_path, "rb") as stream:
            G = nx.read_weighted_edgelist(stream, delimiter=",")
        stream.close()
    elif fmt == ".edgelist_ssv" or fmt == ".ssv":
        with open(est_path, "rb") as stream:
            G = nx.read_weighted_edgelist(stream, delimiter=" ")
        stream.close()
    elif fmt == ".edgelist_tsv" or fmt == ".tsv":
        with open(est_path, "rb") as stream:
            G = nx.read_weighted_edgelist(stream, delimiter="\t")
    elif fmt == ".gpickle":
        G = nx.read_gpickle(est_path)
    elif fmt == ".graphml":
        G = nx.read_graphml(est_path)
    elif fmt == ".txt":
        G = nx.from_numpy_array(np.genfromtxt(est_path))
    elif fmt == ".npy":
        G = nx.from_numpy_array(np.load(est_path))
    else:
        raise ValueError("\nERROR: File format not supported!")

    G.graph["ecount"] = nx.number_of_edges(G)
    G = nx.convert_node_labels_to_integers(G, first_label=1)

    return nx.to_numpy_matrix(G, weight="weight")


def load_mat_ext(
    est_path,
    ID,
    network,
    conn_model,
    roi,
    prune,
    norm,
    binary,
    min_span_tree,
    dens_thresh,
    disp_filt,
):
    from pynets.core.utils import load_mat

    conn_matrix = load_mat(est_path)
    return (
        conn_matrix,
        est_path,
        ID,
        network,
        conn_model,
        roi,
        prune,
        norm,
        binary,
        min_span_tree,
        dens_thresh,
        disp_filt,
    )


def save_mat(conn_matrix, est_path, fmt=None):
    """
    Save an adjacency matrix using any of a variety of methods.

    Parameters
    ----------
    conn_matrix : array
        Adjacency matrix stored as an m x n array of nodes and edges.
    est_path : str
        File path to .npy file containing graph.
    fmt : str
        Format to save connectivity matrix/graph (e.g. .npy, .pkl, .graphml,
         .txt, .ssv, .csv).

    """
    import numpy as np
    import networkx as nx
    import pkg_resources
    import yaml

    if fmt is None:
        with open(
            pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
        ) as stream:
            hardcoded_params = yaml.load(stream)
            fmt = hardcoded_params["graph_file_format"][0]
        stream.close()

    G = nx.from_numpy_array(conn_matrix)
    G.graph["ecount"] = nx.number_of_edges(G)
    G = nx.convert_node_labels_to_integers(G, first_label=1)
    if fmt == "edgelist_csv":
        nx.write_weighted_edgelist(
            G, f"{est_path.split('.npy')[0]}.csv", encoding="utf-8"
        )
    elif fmt == "gpickle":
        nx.write_gpickle(G, f"{est_path.split('.npy')[0]}.pkl")
    elif fmt == "graphml":
        nx.write_graphml(G, f"{est_path.split('.npy')[0]}.graphml")
    elif fmt == "txt":
        np.savetxt(
            f"{est_path.split('.npy')[0]}{'.txt'}",
            nx.to_numpy_matrix(G))
    elif fmt == "npy":
        np.save(est_path, nx.to_numpy_matrix(G))
    elif fmt == "edgelist_ssv":
        nx.write_weighted_edgelist(
            G,
            f"{est_path.split('.npy')[0]}.ssv",
            delimiter=" ",
            encoding="utf-8")
    else:
        raise ValueError("\nERROR: File format not supported!")

    return


def save_mat_thresholded(
    conn_matrix,
    est_path_orig,
    thr_type,
    ID,
    network,
    thr,
    conn_model,
    roi,
    prune,
    norm,
    binary,
):
    from pynets.core.utils import save_mat
    from nipype.utils.filemanip import fname_presuffix

    est_path = fname_presuffix(est_path_orig,
                               suffix=f"_thrtype-{thr_type}_thr-{thr}")
    save_mat(conn_matrix, est_path, fmt="npy")

    return est_path, ID, network, thr, conn_model, roi, prune, norm, binary


def pass_meta_outs(
    conn_model_iterlist,
    est_path_iterlist,
    network_iterlist,
    thr_iterlist,
    prune_iterlist,
    ID_iterlist,
    roi_iterlist,
    norm_iterlist,
    binary_iterlist,
):
    """
    Passes lists of iterable parameters as metadata.

    Parameters
    ----------
    conn_model_iterlist : list
       List of connectivity estimation model parameters (e.g. corr for correlation, cov for covariance,
       sps for precision covariance, partcorr for partial correlation). sps type is used by default.
    est_path_iterlist : list
        List of file paths to .npy file containing graph with thresholding applied.
    network_iterlist : list
        List of resting-state networks based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the
        study of brain subgraphs.
    thr_iterlist : list
        List of values, between 0 and 1, to threshold the graph using any variety of methods
        triggered through other options.
    prune_iterlist : list
        List of booleans indicating whether final graphs were pruned of disconnected nodes/isolates.
    ID_iterlist : list
        List of repeated subject id strings.
    roi_iterlist : list
        List of file paths to binarized/boolean region-of-interest Nifti1Image files.
    norm_iterlist : list
        Indicates method of normalizing resulting graph.
    binary_iterlist : list
        List of booleans indicating whether resulting graph edges to form an unweighted graph were binarized.

    Returns
    -------
    conn_model_iterlist : list
       List of connectivity estimation model parameters (e.g. corr for correlation, cov for covariance,
       sps for precision covariance, partcorr for partial correlation). sps type is used by default.
    est_path_iterlist : list
        List of file paths to .npy file containing graph with thresholding applied.
    network_iterlist : list
        List of resting-state networks based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the
        study of brain subgraphs.
    thr_iterlist : list
        List of values, between 0 and 1, to threshold the graph using any variety of methods
        triggered through other options.
    prune_iterlist : list
        List of booleans indicating whether final graphs were pruned of disconnected nodes/isolates.
    ID_iterlist : list
        List of repeated subject id strings.
    roi_iterlist : list
        List of file paths to binarized/boolean region-of-interest Nifti1Image files.
    norm_iterlist : list
        Indicates method of normalizing resulting graph.
    binary_iterlist : list
        List of booleans indicating whether resulting graph edges to form an unweighted graph were binarized.
    embed_iterlist : list
        List of booleans indicating whether omnibus embedding of graph population was performed.
    multimodal_iterlist : list
        List of booleans indicating whether multiple modalities of input data have been specified.

    """

    return (
        conn_model_iterlist,
        est_path_iterlist,
        network_iterlist,
        thr_iterlist,
        prune_iterlist,
        ID_iterlist,
        roi_iterlist,
        norm_iterlist,
        binary_iterlist,
    )


def pass_meta_ins(
        conn_model,
        est_path,
        network,
        thr,
        prune,
        ID,
        roi,
        norm,
        binary):
    """
    Passes parameters as metadata.

    Parameters
    ----------
    conn_model : str
       Connectivity estimation model (e.g. corr for correlation, cov for covariance, sps for precision covariance,
       partcorr for partial correlation). sps type is used by default.
    est_path : str
        File path to .npy file containing graph with thresholding applied.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    thr : float
        A value, between 0 and 1, to threshold the graph using any variety of methods
        triggered through other options.
    prune : bool
        Indicates whether to prune final graph of disconnected nodes/isolates.
    ID : str
        A subject id or other unique identifier.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    norm : int
        Indicates method of normalizing resulting graph.
    binary : bool
        Indicates whether to binarize resulting graph edges to form an
        unweighted graph.

    Returns
    -------
    conn_model : str
       Connectivity estimation model (e.g. corr for correlation, cov for covariance, sps for precision covariance,
       partcorr for partial correlation). sps type is used by default.
    est_path : str
        File path to .npy file containing graph with thresholding applied.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    thr : float
        A value, between 0 and 1, to threshold the graph using any variety of methods
        triggered through other options.
    prune : bool
        Indicates whether to prune final graph of disconnected nodes/isolates.
    ID : str
        A subject id or other unique identifier.
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    norm : int
        Indicates method of normalizing resulting graph.
    binary : bool
        Indicates whether to binarize resulting graph edges to form an
        unweighted graph.

    """
    est_path_iterlist = est_path
    conn_model_iterlist = conn_model
    network_iterlist = network
    thr_iterlist = thr
    prune_iterlist = prune
    ID_iterlist = ID
    roi_iterlist = roi
    norm_iterlist = norm
    binary_iterlist = binary
    # print('\n\nParam-iters:\n')
    # print(conn_model_iterlist)
    # print(est_path_iterlist)
    # print(network_iterlist)
    # print(thr_iterlist)
    # print(prune_iterlist)
    # print(ID_iterlist)
    # print(roi_iterlist)
    # print(norm_iterlist)
    # print(binary_iterlist)
    # print('\n\n')
    return (
        conn_model_iterlist,
        est_path_iterlist,
        network_iterlist,
        thr_iterlist,
        prune_iterlist,
        ID_iterlist,
        roi_iterlist,
        norm_iterlist,
        binary_iterlist,
    )


def pass_meta_ins_multi(
    conn_model_func,
    est_path_func,
    network_func,
    thr_func,
    prune_func,
    ID_func,
    roi_func,
    norm_func,
    binary_func,
    conn_model_struct,
    est_path_struct,
    network_struct,
    thr_struct,
    prune_struct,
    ID_struct,
    roi_struct,
    norm_struct,
    binary_struct,
):
    """
    Passes multimodal iterable parameters as metadata.

    Parameters
    ----------
    conn_model_func : str
       Functional connectivity estimation model (e.g. corr for correlation, cov for covariance, sps for precision
       covariance, partcorr for partial correlation). sps type is used by default.
    est_path_func : str
        File path to .npy file containing functional graph with thresholding applied.
    network_func : str
        Functional resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the
        study of brain subgraphs.
    thr_func : float
        A value, between 0 and 1, to threshold the functional graph using any variety of methods
        triggered through other options.
    prune_func : bool
        Indicates whether to prune final functional graph of disconnected nodes/isolates.
    ID_func : str
        A subject id or other unique identifier for the functional workflow.
    roi_func : str
        File path to binarized/boolean region-of-interest Nifti1Image file applied to the functional data.
    norm_func : int
        Indicates method of normalizing resulting functional graph.
    binary_func : bool
        Indicates whether to binarize resulting graph edges to form an unweighted functional graph.
    conn_model_struct : str
       Diffusion structural connectivity estimation model (e.g. corr for correlation, cov for covariance,
       sps for precision covariance, partcorr for partial correlation). sps type is used by default.
    est_path_struct : str
        File path to .npy file containing diffusion structural graph with thresholding applied.
    network_struct : str
        Diffusion structural resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter
        nodes in the study of brain subgraphs.
    thr_struct : float
        A value, between 0 and 1, to threshold the diffusion structural graph using any variety of methods
        triggered through other options.
    prune_struct : bool
        Indicates whether to prune final diffusion structural graph of disconnected nodes/isolates.
    ID_struct : str
        A subject id or other unique identifier for the diffusion structural workflow.
    roi_struct : str
        File path to binarized/boolean region-of-interest Nifti1Image file applied too the dwi data.
    norm_struct : int
        Indicates method of normalizing resulting diffusion structural graph.
    binary_struct : bool
        Indicates whether to binarize resulting diffusion structural graph edges to form an unweighted graph.


    Returns
    -------
    conn_model_iterlist : list
       List of connectivity estimation model parameters (e.g. corr for correlation, cov for covariance,
       sps for precision covariance, partcorr for partial correlation). sps type is used by default.
    est_path_iterlist : list
        List of file paths to .npy file containing graph with thresholding applied.
    network_iterlist : list
        List of resting-state networks based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the
        study of brain subgraphs.
    thr_iterlist : list
        List of values, between 0 and 1, to threshold the graph using any variety of methods
        triggered through other options.
    prune_iterlist : list
        List of booleans indicating whether final graphs were pruned of disconnected nodes/isolates.
    ID_iterlist : list
        List of repeated subject id strings.
    roi_iterlist : list
        List of file paths to binarized/boolean region-of-interest Nifti1Image files.
    norm_iterlist : list
        Indicates method of normalizing resulting graph.
    binary_iterlist : list
        List of booleans indicating whether resulting graph edges to form an unweighted graph were binarized.
    embed_iterlist : list
        List of booleans indicating whether omnibus embedding of graph population was performed.
    multimodal_iterlist : list
        List of booleans indicating whether multiple modalities of input data have been specified.

    """
    est_path_iterlist = [est_path_func, est_path_struct]
    conn_model_iterlist = [conn_model_func, conn_model_struct]
    network_iterlist = [network_func, network_struct]
    thr_iterlist = [thr_func, thr_struct]
    prune_iterlist = [prune_func, prune_struct]
    ID_iterlist = [ID_func, ID_struct]
    roi_iterlist = [roi_func, roi_struct]
    norm_iterlist = [norm_func, norm_struct]
    binary_iterlist = [binary_func, binary_struct]
    # print('\n\nParam-iters:\n')
    # print(conn_model_iterlist)
    # print(est_path_iterlist)
    # print(network_iterlist)
    # print(thr_iterlist)
    # print(prune_iterlist)
    # print(ID_iterlist)
    # print(roi_iterlist)
    # print(norm_iterlist)
    # print(binary_iterlist)
    # print('\n\n')
    return (
        conn_model_iterlist,
        est_path_iterlist,
        network_iterlist,
        thr_iterlist,
        prune_iterlist,
        ID_iterlist,
        roi_iterlist,
        norm_iterlist,
        binary_iterlist,
    )


def collectpandasjoin(net_mets_csv):
    """
    Passes csv pandas dataframe as metadata.

    Parameters
    ----------
    net_mets_csv : str
        File path to csv pandas dataframe.

    Returns
    -------
    net_mets_csv_out : str
        File path to csv pandas dataframe as itself.

    """
    net_mets_csv_out = net_mets_csv
    return net_mets_csv_out


def flatten(l):
    """
    Flatten list of lists.
    """
    import collections

    for el in l:
        if isinstance(
                el, collections.Iterable) and not isinstance(
                el, (str, bytes)):
            for ell in flatten(el):
                yield ell
        else:
            yield el


def decompress_nifti(infile):
    from nipype.utils.filemanip import split_filename
    import gzip
    import os
    import shutil

    _, base, ext = split_filename(infile)

    if ext[-3:].lower() == ".gz":
        ext = ext[:-3]

    with gzip.open(infile, "rb") as in_file:
        with open(os.path.abspath(base + ext), "wb") as out_file:
            shutil.copyfileobj(in_file, out_file, 128*1024)
        out_file.close()
    in_file.close()

    os.remove(infile)
    return out_file.name


def proportional(k, voxels_list):
    """Hagenbach-Bischoff Quota"""
    quota = sum(voxels_list) / (1.0 + k)
    frac = [voxels / quota for voxels in voxels_list]
    res = [int(f) for f in frac]
    n = k - sum(res)
    if n == 0:
        return res
    if n < 0:
        return [min(x, k) for x in res]
    remainders = [ai - bi for ai, bi in zip(frac, res)]
    limit = sorted(remainders, reverse=True)[n - 1]
    for i, r in enumerate(remainders):
        if r >= limit:
            res[i] += 1
            n -= 1
            if n == 0:
                return res


def collect_pandas_df(
    network, ID, net_mets_csv_list, plot_switch, multi_nets, multimodal
):
    """
    API for summarizing independent lists of pickled pandas dataframes of
     graph metrics for each modality, RSN, and roi.

    Parameters
    ----------
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming
        (e.g. 'Default') used to filter nodes in the study of brain subgraphs.
    ID : str
        A subject id or other unique identifier.
    net_mets_csv_list : list
        List of file paths to pickled pandas dataframes as themselves.
    plot_switch : bool
        Activate summary plotting (histograms, ROC curves, etc.)
    multi_nets : list
        List of Yeo RSN's specified in workflow(s).
    multimodal : bool
        Indicates whether multiple modalities of input data have been
        specified.

    Returns
    -------
    combination_complete : bool
        If True, then collect_pandas_df completed successfully.

    """
    import yaml
    import pkg_resources
    from pathlib import Path
    from pynets.core.utils import flatten
    from pynets.stats.netstats import collect_pandas_df_make

    # Available functional and structural connectivity models
    with open(
        pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
    ) as stream:
        hardcoded_params = yaml.load(stream)
        try:
            func_models = hardcoded_params["available_models"]["func_models"]
        except KeyError:
            print(
                "ERROR: available functional models not sucessfully extracted"
                " from runconfig.yaml"
            )
        try:
            struct_models = hardcoded_params["available_models"][
                "struct_models"]
        except KeyError:
            print(
                "ERROR: available structural models not sucessfully extracted"
                " from runconfig.yaml"
            )

    net_mets_csv_list = list(flatten(net_mets_csv_list))

    if multi_nets is not None:
        net_mets_csv_list_nets = net_mets_csv_list
        for network in multi_nets:
            net_mets_csv_list = list(
                set([i for i in net_mets_csv_list_nets if network in i])
            )
            if multimodal is True:
                net_mets_csv_list_dwi = list(
                    set(
                        [
                            i
                            for i in net_mets_csv_list
                            if i.split("model-")[1].split("_")[0] in
                               struct_models
                        ]
                    )
                )
                combination_complete_dwi = collect_pandas_df_make(
                    net_mets_csv_list_dwi, ID, network, plot_switch
                )
                net_mets_csv_list_func = list(
                    set(
                        [
                            i
                            for i in net_mets_csv_list
                            if i.split("model-")[1].split("_")[0] in
                               func_models
                        ]
                    )
                )
                combination_complete_func = collect_pandas_df_make(
                    net_mets_csv_list_func, ID, network, plot_switch
                )

                if (
                    combination_complete_dwi is True
                    and combination_complete_func is True
                ):
                    combination_complete = True
                else:
                    combination_complete = False
            else:
                combination_complete = collect_pandas_df_make(
                    net_mets_csv_list, ID, network, plot_switch
                )
    else:
        if multimodal is True:
            net_mets_csv_list_dwi = list(
                set(
                    [
                        i
                        for i in net_mets_csv_list
                        if i.split("model-")[1].split("_")[0] in struct_models
                    ]
                )
            )
            combination_complete_dwi = collect_pandas_df_make(
                net_mets_csv_list_dwi, ID, network, plot_switch
            )
            net_mets_csv_list_func = list(
                set(
                    [
                        i
                        for i in net_mets_csv_list
                        if i.split("model-")[1].split("_")[0] in func_models
                    ]
                )
            )
            combination_complete_func = collect_pandas_df_make(
                net_mets_csv_list_func, ID, network, plot_switch
            )

            if combination_complete_dwi is \
                True and combination_complete_func is True:
                combination_complete = True
            else:
                combination_complete = False
        else:
            combination_complete = collect_pandas_df_make(
                net_mets_csv_list, ID, network, plot_switch
            )

    return combination_complete


def check_est_path_existence(est_path_list):
    """
    Checks for the existence of each graph estimated and saved to disk.

    Parameters
    ----------
    est_path_list : list
        List of file paths to .npy file containing graph with thresholding applied.
    Returns
    -------
    est_path_list_ex : list
        List of existing file paths to .npy file containing graph with thresholding applied.
    bad_ixs : int
        List of indices in est_path_list with non-existent and/or corrupt files.

    """
    est_path_list_ex = []
    bad_ixs = []
    i = -1

    for est_path in est_path_list:
        i = i + 1
        if op.isfile(est_path) is True:
            est_path_list_ex.append(est_path)
        else:
            print(f"\n\nWarning: Missing {est_path}...\n\n")
            bad_ixs.append(i)
            continue
    return est_path_list_ex, bad_ixs


def save_coords_and_labels_to_pickle(coords, labels, dir_path, network):
    """
    Save coordinates and labels to pickle files.

    Parameters
    ----------
    coords : list
        List of (x, y, z) tuples corresponding to a coordinate atlas used or
        which represent the center-of-mass of each parcellation node.
    labels : list
        List of string labels corresponding to ROI nodes.
    dir_path : str
        Path to directory containing subject derivative data for given run.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.

    Returns
    -------
    coord_path : str
        Path to pickled coordinates list.
    labels_path : str
        Path to pickled labels list.

    """
    import pickle
    import os

    namer_dir = f"{dir_path}/nodes"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    if network is not None:
        coord_path = f"{namer_dir}{'/'}{network}{'_mni_coords_rsn.pkl'}"
        labels_path = f"{namer_dir}{'/'}{network}{'_mni_labels_rsn.pkl'}"
    else:
        coord_path = f"{namer_dir}/all_mni_coords.pkl"
        labels_path = f"{namer_dir}/all_mni_labels.pkl"

    # Save coords to pickle
    with open(coord_path, "wb") as f:
        pickle.dump(coords, f, protocol=2)

    # Save labels to pickle
    with open(labels_path, "wb") as f:
        pickle.dump(labels, f, protocol=2)

    return coord_path, labels_path


def missing_elements(L):
    start, end = L[0], L[-1]
    return sorted(set(range(start, end + 1)).difference(L))


def get_template_tf(template_name, vox_size):
    from pathlib import Path
    from templateflow.api import get as get_template

    templateflow_home = Path(
        os.getenv(
            "TEMPLATEFLOW_HOME",
            os.path.join(os.getenv("HOME"), ".cache", "templateflow"),
        )
    )
    res = int(vox_size.strip("mm"))
    # str(get_template(
    # template_name, resolution=res, desc=None, suffix='T1w',
    # extension=['.nii', '.nii.gz']))

    template = str(
        get_template(
            template_name,
            resolution=res,
            desc="brain",
            suffix="T1w",
            extension=[".nii", ".nii.gz"],
        )
    )

    template_mask = str(
        get_template(
            template_name,
            resolution=res,
            desc="brain",
            suffix="mask",
            extension=[".nii", ".nii.gz"],
        )
    )

    return template, template_mask, templateflow_home


def save_nifti_parcels_map(ID, dir_path, network, net_parcels_map_nifti, vox_size):
    """
    This function takes a Nifti1Image parcellation object resulting from some form of masking and saves it to disk.

    Parameters
    ----------
    ID : str
        A subject id or other unique identifier.
    dir_path : str
        Path to directory containing subject derivative data for given run.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    net_parcels_map_nifti : Nifti1Image
        A nibabel-based nifti image consisting of a 3D array with integer voxel intensities corresponding to ROI
        membership.
    vox_size : str
        Voxel size in mm. (e.g. 2mm).

    Returns
    -------
    net_parcels_nii_path : str
        File path to Nifti1Image consisting of a 3D array with integer voxel intensities corresponding to ROI
        membership.

    """
    import os
    import yaml
    import pkg_resources
    import sys
    from nilearn.image import resample_to_img

    with open(
        pkg_resources.resource_filename("pynets", "runconfig.yaml"), "r"
    ) as stream:
        hardcoded_params = yaml.load(stream)
        try:
            template_name = hardcoded_params["template"][0]
        except KeyError:
            print(
                "No template specified in runconfig.yaml"
            )
            sys.exit(0)
    stream.close()

    namer_dir = f"{dir_path}/parcellations"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    net_parcels_nii_path = "%s%s%s%s%s" % (
        namer_dir,
        "/parcellation_space-",
        template_name,
        "%s" % ("%s%s" % ("_rsn-", network) if network is not None else ""),
        ".nii.gz",
    )

    template_brain = pkg_resources.resource_filename(
        "pynets", f"templates/{template_name}_brain_{vox_size}.nii.gz"
    )
    try:
        template_img = nib.load(template_brain)
    except indexed_gzip.ZranError as e:
        print(e,
              f"\nCannot load MNI template. Do you have git-lfs "
              f"installed?")

    net_parcels_map_nifti = resample_to_img(
        net_parcels_map_nifti, template_img, interpolation="nearest"
    )

    nib.save(net_parcels_map_nifti, net_parcels_nii_path)
    return net_parcels_nii_path


def save_ts_to_file(
    roi,
    network,
    ID,
    dir_path,
    ts_within_nodes,
    smooth,
    hpass,
    node_size,
    extract_strategy,
):
    """
    This function saves the time-series 4D numpy array to disk as a .npy file.

    Parameters
    ----------
    roi : str
        File path to binarized/boolean region-of-interest Nifti1Image file.
    network : str
        Resting-state network based on Yeo-7 and Yeo-17 naming (e.g. 'Default') used to filter nodes in the study of
        brain subgraphs.
    ID : str
        A subject id or other unique identifier.
    dir_path : str
        Path to directory containing subject derivative data for given run.
    ts_within_nodes : array
        2D m x n array consisting of the time-series signal for each ROI node where m = number of scans and
        n = number of ROI's, where ROI's are parcel volumes.
    smooth : int
        Smoothing width (mm fwhm) to apply to time-series when extracting signal from ROI's.
    hpass : bool
        High-pass filter values (Hz) to apply to node-extracted time-series.
    node_size : int
        Spherical centroid node size in the case that coordinate-based centroids
        are used as ROI's for time-series extraction.
    extract_strategy : str
        The name of a valid function used to reduce the time-series region extraction.

    Returns
    -------
    out_path_ts : str
        Path to .npy file containing array of fMRI time-series extracted from nodes.

    """
    import os

    namer_dir = f"{dir_path}/timeseries"
    if not os.path.isdir(namer_dir):
        os.makedirs(namer_dir, exist_ok=True)

    if hpass is None:
        hpass = 0

    if smooth is None:
        smooth = 0

    # Save time series as npy file
    out_path_ts = "%s%s%s%s%s%s%s%s%s%s%s" % (namer_dir,
                                              "/nodetimeseries_sub-",
                                              ID,
                                              "_",
                                              "%s" % ("%s%s%s" % ("rsn-",
                                                                  network,
                                                                  "_") if network is not None else ""),
                                              "%s" % ("%s%s%s" % ("roi-",
                                                                  op.basename(roi).split(".")[0],
                                                                  "_") if roi is not None else ""),
                                              "%s" % ("%s%s%s" % ("spheres-",
                                                                  node_size,
                                                                  "mm_") if (
                                                  (node_size != "parc") and (
                                                      node_size is not None)) else "parc_"),
                                              "%s" % ("%s%s%s" % ("smooth-",
                                                                  smooth,
                                                                  "fwhm_") if float(smooth) > 0 else ""),
                                              "%s" % ("%s%s%s" % ("hpass-",
                                                                  hpass,
                                                                  "Hz_") if hpass is not None else ""),
                                              "%s" % ("%s%s" % ("extract-",
                                                                  extract_strategy) if extract_strategy is not None else ""),
                                              ".npy",
                                              )

    np.save(out_path_ts, ts_within_nodes)
    return out_path_ts


def as_list(x):
    """
    A function to convert an item to a list if it is not, or pass
    it through otherwise.
    """
    if not isinstance(x, list):
        return [x]
    else:
        return x


def merge_dicts(x, y):
    """
    A function to merge two dictionaries, making it easier for us to make
    modality specific queries for dwi images (since they have variable
    extensions due to having an nii, bval, and bvec file).
    """
    z = x.copy()
    z.update(y)
    return z


def timeout(seconds):
    """
    Timeout function for hung calculations.
    """
    from functools import wraps
    import errno
    import os
    import signal

    class TimeoutError(Exception):
        pass

    def decorator(func):
        def _handle_timeout(signum, frame):
            error_message = os.strerror(errno.ETIME)
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


class build_sql_db(object):
    """
    A SQL exporter for AUC metrics.
    """

    def __init__(self, dir_path, ID):
        from sqlalchemy import create_engine

        self.ID = ID
        db_file = dir_path + "/" + self.ID + "_auc_db.sql"
        self.engine = create_engine(
            "sqlite:///" + db_file, echo=False, encoding="utf-8"
        )
        self.hyperparams = None
        self.modality = None
        return

    def create_modality_table(self, modality):
        from sqlalchemy.sql import text

        self.modality = modality
        statement = """CREATE TABLE IF NOT EXISTS """ + \
            self.modality + """(id TEXT);"""
        self.engine.execute(text(statement.replace("'", "")))

    def add_hp_columns(self, hyperparams):
        from sqlalchemy.sql import text

        self.hyperparams = hyperparams
        for hp in self.hyperparams:
            try:
                statement = (
                    """ALTER TABLE """
                    + self.modality
                    + """ ADD COLUMN """
                    + hp
                    + """;"""
                )
                self.engine.execute(text(statement.replace("'", "")))
            except BaseException:
                continue
        return

    def add_row_from_df(self, df_summary_auc, hyperparam_dict):
        import pandas as pd

        df_summary_auc_ext = pd.concat(
            [
                pd.DataFrame.from_dict(hyperparam_dict,
                                       orient="index").transpose(),
                df_summary_auc,
            ],
            axis=1,
        )
        df_summary_auc_ext.to_sql(
            self.modality,
            con=self.engine,
            index=False,
            chunksize=1000,
            if_exists="replace",
        )
        return


class watchdog(object):
    def run(self):
        self.shutdown = threading.Event()
        watchdog_thread = threading.Thread(target=self._watchdog,
                                           name="watchdog")
        try:
            watchdog_thread.start()
            self._run()
        finally:
            self.shutdown.set()
            watchdog_thread.join()
        return 0

    def _watchdog(self):
        self.last_progress_time = time.time()
        while True:
            if self.shutdown.wait(timeout=5):
                return
            last_progress_delay = time.time() - self.last_progress_time
            if last_progress_delay < WATCHDOG_HARD_KILL_TIMEOUT:
                continue
            try:
                stacks = self._get_thread_stack_traces()
                log.error(
                    "no progress in %0.01f seconds\n"
                    "kill -9 time...\n\n%s",
                    last_progress_delay, self.last_message,
                    "\n\n".join(stacks),
                    extra={"thread_stacks": stacks},
                )
            except:
                pass
            # Hopefully give logs some time to flush
            time.sleep(1)
            os.kill(0, 9)

    def _run(self):
        from pynets.cli.pynets_run import main
        while True:
            self.last_progress_time = time.time()
            main()
