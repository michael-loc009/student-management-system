# =======Khai báo sử dụng thư viện hàm
import json
import glob
from pathlib import Path

# =======Khai báo biến cục bộ
Thu_muc_Du_lieu = Path("Du_lieu")
Thu_muc_HTML = Thu_muc_Du_lieu / "HTML"
Thu_muc_Cong_ty = Thu_muc_Du_lieu / "Cong_ty"
Thu_muc_Nhan_vien = Thu_muc_Du_lieu / "Nhan_vien"

# ================Xử lý lưu trữ=======================================


def Doc_Khung_HTML():
    Duong_dan = Thu_muc_HTML / "Khung.html"
    Tap_tin = open(Duong_dan, encoding="utf-8")
    Chuoi_HTML = Tap_tin.read()
    return Chuoi_HTML


def Doc_Cong_ty(Loai_Nhan_vien="", Ten_Dang_nhap="", Mat_khau=""):
    Duong_dan = Thu_muc_Cong_ty / "Cong_ty.json"
    Tap_tin = open(Duong_dan, encoding="utf-8")
    Chuoi_JSON = Tap_tin.read()
    Cong_ty = json.loads(Chuoi_JSON)

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
    Danh_sach_nhan_vien = []
    for Duong_dan in Thu_muc_Nhan_vien.glob("*.json"):
        Chuoi_JSON = Duong_dan.read_text("utf-8")
        Nhan_vien = json.loads(Chuoi_JSON)
        if Nhan_vien["Ten_Dang_nhap"] == Ten_Dang_nhap and Nhan_vien["Mat_khau"] == Mat_khau:
            Nhan_vien.pop("Ten_Dang_nhap", None)
            Nhan_vien.pop("Mat_khau", None)
            Danh_sach_nhan_vien.append(Nhan_vien)
            break
    return Danh_sach_nhan_vien


def Doc_Danh_sach_Nhan_vien(Ma_Chi_nhanh, Ma_Don_vi):
    Danh_sach_Nhan_vien = []
    for Duong_dan in Thu_muc_Nhan_vien.glob("*.json"):
        Chuoi_JSON = Duong_dan.read_text("utf-8")
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
    return Danh_sach_Nhan_vien


def Ghi_Nhan_vien(Nhan_vien, Thuoc_tinh_can_thay_doi):
    Duong_dan = Thu_muc_Nhan_vien / f"{Nhan_vien['Ma_so']}.json"

    with open(Duong_dan, 'r', encoding="utf-8") as Tap_tin:
        Nhan_vien_goc = json.load(Tap_tin)
        if Thuoc_tinh_can_thay_doi in Nhan_vien_goc:
            Nhan_vien_goc[Thuoc_tinh_can_thay_doi] = Nhan_vien[Thuoc_tinh_can_thay_doi]

    with open(Duong_dan, 'w', encoding="utf-8") as Tap_tin:
        json.dump(Nhan_vien_goc, Tap_tin, ensure_ascii=False, indent=1)


def Ghi_Hinh_Nhan_vien(Ma_Nhan_vien, Hinh):
    Duong_dan = f"Media\\{Ma_Nhan_vien}.png"
    Hinh.save(Duong_dan)
