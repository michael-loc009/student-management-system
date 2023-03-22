# =======Khai báo sử dụng thư viện hàm
from flask import Flask, Markup, request, session
from XL_3L import *
# =======Khai báo và cấu hình ứng dụng
Ung_dung = Flask(__name__, static_url_path="/Media", static_folder="..\\Media")
Ung_dung.secret_key = '123456789'

# =======Khai báo và khởi động biến toàn cục


@Ung_dung.route("/", methods=["GET"])
def XL_Khoi_dong():
    Chuoi_HTML_Khung = ""
    Chuoi_HTML = ""

    if "Chuoi_HTML_Khung" in session:
        Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    else:
        Chuoi_HTML_Khung = Doc_Khung_HTML()
        session["Chuoi_HTML_Khung"] = Chuoi_HTML_Khung

    if "Quan_ly_Chi_nhanh" in session:
        Quan_ly_Chi_nhanh = session["Quan_ly_Chi_nhanh"]
        Danh_sach_Don_vi = Quan_ly_Chi_nhanh["Danh_sach_Don_vi"]
        Danh_sach_Nhan_vien = Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"]

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLCN_B", "QLCN_B")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Dang_nhap", methods=["POST"])
def XL_Dang_nhap():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""

    Ten_Dang_nhap = request.form.get("Th_Ten_Dang_nhap")
    Mat_khau = request.form.get("Th_Mat_khau")

    Du_lieu = Doc_Du_lieu(Ten_Dang_nhap, Mat_khau, "Quan_ly_Chi_nhanh")
    if Du_lieu:
        Cong_ty = Du_lieu["Cong_ty"]
        Danh_sach_Nhan_vien = Du_lieu["Danh_sach_Nhan_vien"]

        Quan_ly_Chi_nhanh = Cong_ty["Danh_sach_Quan_ly_Chi_nhanh"][0]
        Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        Quan_ly_Chi_nhanh["Quy_dinh_Nhan_vien"] = Cong_ty["Quy_dinh_Nhan_vien"]
        Quan_ly_Chi_nhanh["Danh_sach_Ngoai_ngu"] = Cong_ty["Danh_sach_Ngoai_ngu"]

        Danh_sach_Don_vi = [
            Don_vi for Don_vi in Cong_ty["Danh_sach_Don_vi"] if Don_vi["Chi_nhanh"]["Ma_so"] == Quan_ly_Chi_nhanh["Chi_nhanh"]["Ma_so"]]
        Quan_ly_Chi_nhanh["Danh_sach_Don_vi"] = Danh_sach_Don_vi

        session["Quan_ly_Chi_nhanh"] = Quan_ly_Chi_nhanh

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Tra_cuu_Nhan_vien", methods=["POST"])
def XL_Tra_cuu_Nhan_vien():
    Quan_ly_Chi_nhanh = session["Quan_ly_Chi_nhanh"]
    Danh_sach_Nhan_vien = Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"]
    Danh_sach_Don_vi = Quan_ly_Chi_nhanh["Danh_sach_Don_vi"]
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_Tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
    Chuoi_HTML = ""

    if Danh_sach_Nhan_vien and Quan_ly_Chi_nhanh:
        Danh_sach_Ket_qua = Tra_cuu_Nhan_vien(
            Danh_sach_Nhan_vien, Chuoi_Tra_cuu)
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Ket_qua, Danh_sach_Don_vi)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Thong_ke_Nhan_vien_Theo_Don_vi", methods=["POST"])
def XL_Thong_ke_Nhan_vien_Theo_Don_vi():
    Quan_ly_Chi_nhanh = session["Quan_ly_Chi_nhanh"]
    Danh_sach_Nhan_vien = Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"]
    Danh_sach_Don_vi = Quan_ly_Chi_nhanh["Danh_sach_Don_vi"]
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""

    if Danh_sach_Nhan_vien and Quan_ly_Chi_nhanh:
        Thong_ke_Nhan_vien_Theo_Don_vi = Thong_ke_Nhan_vien_theo_Don_vi(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)
        Chuoi_HTML = Tao_Chuoi_HTML_Thong_ke_Nhan_vien_Theo_Don_vi(
            Thong_ke_Nhan_vien_Theo_Don_vi)
        Chuoi_HTML += Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)

    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Thong_ke_Nhan_vien_Theo_Ngoai_ngu", methods=["POST"])
