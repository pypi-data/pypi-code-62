from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject
from dapodik.rest import JenisKeluar
from dapodik.utils.decorator import set_meta


@set_meta('ptk_terdaftar_id')
@dataclass(eq=False)
class PtkTerdaftar(DapodikObject):
    ptk_terdaftar_id: str
    ptk_id: str
    sekolah_id: str
    jenis_keluar_id: Optional[str]
    tahun_ajaran_id: str
    nomor_surat_tugas: str
    tanggal_surat_tugas: str
    ptk_induk: str
    tmt_tugas: str
    aktif_bulan_01: str
    aktif_bulan_02: str
    aktif_bulan_03: str
    aktif_bulan_04: str
    aktif_bulan_05: str
    aktif_bulan_06: str
    aktif_bulan_07: str
    aktif_bulan_08: str
    aktif_bulan_09: str
    aktif_bulan_10: str
    aktif_bulan_11: str
    aktif_bulan_12: str
    tgl_ptk_keluar: Optional[str]
    create_date: datetime
    last_update: datetime
    soft_delete: str
    last_sync: datetime
    updater_id: str
    ptk_id_str: str
    sekolah_id_str: str
    tahun_ajaran_id_str: str

    @property
    @JenisKeluar.getter
    def jenis_keluar(self) -> Optional[JenisKeluar]:
        return self.jenis_keluar_id
