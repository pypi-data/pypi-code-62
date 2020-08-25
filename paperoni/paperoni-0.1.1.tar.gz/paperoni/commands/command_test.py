import argparse
import json
import urllib.request
from collections import defaultdict

import requests
from coleo import Argument as Arg, default, tooled
from tqdm import tqdm

from ..config import get_config
from ..io import PapersFile, ResearchersFile
from ..papers import Papers
from ..query import QueryManager
from .searchutils import search_ext


@tooled
def command_test():

    papers = search_ext()
    for p in papers:
        print(p.type())

    # # # Microsoft Cognitive API key
    # # key: Arg & str = default(get_config("key"))

    # # qm = QueryManager(key)
    # # # res = qm.histo("And(Composite(AA.AuN=='yoshua bengio'),Y=2019)", "CC")
    # # res = qm.histo(
    # #     "And(Composite(F.FN=='artificial intelligence'),Y>2018)", "Y"
    # # )
    # # print(res)

    # # [alias: -c]
    # collection: Arg & PapersFile

    # groups = defaultdict(list)
    # for paper in collection:
    #     if "FamId" in paper.data:
    #         groups[paper.data["FamId"]].append(paper)
    #     # else:
    #     #     paper.format_term()

    # for fid, group in groups.items():
    #     if "DeepMDP" in group[0].title:
    #         for p in group:
    #             print("===", p.pid == fid)
    #             p.format_term()
    #         # break

    # # for fid, group in groups.items():
    # #     if len(group) > 1 and "DeepMDP" in group[0].title:
    # #         for p in group:
    # #             print("===", p.pid == fid)
    # #             p.format_term()
    # #         break
