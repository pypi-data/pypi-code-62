from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject
from dapodik.utils.decorator import set_meta


@set_meta('klasifikasi_lembaga_id')
@dataclass(eq=False)
class KlasifikasiLembaga(DapodikObject):
    klasifikasi_lembaga_id: str
    nama: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime
