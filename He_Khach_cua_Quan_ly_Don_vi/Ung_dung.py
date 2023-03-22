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

    if "Quan_ly_Don_vi" in session:
        Quan_ly_Don_vi = session["Quan_ly_Don_vi"]
        Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]
        Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_B2", "QLDV_B2")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Dang_nhap", methods=["POST"])
def XL_Dang_nhap():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Ten_Dang_nhap = request.form.get("Th_Ten_Dang_nhap")
    Mat_khau = request.form.get("Th_Mat_khau")

    Chuoi_HTML = ""
    Du_lieu = Doc_Du_lieu(Ten_Dang_nhap, Mat_khau, "Quan_ly_Don_vi")

    if Du_lieu:
        Cong_ty = Du_lieu["Cong_ty"]
        Danh_sach_Nhan_vien = Du_lieu["Danh_sach_Nhan_vien"]

        Quan_ly_Don_vi = Cong_ty["Danh_sach_Quan_ly_Don_vi"][0]
        Quan_ly_Don_vi["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        Quan_ly_Don_vi["Quy_dinh_Nhan_vien"] = Cong_ty["Quy_dinh_Nhan_vien"]
        Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"] = Cong_ty["Danh_sach_Ngoai_ngu"]

        session["Quan_ly_Don_vi"] = Quan_ly_Don_vi

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Cong_ty["Danh_sach_Ngoai_ngu"])
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Tra_cuu_Nhan_vien", methods=["POST"])
def XL_Tra_cuu_Nhan_vien():
    Quan_ly_Don_vi = session["Quan_ly_Don_vi"]
    Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]

    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_Tra_cuu = request.form.get("Th_Chuoi_Tra_cuu")
    Chuoi_HTML = ""

    if Danh_sach_Nhan_vien and Quan_ly_Don_vi:
        Danh_sach_Ket_qua = Tra_cuu_Nhan_vien(
            Danh_sach_Nhan_vien, Chuoi_Tra_cuu)
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Ket_qua, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Dien_thoai", methods=["POST"])
def XL_Cap_nhat_Dien_Thoai():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Don_vi = session["Quan_ly_Don_vi"]

    Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]

    Dien_thoai = request.form.get("Th_Dien_thoai")
    Ma_Nhan_vien = request.form.get("Th_Ma_so")

    if Danh_sach_Nhan_vien and Dien_thoai and Quan_ly_Don_vi and Ma_Nhan_vien:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                Nhan_vien["Dien_thoai"] = Dien_thoai
                Ghi_Nhan_vien(Nhan_vien, "Dien_thoai")
                break

        Quan_ly_Don_vi["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Don_vi"] = Quan_ly_Don_vi
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_B2", "QLDV_B2")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Dia_chi", methods=["POST"])
def XL_Cap_nhat_Dia_chi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Don_vi = session["Quan_ly_Don_vi"]
    Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]

    Dia_chi = request.form.get("Th_Dia_chi")
    Ma_Nhan_vien = request.form.get("Th_Ma_so")

    if Danh_sach_Nhan_vien and Dia_chi and Quan_ly_Don_vi and Ma_Nhan_vien:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                Nhan_vien["Dia_chi"] = Dia_chi
                Ghi_Nhan_vien(Nhan_vien, "Dia_chi")
                break

        Quan_ly_Don_vi["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Don_vi"] = Quan_ly_Don_vi

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_B2", "QLDV_B2")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Hinh", methods=["POST"])
def XL_Cap_nhat_Hinh():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""

    Quan_ly_Don_vi = session["Quan_ly_Don_vi"]
    Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]

    Hinh = request.files["Th_Hinh"]
    Ma_Nhan_vien = request.form.get("Th_Ma_so")

    if Danh_sach_Nhan_vien and Hinh and Quan_ly_Don_vi and Ma_Nhan_vien:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh)

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_B2", "QLDV_B2")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Ngoai_ngu", methods=["POST"])
def XL_Cap_nhat_Ngoai_ngu():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Don_vi = session["Quan_ly_Don_vi"]
    Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]

    Ngoai_ngu_duoc_chon = request.form.getlist("Th_Ngoai_ngu")
    Ma_Nhan_vien = request.form.get("Th_Ma_so")

    Danh_sach_Ngoai_ngu_duoc_chon = []
    for v1 in Ngoai_ngu_duoc_chon:
        for v2 in Danh_sach_Ngoai_ngu:
            if v1 == v2["Ma_so"]:
                Danh_sach_Ngoai_ngu_duoc_chon.append(v2)
                break

    if Danh_sach_Nhan_vien and Ngoai_ngu_duoc_chon and Quan_ly_Don_vi and Ma_Nhan_vien:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                Nhan_vien["Danh_sach_Ngoai_ngu"] = Danh_sach_Ngoai_ngu_duoc_chon
                Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Ngoai_ngu")
                break

        Quan_ly_Don_vi["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Don_vi"] = Quan_ly_Don_vi

        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_B2", "QLDV_B2")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Them_Y_kien_cho_Don_xin_nghi", methods=["POST"])
