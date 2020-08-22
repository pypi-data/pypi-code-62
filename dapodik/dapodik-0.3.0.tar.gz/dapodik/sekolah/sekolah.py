from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from dapodik.base import DapodikObject
from .yayasan import Yayasan


@dataclass(eq=False)
class Sekolah(DapodikObject):
    sekolah_id: str
    nama: str
    nama_nomenklatur: Optional[str]
    nss: str
    npsn: str
    bentuk_pendidikan_id: int
    alamat_jalan: str
    rt: Optional[str]
    rw: Optional[str]
    nama_dusun: Optional[str]
    desa_kelurahan: str
    kode_wilayah: str
    kode_pos: Optional[str]
    lintang: Optional[str]
    bujur: Optional[str]
    nomor_telepon: Optional[str]
    nomor_fax: Optional[str]
    email: Optional[str]
    website: Optional[str]
    kebutuhan_khusus_id: int
    status_sekolah: str
    sk_pendirian_sekolah: str
    tanggal_sk_pendirian: str
    status_kepemilikan_id: str
    yayasan_id: Yayasan
    sk_izin_operasional: str
    tanggal_sk_izin_operasional: str
    no_rekening: Optional[str]
    nama_bank: Optional[str]
    cabang_kcp_unit: Optional[str]
    rekening_atas_nama: Optional[str]
    mbs: str
    luas_tanah_milik: str
    luas_tanah_bukan_milik: str
    kode_registrasi: str
    npwp: Optional[str]
    nm_wp: Optional[str]
    keaktifan: str
    flag: Optional[str]
    create_date: datetime
    last_update: datetime
    soft_delete: str
    last_sync: datetime
    updater_id: str
    bentuk_pendidikan_id_str: str
    kode_wilayah_str: str
    kebutuhan_khusus_id_str: str
    yayasan_id_str: str
    vld_count: int

    @property
    @Yayasan.getter
    def yayasan(self):
        return self.yayasan_id

    @yayasan.setter
    def yayasan(self, value):
        self.yayasan_id = value
