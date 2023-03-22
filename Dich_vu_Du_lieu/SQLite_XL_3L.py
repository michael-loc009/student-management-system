# =======Khai báo sử dụng thư viện hàm
import json
import glob
import sqlite3
from pathlib import Path

# =======Khai báo biến cục bộ
Thu_muc_Du_lieu = "Du_lieu"
Thu_muc_HTML = Path(Thu_muc_Du_lieu) / "HTML"
Ten_CSDL = "QLNV.sqlite"
Duong_dan_CSDL = f"{Thu_muc_Du_lieu}\\{Ten_CSDL}"


def Doc_Khung_HTML():
    Duong_dan = Thu_muc_HTML / "Khung.html"
    Tap_tin = open(Duong_dan, encoding="utf-8")
    Chuoi_HTML = Tap_tin.read()
    return Chuoi_HTML


def Doc_Cong_ty(Loai_Nhan_vien="", Ten_Dang_nhap="", Mat_khau=""):
    Cong_ty = {}
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Lenh = "select * from Cong_ty"
    for Dong in Ket_noi.execute(Lenh):
        Chuoi_JSON = Dong[1]
        Cong_ty = json.loads(Chuoi_JSON)
    Ket_noi.close()

    if Loai_Nhan_vien == "Quan_ly_Chi_nhanh":
        Danh_sach = [Quan_ly_Chi_nhanh for Quan_ly_Chi_nhanh in Cong_ty["Danh_sach_Quan_ly_Chi_nhanh"]
                     if Quan_ly_Chi_nhanh["Ten_Dang_nhap"] == Ten_Dang_nhap and Quan_ly_Chi_nhanh["Mat_khau"] == Mat_khau]
        Hop_le = any(Danh_sach)
        if not Hop_le:
            return None

        Danh_sach[0].pop("Ten_Dang_nhap", None)
        Danh_sach[0].pop("Mat_khau", None)
        Cong_ty["Danh_sach_Quan_ly_Chi_nhanh"] = Danh_sach
        Cong_ty["Danh_sach_Quan_ly_Don_vi"] = []

    if Loai_Nhan_vien == "Quan_ly_Don_vi":
        Danh_sach = [Quan_ly_Don_vi for Quan_ly_Don_vi in Cong_ty["Danh_sach_Quan_ly_Don_vi"]
                     if Quan_ly_Don_vi["Ten_Dang_nhap"] == Ten_Dang_nhap and Quan_ly_Don_vi["Mat_khau"] == Mat_khau]
        Hop_le = any(Danh_sach)
        if not Hop_le:
            return None

        Danh_sach[0].pop("Ten_Dang_nhap", None)
        Danh_sach[0].pop("Mat_khau", None)
        Cong_ty["Danh_sach_Quan_ly_Chi_nhanh"] = []
        Cong_ty["Danh_sach_Quan_ly_Don_vi"] = Danh_sach

    if Loai_Nhan_vien == "":
        Cong_ty["Danh_sach_Quan_ly_Chi_nhanh"] = []
        Cong_ty["Danh_sach_Quan_ly_Don_vi"] = []

    return Cong_ty


def Doc_Nhan_vien(Ten_Dang_nhap="", Mat_khau=""):
    Danh_sach_Nhan_vien = []
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Lenh = "select * from Nhan_vien"
    for Dong in Ket_noi.execute(Lenh):
        Chuoi_JSON = Dong[1]
        Nhan_vien = json.loads(Chuoi_JSON)
        if Nhan_vien["Ten_Dang_nhap"] == Ten_Dang_nhap and Nhan_vien["Mat_khau"] == Mat_khau:
            Nhan_vien.pop("Ten_Dang_nhap", None)
            Nhan_vien.pop("Mat_khau", None)
            Danh_sach_Nhan_vien.append(Nhan_vien)
            Danh_sach_Nhan_vien.append(Nhan_vien)
            break
    Ket_noi.close()

    return Danh_sach_Nhan_vien


def Doc_Danh_sach_Nhan_vien(Ma_Chi_nhanh, Ma_Don_vi):
    Danh_sach_Nhan_vien = []
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Lenh = "select * from Nhan_vien"

    for Dong in Ket_noi.execute(Lenh):
        Chuoi_JSON = Dong[1]
        Nhan_vien = json.loads(Chuoi_JSON)
        Don_vi = Nhan_vien["Don_vi"]
        Chi_nhanh = Nhan_vien["Don_vi"]["Chi_nhanh"]

        if Ma_Chi_nhanh:
            if Chi_nhanh["Ma_so"] == Ma_Chi_nhanh:
                Nhan_vien.pop("Ten_Dang_nhap", None)
                Nhan_vien.pop("Mat_khau", None)
                Danh_sach_Nhan_vien.append(Nhan_vien)

        if Ma_Don_vi:
            if Don_vi["Ma_so"] == Ma_Don_vi:
                Nhan_vien.pop("Ten_Dang_nhap", None)
                Nhan_vien.pop("Mat_khau", None)
                Danh_sach_Nhan_vien.append(Nhan_vien)

    Ket_noi.close()

    return Danh_sach_Nhan_vien


def Ghi_Nhan_vien(Nhan_vien, Thuoc_tinh_can_thay_doi):
    Ket_noi = sqlite3.connect(Duong_dan_CSDL)
    Ma_Nhan_vien = Nhan_vien["Ma_so"]
    Lenh = f"select * from Nhan_vien where Ma_so = '{Ma_Nhan_vien}'"

    for Dong in Ket_noi.execute(Lenh):
        Chuoi_JSON = Dong[1]
        Nhan_vien_goc = json.loads(Chuoi_JSON)
        if Thuoc_tinh_can_thay_doi in Nhan_vien_goc:
            Nhan_vien_goc[Thuoc_tinh_can_thay_doi] = Nhan_vien[Thuoc_tinh_can_thay_doi]
            Chuoi_JSON = json.dumps(Nhan_vien_goc)
            Lenh = f"update Nhan_vien set Chuoi_JSON = '{Chuoi_JSON}' where Ma_so = '{Ma_Nhan_vien}'"
            Ket_noi.execute(Lenh)
            Ket_noi.commit()

    Ket_noi.close()


def Ghi_Hinh_Nhan_vien(Ma_Nhan_vien, Hinh):
    Duong_dan = f"Media\\{Ma_Nhan_vien}.png"
    Hinh.save(Duong_dan)
