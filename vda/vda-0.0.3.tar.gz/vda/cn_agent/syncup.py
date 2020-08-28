import os
from collections import namedtuple
import json

from vda.grpc import cn_agent_pb2

from vda.common.constant import Constant
from vda.common.spdk_client import SpdkError
from vda.common.name_fmt import NameFmt
from vda.common.operation_client import OperationClient
from vda.common.cn_agent_schema import CnCfgSchema


g_cn_cfg = None

GrpCtx = namedtuple("GrpCtx", [
    "grp_bdev_set",
    "raid0_bdev_set",
])


def get_grp_ctx():
    grp_ctx = GrpCtx(
        grp_bdev_set=set(),
        raid0_bdev_set=set(),
    )
    return grp_ctx


def create_grp(
        oc,
        grp_bdev_name,
        da_conf_str,
        frontend_bdev_list,
        grp_cfg,
        grp_ctx,
):
    da_conf = json.loads(da_conf_str)
    sorted_list = sorted(frontend_bdev_list, key=lambda x: x[0])
    bdev_name_list = []
    for _, bdev_name in sorted_list:
        bdev_name_list.append(bdev_name)
    stripe_size_kb = da_conf["stripe_size_kb"]
    raid0_bdev_name = NameFmt.raid0_bdev_name(grp_cfg.grp_id)
    grp_ctx.raid0_bdev_set.add(raid0_bdev_name)
    oc.create_raid0_bdev(raid0_bdev_name, bdev_name_list, stripe_size_kb)
    grp_ctx.grp_bdev_set.add(grp_bdev_name)
    oc.create_grp_bdev(grp_bdev_name, raid0_bdev_name)


def cleanup_grps(oc, grp_ctx):
    grp_bdev_prefix = NameFmt.grp_bdev_prefix()
    grp_bdev_list = oc.get_grp_bdev_list(grp_bdev_prefix)
    for grp_bdev_name in grp_bdev_list:
        if grp_bdev_name not in grp_ctx.grp_bdev_set:
            oc.delete_grp_bdev(grp_bdev_name)

    raid0_bdev_prefix = NameFmt.raid0_bdev_prefix()
    raid0_bdev_list = oc.get_raid0_bdev_list(raid0_bdev_prefix)
    for raid0_bdev_name in raid0_bdev_list:
        if raid0_bdev_name not in grp_ctx.raid0_bdev_set:
            oc.delete_raid0_bdev(raid0_bdev_name)


