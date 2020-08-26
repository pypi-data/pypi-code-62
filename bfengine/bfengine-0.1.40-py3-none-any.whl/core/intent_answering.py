import time
import traceback
import os
import xlsxwriter
import xlrd

from tqdm import tqdm

from .module import Module
from ..caller.qa_caller import QACaller
from ..caller.intent_caller import  IntentCaller
from ..entity.answer import Answer
from ..entity.enums import QuestionType, QuestionMode,QuestionField
from ..entity.exception import BfEngineException, ErrorCode
from ..logger import log


class IntentAnswering(Module):
    """
    问答
    """
    tmp_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    faq_sq_empty_path = tmp_dir + "/data/问答上传模板.xlsx"
    faq_lq_empty_path = tmp_dir + "/data/语料上传模板.xlsx"

    def __init__(self, app_id,set):
        super().__init__(app_id, 'qa',set)
        self.intentCaller = IntentCaller(app_id)
    def train(self, data: str = None,intent_path: str = None,append: bool = False):
        """
        :param data:
        :param append: 是否追加，True
        :return: 训练是否成功
        """
        try:
            log.info('intent: prepare train')
            if data:
                group_ids = []
                for item in data["data"]:
                    try:
                        group_id = self._add_group(item["domain"])
                        group_ids.append(group_id)
                        self._add_intents(group_id=group_id, intents=item["intents"])
                    except BfEngineException as bfe:
                        log.error(bfe)
                for group_id in group_ids:
                    self._train(group_id=group_id)
            elif intent_path:
                return
        except BfEngineException as bfe:
            log.error(bfe)
            return False
        except Exception as e:
            log.error('unknown exception')
            log.error(e)
            return False
        return True
    def domain(self,domain:str=None) -> bool:
        if not domain:
            return False

    def publish(self):
        """
        :发布
        :return: 机器人回答
        """
        self._pulish()
    def export(self,sq_path: str = None, lq_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        self._export(sq_path,lq_path)

    def query(self, text: str,online: bool=False) -> Answer:
        """
        :param text: 用户问
        :return: 机器人回答
        """

        data = self.intentCaller.predict(text,online)
        if len(data)>0:
            return Answer(text=data[0]["matchQuestion"],score=data[0]["score"])
        else:
            return None
    def _add_group(self,domain:str = None):
        return self.intentCaller.add_group(domain=domain)
    def _add_intents(self,group_id:str=None,intents:str=None):
        for intent in intents:
            self._add_intent(group_id=group_id,intent=intent)
    def _add_intent(self,group_id:str=None,intent:str=None):
        return self.intentCaller.add_intent(group_id=group_id,intent=intent)
    def _train(self,group_id:str=None,):
        log.info('qa: start training')
        self.intentCaller.train(group_id=group_id)
        progress = 0
        with tqdm(total=100) as bar:
            bar.set_description("intent training...")
            while progress < 100:
                old_progress = progress
                progress = self.intentCaller.train_status(group_id=group_id)
                bar.update(progress - old_progress)
                time.sleep(1)
            bar.set_description("intent train finished")
        time.sleep(5)
    def _export(self,sq_path: str = None, lq_path: str = None):
        """
        导出问答和语料文件
        :param sq_path 问答文件路径
        :param lq_path 语料文件路径
        """
        try:
            if sq_path:
                data_path = self.qaCaller.download_launch(QuestionType.SQ_ANS)
                self.qaCaller.download(sq_path,data_path)
            if lq_path:
                data_path = self.qaCaller.download_launch(QuestionType.LQ)
                self.qaCaller.download(lq_path, data_path)
        except BfEngineException as bfe:
            log.error(bfe)
        except Exception as e:
            log.error(e)
    def _read_intent_path(self,intent_path:str=None)->list:
        workbook = xlrd.open_workbook(intent_path)
        if workbook.sheets()==0:
            return []
        sheet = workbook.sheet_by_index(0)
        intent = {}
        for row in range(1, sheet.nrows):  # 行
            name = sheet.cell_value(row, 0)  # 语料
            corpus = sheet.cell_value(row, 1) # 意图名称
            if name in intent.keys():
                intent[name].append(corpus)
            else:
                intent[name]=[corpus]
        return intent