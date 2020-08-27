# MIT License
#
# Copyright (c) 2020 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json

from blockchainetl_common.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl_common.jobs.base_job import BaseJob
from blockchainetl_common.utils import validate_range

from bandetl.utils.string_utils import json_dumps
from cli.bandetl.service.band_service import BandService


class ExportTransactionsJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            band_rpc,
            max_workers,
            item_exporter,
            batch_size=1,
            export_transactions=True,
            export_event_logs=True,
            export_exceptions=True,
            export_transitions=True):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.band_service = BandService(band_rpc)

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        transactions = self.band_service.get_transactions(block_number_batch)

        for transaction in transactions:
            for tx in transaction.get('txs', []):
                self.item_exporter.export_item({**tx, **{
                    'type': 'transaction',
                    'raw_json': json_dumps(tx),
                }})

                for msg in tx.get('tx', {}).get('value', {}).get('msg', []):
                    self.item_exporter.export_item({**msg, **{
                        'type': 'message',
                        'message_type': msg.get('type'),
                        'raw_json': json_dumps(msg),
                    }})

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