def XL_Thong_ke_Nhan_vien_Theo_Ngoai_ngu():
    Quan_ly_Chi_nhanh = session["Quan_ly_Chi_nhanh"]
    Danh_sach_Nhan_vien = Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Chi_nhanh["Danh_sach_Ngoai_ngu"]
    Danh_sach_Don_vi = Quan_ly_Chi_nhanh["Danh_sach_Don_vi"]
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""

    if Danh_sach_Nhan_vien and Quan_ly_Chi_nhanh:
        Thong_ke_Nhan_vien_Theo_Ngoai_ngu = Thong_ke_Nhan_vien_theo_Ngoai_ngu(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
        Chuoi_HTML = Tao_Chuoi_HTML_Thong_ke_Nhan_vien_Theo_Ngoai_ngu(
            Thong_ke_Nhan_vien_Theo_Ngoai_ngu)
        Chuoi_HTML += Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Chuyen_Don_vi", methods=["POST"])
def XL_Chuyen_Don_vi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Chi_nhanh = session["Quan_ly_Chi_nhanh"]
    Danh_sach_Nhan_vien = Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"]
    Danh_sach_Don_vi = Quan_ly_Chi_nhanh["Danh_sach_Don_vi"]

    Don_vi_duoc_chon = request.form.get("Th_Don_vi")
    Ma_Nhan_vien = request.form.get("Th_Ma_so")

    for Don_vi in Danh_sach_Don_vi:
        if Don_vi["Ma_so"] == Don_vi_duoc_chon:
            Don_vi_duoc_chon = Don_vi
            break

    if Danh_sach_Nhan_vien and Don_vi_duoc_chon and Quan_ly_Chi_nhanh and Ma_Nhan_vien:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                Nhan_vien["Don_vi"] = Don_vi_duoc_chon
                Ghi_Nhan_vien(Nhan_vien, "Don_vi")
                break

        Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Chi_nhanh"] = Quan_ly_Chi_nhanh
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLCN_B", "QLCN_B")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Them_Y_kien_cho_Don_xin_nghi", methods=["POST"])
def Them_Y_kien_cho_Don_xin_nghi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Chi_nhanh = session["Quan_ly_Chi_nhanh"]
    Danh_sach_Nhan_vien = Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"]
    Danh_sach_Don_vi = Quan_ly_Chi_nhanh["Danh_sach_Don_vi"]

    Ma_Nhan_vien = request.form.get("Th_Ma_Nhan_vien")
    Ma_so_Don_xin_nghi = request.form.get("Th_Ma_Don_xin_nghi")
    Ngay_Tao = request.form.get("Th_Ngay_tao")
    Y_kien = request.form.get("Th_Y_kien")
    Duyet_Don_xin_nghi = request.form.get("Th_Duyet_Don_xin_nghi")

    if Ngay_Tao:
        Ngay_Tao = Dinh_dang_Ngay(Ngay_Tao, "%Y-%m-%d", "%d-%m-%Y")

    Duyet_Don_xin_nghi = Xu_ly_Boolean(Duyet_Don_xin_nghi)

    if Danh_sach_Nhan_vien and Ngay_Tao and Y_kien and Quan_ly_Chi_nhanh:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                for Don_xin_nghi in Nhan_vien["Danh_sach_Don_xin_nghi"]:
                    if Don_xin_nghi["Ma_so"] == Ma_so_Don_xin_nghi:
                        Don_xin_nghi["Duyet_boi_Quan_li_Chi_nhanh"] = Duyet_Don_xin_nghi
                        Y_kien_Quan_ly_Chi_nhanh = Y_kien_Don_xin_nghi(
                            Ngay_Tao, Y_kien)
                        Don_xin_nghi["Y_kien_Quan_ly_Chi_nhanh"] = json.loads(
                            json.dumps(Y_kien_Quan_ly_Chi_nhanh.__dict__))
                        Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Don_xin_nghi")
                        break
                break

        Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Chi_nhanh"] = Quan_ly_Chi_nhanh

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLCN_B", "QLCN_B")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Sua_Y_kien_cho_Don_xin_nghi", methods=["POST"])
def Sua_Y_kien_cho_Don_xin_nghi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Chi_nhanh = session["Quan_ly_Chi_nhanh"]
    Danh_sach_Nhan_vien = Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"]
    Danh_sach_Don_vi = Quan_ly_Chi_nhanh["Danh_sach_Don_vi"]

    Ma_Nhan_vien = request.form.get("Th_Ma_Nhan_vien")
    Ma_so_Don_xin_nghi = request.form.get("Th_Ma_Don_xin_nghi")
    Ngay_Tao = request.form.get("Th_Ngay_tao")
    Y_kien = request.form.get("Th_Y_kien")
    Duyet_Don_xin_nghi = request.form.get("Th_Duyet_Don_xin_nghi")

    if Ngay_Tao:
        Ngay_Tao = Dinh_dang_Ngay(Ngay_Tao, "%Y-%m-%d", "%d-%m-%Y")

    Duyet_Don_xin_nghi = Xu_ly_Boolean(Duyet_Don_xin_nghi)

    if Danh_sach_Nhan_vien and Ngay_Tao and Y_kien and Quan_ly_Chi_nhanh:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                for Don_xin_nghi in Nhan_vien["Danh_sach_Don_xin_nghi"]:
                    if Don_xin_nghi["Ma_so"] == Ma_so_Don_xin_nghi:
                        Don_xin_nghi["Duyet_boi_Quan_li_Chi_nhanh"] = Duyet_Don_xin_nghi
                        Don_xin_nghi["Y_kien_Quan_ly_Chi_nhanh"]["Ngay"] = Ngay_Tao
                        Don_xin_nghi["Y_kien_Quan_ly_Chi_nhanh"]["Noi_dung"] = Y_kien
                        Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Don_xin_nghi")
                        break
                break

        Quan_ly_Chi_nhanh["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Chi_nhanh"] = Quan_ly_Chi_nhanh
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Don_vi)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLCN_B", "QLCN_B")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML
