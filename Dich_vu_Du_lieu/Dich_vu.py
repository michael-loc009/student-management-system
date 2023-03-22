# =======Khai báo sử dụng thư viện hàm
from flask import Flask, Markup, request, session, jsonify
import json
# from JSON_XL_3L import *
from SQLite_XL_3L import *

# =======Khai báo và cấu hình dịch vụ
Dich_vu = Flask(__name__, static_url_path="/Media", static_folder="Media")
Dich_vu.secret_key = '123456789'


@Dich_vu.route("/Doc_khung_HTML", methods=["POST"])
def XL_Khoi_dong():
    Doi_tuong_A = request.get_json()
    Doi_tuong_B = {"Kq": True}
    Doi_tuong_B["Chuoi_HTML_Khung"] = Doc_Khung_HTML()
    if not Doi_tuong_B["Chuoi_HTML_Khung"]:
        Doi_tuong_B["Kq"] = False

    return jsonify(Doi_tuong_B)


@Dich_vu.route("/Dang_nhap", methods=["POST"])
def XL_Dang_nhap():
    Doi_tuong_A = request.get_json()

    Loai_nhan_vien = Doi_tuong_A["Loai_Nhan_vien"]
    Ten_Dang_nhap = Doi_tuong_A["Ten_Dang_nhap"]
    Mat_khau = Doi_tuong_A["Mat_khau"]
    Doi_tuong_B = {"Kq": False}

    if Loai_nhan_vien and Ten_Dang_nhap and Mat_khau:

        if Loai_nhan_vien == "Nhan_vien":
            Doi_tuong_B["Danh_sach_Nhan_vien"] = Doc_Nhan_vien(
                Ten_Dang_nhap, Mat_khau)
            Doi_tuong_B["Cong_ty"] = Doc_Cong_ty("", "", "")
            Doi_tuong_B["Kq"] = True

        if Loai_nhan_vien == "Quan_ly_Don_vi":
            Doi_tuong_B["Cong_ty"] = Doc_Cong_ty(
                "Quan_ly_Don_vi", Ten_Dang_nhap, Mat_khau)
            Danh_sach_Quan_ly_Don_vi = Doi_tuong_B["Cong_ty"]["Danh_sach_Quan_ly_Don_vi"]

            if len(Danh_sach_Quan_ly_Don_vi) > 0:
                Quan_ly_Don_vi = Danh_sach_Quan_ly_Don_vi[0]
                Doi_tuong_B["Danh_sach_Nhan_vien"] = Doc_Danh_sach_Nhan_vien(
                    "", Quan_ly_Don_vi["Don_vi"]["Ma_so"])
                Doi_tuong_B["Kq"] = True

        if Loai_nhan_vien == "Quan_ly_Chi_nhanh":
            Doi_tuong_B["Cong_ty"] = Doc_Cong_ty(
                "Quan_ly_Chi_nhanh", Ten_Dang_nhap, Mat_khau)
            Danh_sach_Quan_ly_Chi_nhanh = Doi_tuong_B["Cong_ty"]["Danh_sach_Quan_ly_Chi_nhanh"]

            if len(Danh_sach_Quan_ly_Chi_nhanh) > 0:
                Quan_ly_Chi_nhanh = Danh_sach_Quan_ly_Chi_nhanh[0]
                Doi_tuong_B["Danh_sach_Nhan_vien"] = Doc_Danh_sach_Nhan_vien(
                    Quan_ly_Chi_nhanh["Chi_nhanh"]["Ma_so"], "")
                Doi_tuong_B["Kq"] = True

    return jsonify(Doi_tuong_B)


@Dich_vu.route("/Ghi_Nhan_vien", methods=["POST"])
def XL_Ghi_Nhan_vien():
    Doi_tuong_A = request.get_json()
    Nhan_vien = Doi_tuong_A["Nhan_vien"]
    Thuoc_tinh_can_thay_doi = Doi_tuong_A["Thuoc_tinh_can_thay_doi"]
    Doi_tuong_B = {"Kq": False}
    if Nhan_vien and Thuoc_tinh_can_thay_doi:
        Ghi_Nhan_vien(Nhan_vien, Thuoc_tinh_can_thay_doi)
        Doi_tuong_B["Kq"] = True
    return jsonify(Doi_tuong_B)


@Dich_vu.route("/Ghi_Hinh_Nhan_vien", methods=["POST"])
def XL_Ghi_Hinh_Nhan_vien():
    Doi_tuong_A = request.form.get("Ma_Nhan_vien")
    Ma_Nhan_vien = Doi_tuong_A
    Hinh = request.files["Th_Hinh"]
    Doi_tuong_B = {"Kq": False}
    if Ma_Nhan_vien and Hinh:
        Ghi_Hinh_Nhan_vien(Ma_Nhan_vien, Hinh)
        Doi_tuong_B["Kq"] = True
    return jsonify(Doi_tuong_B)