def Them_Y_kien_cho_Don_xin_nghi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Don_vi = session["Quan_ly_Don_vi"]
    Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]

    Ma_Nhan_vien = request.form.get("Th_Ma_Nhan_vien")
    Ma_so_Don_xin_nghi = request.form.get("Th_Ma_Don_xin_nghi")
    Ngay_Tao = request.form.get("Th_Ngay_tao")
    Y_kien = request.form.get("Th_Y_kien")
    Duyet_Don_xin_nghi = request.form.get("Th_Duyet_Don_xin_nghi")

    if Ngay_Tao:
        Ngay_Tao = Dinh_dang_Ngay(Ngay_Tao, "%Y-%m-%d", "%d-%m-%Y")

    Duyet_Don_xin_nghi = Xu_ly_Boolean(Duyet_Don_xin_nghi)

    if Danh_sach_Nhan_vien and Ngay_Tao and Y_kien and Quan_ly_Don_vi:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                for Don_xin_nghi in Nhan_vien["Danh_sach_Don_xin_nghi"]:
                    if Don_xin_nghi["Ma_so"] == Ma_so_Don_xin_nghi:
                        Don_xin_nghi["Duyet_boi_Quan_li_Don_vi"] = Duyet_Don_xin_nghi
                        Y_kien_Quan_ly_Don_vi = Y_kien_Don_xin_nghi(
                            Ngay_Tao, Y_kien)
                        Don_xin_nghi["Y_kien_Quan_ly_Don_vi"] = json.loads(
                            json.dumps(Y_kien_Quan_ly_Don_vi.__dict__))
                        Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Don_xin_nghi")
                        break
                break

        Quan_ly_Don_vi["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Don_vi"] = Quan_ly_Don_vi
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_B2", "QLDV_B2")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Sua_Y_kien_cho_Don_xin_nghi", methods=["POST"])
def Sua_Y_kien_cho_Don_xin_nghi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Quan_ly_Don_vi = session["Quan_ly_Don_vi"]
    Danh_sach_Nhan_vien = Quan_ly_Don_vi["Danh_sach_Nhan_vien"]
    Danh_sach_Ngoai_ngu = Quan_ly_Don_vi["Danh_sach_Ngoai_ngu"]

    Ma_Nhan_vien = request.form.get("Th_Ma_Nhan_vien")
    Ma_so_Don_xin_nghi = request.form.get("Th_Ma_Don_xin_nghi")
    Ngay_Tao = request.form.get("Th_Ngay_tao")
    Y_kien = request.form.get("Th_Y_kien")
    Duyet_Don_xin_nghi = request.form.get("Th_Duyet_Don_xin_nghi")

    if Ngay_Tao:
        Ngay_Tao = Dinh_dang_Ngay(Ngay_Tao, "%Y-%m-%d", "%d-%m-%Y")

    Duyet_Don_xin_nghi = Xu_ly_Boolean(Duyet_Don_xin_nghi)

    if Danh_sach_Nhan_vien and Ngay_Tao and Y_kien and Quan_ly_Don_vi:
        for Nhan_vien in Danh_sach_Nhan_vien:
            if Nhan_vien["Ma_so"] == Ma_Nhan_vien:
                for Don_xin_nghi in Nhan_vien["Danh_sach_Don_xin_nghi"]:
                    if Don_xin_nghi["Ma_so"] == Ma_so_Don_xin_nghi:
                        Don_xin_nghi["Duyet_boi_Quan_li_Don_vi"] = Duyet_Don_xin_nghi
                        Don_xin_nghi["Y_kien_Quan_ly_Don_vi"]["Ngay"] = Ngay_Tao
                        Don_xin_nghi["Y_kien_Quan_ly_Don_vi"]["Noi_dung"] = Y_kien
                        Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Don_xin_nghi")
                        break
                break

        Quan_ly_Don_vi["Danh_sach_Nhan_vien"] = Danh_sach_Nhan_vien
        session["Quan_ly_Don_vi"] = Quan_ly_Don_vi
        Chuoi_HTML = Tao_Chuoi_HTML_Danh_sach_Nhan_vien(
            Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("QLDV_B2", "QLDV_B2")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML
