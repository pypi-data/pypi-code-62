from gt_push_sdk.protobuf.gt_req_pb2 import InnerFiled

from gt_push_sdk.protobuf import *
from . import igt_base_template
from gt_push_sdk.igetui.template.style.AbstractNotifyStyle import *


class RevokeTemplate(igt_base_template.BaseTemplate):
    def __init__(self):
        igt_base_template.BaseTemplate.__init__(self)
        # 在没有找到对应的taskid，是否把对应appid下所有的通知都撤回
        self.force = True
        # 根据oldTaskid进行撤回
        self.oldTaskId = ""
        self.transmissionContent = ""
        self.transmissionType = 0
        self.pushType = "NotifyMsg"

    def getActionChains(self):
        # 构建 actionchain
        actionChain1 = gt_req_pb2.ActionChain()
        actionChain1.actionId = 1
        actionChain1.type = gt_req_pb2.ActionChain.mmsinbox2
        actionChain1.stype = "terminatetask"
        actionChain1.taskid = self.oldTaskId
        innerFiled = actionChain1.field.add()
        innerFiled.key = "force"
        innerFiled.val = str(self.force)
        innerFiled.type = InnerFiled.bool
        actionChain1.next = 100

        # Finish
        actionChain2 = gt_req_pb2.ActionChain()
        actionChain2.type = gt_req_pb2.ActionChain.eoa
        actionChain2.actionId = 100

        actionChains = [actionChain1, actionChain2]

        return actionChains

    def getTemplateId(self):
        return 8