def do_cn_syncup(cn_cfg, spdk_client, local_store, cn_listener_conf):
    global g_cn_cfg
    if g_cn_cfg is None:
        g_cn_cfg = cn_cfg
    if g_cn_cfg.cn_id != cn_cfg.cn_id:
        reply_info = cn_agent_pb2.CnAgentReplyInfo(
            reply_code=Constant.cn_id_mismatch.reply_code,
            reply_msg=Constant.cn_id_mismatch.reply_msg,
        )
        return cn_agent_pb2.SyncupCnReply(reply_info=reply_info)
    if g_cn_cfg.version > cn_cfg.version:
        reply_info = cn_agent_pb2.CnAgentReplyInfo(
            reply_code=Constant.cn_old_version.reply_code,
            reply_msg=Constant.cn_old_version.reply_msg,
        )
        return cn_agent_pb2.SyncupCnReply(reply_info=reply_info)
    g_cn_cfg = cn_cfg
    if local_store:
        schema = CnCfgSchema()
        with open(local_store, "w") as f:
            f.wirte(schema.dumps(cn_cfg))

    oc = OperationClient(spdk_client)

    frontend_nvme_set = set()
    agg_bdev_set = set()
    da_lvs_set = set()
    exp_nqn_set = set()

    standby_nvme_set = set()

    grp_ctx = get_grp_ctx()

    oc.load_nvmfs()

    da_cntlr_info_list = []
    for da_cntlr_cfg in cn_cfg.da_cntlr_cfg_list:
        this_cntlr_cfg = None
        primary_cntlr_cfg = None
        standby_cntlr_cfg_list = []
        for cntlr_cfg in da_cntlr_cfg.cntlr_cfg_list:
            if cntlr_cfg.cntlr_id == da_cntlr_cfg.cntlr_id:
                this_cntlr_cfg = cntlr_cfg
            if cntlr_cfg.primary:
                primary_cntlr_cfg = cntlr_cfg
            else:
                standby_cntlr_cfg_list.append(cntlr_cfg)
        if this_cntlr_cfg is None:
            raise Exception("Can not find this_cntlr_cfg")
        if primary_cntlr_cfg is None:
            raise Exception("Can not find primary_cntlr_cfg")
        if this_cntlr_cfg.primary:
            # create primary
            grp_info_list = []
            grp_bdev_list = []
            for grp_cfg in da_cntlr_cfg.grp_cfg_list:
                vd_info_list = []
                frontend_bdev_list = []
                for vd_cfg in grp_cfg.vd_cfg_list:
                    backend_nqn_name = NameFmt.backend_nqn_name(vd_cfg.vd_id)
                    frontend_nvme_name = NameFmt.frontend_nvme_name(
                        vd_cfg.vd_id)
                    frontend_bdev_name = f"{frontend_nvme_name}n1"
                    frontend_nqn_name = NameFmt.frontend_nqn_name(
                        this_cntlr_cfg.cntlr_id)
                    try:
                        oc.create_frontend_nvme(
                            frontend_nvme_name=frontend_nvme_name,
                            backend_nqn_name=backend_nqn_name,
                            frontend_nqn_name=frontend_nqn_name,
                            dn_listener_conf_str=vd_cfg.dn_listener_conf,
                        )
                    except SpdkError as e:
                        vd_error = True
                        vd_error_msg = e.message
                    else:
                        vd_error = False
                        vd_error_msg = None
                    vd_info = cn_agent_pb2.VdFrontendInfo(
                        vd_id=vd_cfg.vd_id,
                        error=vd_error,
                        error_msg=vd_error_msg,
                    )
                    vd_info_list.append(vd_info)
                    frontend_nvme_set.add(frontend_nvme_name)
                    frontend_bdev_list.append(
                        (vd_cfg.vd_idx, frontend_bdev_name))
                grp_bdev_name = NameFmt.grp_bdev_name(grp_cfg.grp_id)
                try:
                    create_grp(
                        oc=oc,
                        grp_bdev_name=grp_bdev_name,
                        da_conf_str=da_cntlr_cfg.da_conf,
                        frontend_bdev_list=frontend_bdev_list,
                        grp_cfg=grp_cfg,
                        grp_ctx=grp_ctx,
                    )
                except SpdkError as e:
                    grp_error = True
                    grp_error_msg = e.message
                else:
                    grp_error = False
                    grp_error_msg = None
                grp_info = cn_agent_pb2.GrpInfo(
                    grp_id=grp_cfg.grp_id,
                    error=grp_error,
                    error_msg=grp_error_msg,
                    vd_info_list=vd_info_list,
                )
                grp_info_list.append(grp_info)
                grp_bdev_list.append((grp_cfg.grp_idx, grp_bdev_name))
            da_details = None
            agg_bdev_name = NameFmt.agg_bdev_name(da_cntlr_cfg.da_id)
            da_lvs_name = NameFmt.da_lvs_name(da_cntlr_cfg.da_id)
            try:
                oc.create_agg_bdev(agg_bdev_name, grp_bdev_list)
                oc.examine_bdev(agg_bdev_name)
                oc.create_da_lvs(da_lvs_name, agg_bdev_name)
                main_snap_name = NameFmt.main_snap_name(da_cntlr_cfg.da_id)
                oc.create_main_snap(
                    da_lvs_name, main_snap_name, da_cntlr_cfg.da_size)
                da_details = oc.get_da_details(da_lvs_name)
            except SpdkError as e:
                da_cntlr_error = True
                da_cntlr_error_msg = e.message
            else:
                da_cntlr_error = False
                da_cntlr_error_msg = None
            agg_bdev_set.add(agg_bdev_name)
            da_lvs_set.add(da_lvs_name)
            exp_info_list = []
            standby_nqn_list = []
            for cntlr_cfg in standby_cntlr_cfg_list:
                standby_nqn_name = NameFmt.standby_nqn_name(
                    cntlr_cfg.cntlr_id)
                standby_nqn_list.append(standby_nqn_name)
            for exp_cfg in da_cntlr_cfg.exp_cfg_list:
                exp_nqn_name = NameFmt.exp_nqn_name(
                    da_cntlr_cfg.da_name,
                    exp_cfg.exp_name,
                )
                snap_full_name = NameFmt.snap_full_name(
                    da_id=da_cntlr_cfg.da_id,
                    snap_name=exp_cfg.snap_name,
                )
                try:
                    oc.create_exp_primary_nvmf(
                        exp_nqn_name=exp_nqn_name,
                        snap_full_name=snap_full_name,
                        initiator_nqn=exp_cfg.initiator_nqn,
                        standby_nqn_list=standby_nqn_list,
                        cn_listener_conf=cn_listener_conf,
                    )
                except SpdkError as e:
                    exp_error = True
                    exp_error_msg = e.message
                else:
                    exp_error = False
                    exp_error_msg = None
                exp_info = cn_agent_pb2.ExpInfo(
                    exp_id=exp_cfg.exp_id,
                    error=exp_error,
                    error_msg=exp_error_msg,
                )
                exp_info_list.append(exp_info)
                exp_nqn_set.add(exp_nqn_name)
            da_cntlr_info = cn_agent_pb2.DaCntlrInfo(
                da_id=da_cntlr_cfg.da_id,
                cntlr_id=da_cntlr_cfg.cntlr_id,
                da_details=da_details,
                error=da_cntlr_error,
                error_msg=da_cntlr_error_msg,
                grp_info_list=grp_info_list,
                exp_info_list=exp_info_list,
            )
            da_cntlr_info_list.append(da_cntlr_info)
        else:
            # create standby
            exp_info_list = []
            for exp_cfg in da_cntlr_cfg.exp_cfg_list:
                standby_nvme_name = NameFmt.standby_nvme_name(
                    primary_cntlr_cfg.cntlr_id,
                )
                standby_bdev_name = f"{standby_nvme_name}n1"
                exp_nqn_name = NameFmt.exp_nqn_name(
                    da_cntlr_cfg.da_name,
                    exp_cfg.exp_name,
                )
                standby_nqn_name = NameFmt.standby_nqn_name(
                    this_cntlr_cfg.cntlr_id)
                try:
                    oc.create_standby_nvme(
                        standby_nvme_name,
                        exp_nqn_name,
                        standby_nqn_name,
                        primary_cntlr_cfg.cn_listener_conf,
                    )
                    oc.create_exp_standby_nvmf(
                        exp_nqn_name=exp_nqn_name,
                        standby_bdev_name=standby_bdev_name,
                        initiator_nqn=exp_cfg.initiator_nqn,
                        cn_listener_conf=cn_listener_conf,
                    )
                except SpdkError as e:
                    exp_error = True
                    exp_error_msg = e.message
                else:
                    exp_error = False
                    exp_error_msg = None
                exp_info = cn_agent_pb2.ExpInfo(
                    exp_id=exp_cfg.exp_id,
                    error=exp_error,
                    error_msg=exp_error_msg,
                )
                exp_info_list.append(exp_info)
                standby_nvme_set.add(standby_nvme_name)
                exp_nqn_set.add(exp_nqn_name)
            da_cntlr_info = cn_agent_pb2.DaCntlrInfo(
                da_id=da_cntlr_cfg.da_id,
                cntlr_id=da_cntlr_cfg.cntlr_id,
                da_details=None,
                error=False,
                error_msg=None,
                grp_info_list=None,
                exp_info_list=exp_info_list,
            )
            da_cntlr_info_list.append(da_cntlr_info)

    oc.load_bdevs()

    exp_nqn_prefix = NameFmt.exp_nqn_prefix()
    exp_nqn_list = oc.get_exp_nqn_list(exp_nqn_prefix)
    for exp_nqn_name in exp_nqn_list:
        if exp_nqn_name not in exp_nqn_set:
            oc.delete_exp_nvmf(exp_nqn_name)

    standby_nvme_prefix = NameFmt.standby_nvme_prefix()
    standby_nvme_list = oc.get_standby_nvme_list(standby_nvme_prefix)
    for standby_nvme_name in standby_nvme_list:
        if standby_nvme_name not in standby_nvme_set:
            oc.delete_standby_nvme(standby_nvme_name)

    da_lvs_prefix = NameFmt.da_lvs_prefix()
    da_lvs_list = oc.get_da_lvs_list(da_lvs_prefix)
    for da_lvs_name in da_lvs_list:
        if da_lvs_name not in da_lvs_set:
            oc.delete_da_lvs(da_lvs_name)

    agg_bdev_prefix = NameFmt.agg_bdev_prefix()
    agg_bdev_list = oc.get_agg_bdev_list(agg_bdev_prefix)
    for agg_bdev_name in agg_bdev_list:
        if agg_bdev_name not in agg_bdev_set:
            oc.delete_agg_bdev(agg_bdev_name)

    cleanup_grps(oc, grp_ctx)

    frontend_nvme_prefix = NameFmt.frontend_nvme_prefix()
    frontend_nvme_list = oc.get_frontend_nvme_list(frontend_nvme_prefix)
    for frontend_nvme_name in frontend_nvme_list:
        if frontend_nvme_name not in frontend_nvme_set:
            oc.delete_frontend_nvme(frontend_nvme_name)

    cn_info = cn_agent_pb2.CnInfo(
        cn_id=cn_cfg.cn_id,
        error=False,
        error_msg=None,
        da_cntlr_info_list=da_cntlr_info_list,
    )
    reply_info = cn_agent_pb2.CnAgentReplyInfo(
        reply_code=Constant.cn_success.reply_code,
        reply_msg=Constant.cn_success.reply_msg,
    )
    reply = cn_agent_pb2.SyncupCnReply(
        reply_info=reply_info,
        cn_info=cn_info,
    )
    return reply


def syncup_init(client, local_store, listener_conf):
    global g_cn_cfg
    if local_store and os.path.isfile(local_store):
        with open(local_store) as f:
            data = f.read()
        schema = CnCfgSchema()
        g_cn_cfg = schema.loads(data)
        do_cn_syncup(g_cn_cfg, client, local_store, listener_conf)


def syncup_cn(request, context):
    return do_cn_syncup(
        request.cn_cfg,
        context.client,
        context.local_store,
        context.listener_conf,
    )
