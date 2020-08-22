from dataclasses import dataclass
from dapodik.base import DapodikObject
from dapodik.utils.decorator import set_meta


@set_meta('pembelajaran_id')
@dataclass(eq=False)
class Pembelajaran(DapodikObject):
    rombongan_belajar_id: str
    status_di_kurikulum_str: str
    mata_pelajaran_id: int
    nama_mata_pelajaran: str
    sk_mengajar: str
    ptk_terdaftar_id: str
    tanggal_sk_mengajar: str
    jam_mengajar_per_minggu: 24
    induk_pembelajaran_id: str = ""
    status_di_kurikulum: int = 9
    semester_id: str = "20201"
    pembelajaran_id: str = "Admin.model.PembelajaranNew-1"
