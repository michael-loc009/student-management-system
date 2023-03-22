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

    if "Nhan_vien" in session:
        Nhan_vien = session["Nhan_vien"]
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Dang_nhap", methods=["POST"])
def XL_Dang_nhap():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Ten_Dang_nhap = request.form.get("Th_Ten_Dang_nhap")
    Mat_khau = request.form.get("Th_Mat_khau")

    Chuoi_HTML = ""

    Du_lieu = Doc_Du_lieu(Ten_Dang_nhap, Mat_khau, "Nhan_vien")

    if Du_lieu:
        Cong_ty = Du_lieu["Cong_ty"]
        Nhan_vien = Du_lieu["Danh_sach_Nhan_vien"][0]
        Nhan_vien["Quy_dinh_Nhan_vien"] = Cong_ty["Quy_dinh_Nhan_vien"]
        session["Nhan_vien"] = Nhan_vien
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("", "", "Đăng nhập không hợp lệ")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Quan_ly_Ho_so", methods=["POST"])
def XL_Quan_ly_Ho_so():
    Nhan_vien = session["Nhan_vien"]
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""

    if Nhan_vien:
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Nhan_vien(Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Dien_thoai", methods=["POST"])
def XL_Cap_nhat_Dien_Thoai():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Nhan_vien = session["Nhan_vien"]
    Dien_thoai = request.form.get("Th_Dien_thoai")

    if Nhan_vien and Dien_thoai:
        Nhan_vien["Dien_thoai"] = Dien_thoai
        Ghi_Nhan_vien(Nhan_vien, "Dien_thoai")
        session["Nhan_vien"] = Nhan_vien
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Nhan_vien(Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Dia_chi", methods=["POST"])
def XL_Cap_nhat_Dia_chi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Nhan_vien = session["Nhan_vien"]
    Dia_chi = request.form.get("Th_Dia_chi")

    if Nhan_vien and Dia_chi:
        Nhan_vien["Dia_chi"] = Dia_chi
        Ghi_Nhan_vien(Nhan_vien, "Dia_chi")
        session["Nhan_vien"] = Nhan_vien
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Nhan_vien(Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Hinh", methods=["POST"])
def XL_Cap_nhat_Hinh():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Nhan_vien = session["Nhan_vien"]
    Hinh = request.files["Th_Hinh"]

    if Nhan_vien and Hinh:
        Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh)
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Nhan_vien(Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Quan_ly_Don_xin_nghi", methods=["POST"])
def XL_Quan_ly_Don_xin_nghi():
    Nhan_vien = session["Nhan_vien"]
    Quy_dinh_Nhan_vien = Nhan_vien["Quy_dinh_Nhan_vien"]
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Danh_sach_Don_xin_nghi = Nhan_vien["Danh_sach_Don_xin_nghi"]

    if Nhan_vien:
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Danh_sach_Don_xin_nghi(
                Danh_sach_Don_xin_nghi, Quy_dinh_Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Tao_Don_xin_nghi", methods=["POST"])
def Tao_Don_xin_nghi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Nhan_vien = session["Nhan_vien"]
    Quy_dinh_Nhan_vien = Nhan_vien["Quy_dinh_Nhan_vien"]
    Danh_sach_Don_xin_nghi = Nhan_vien["Danh_sach_Don_xin_nghi"]
    Ma_so_Don_xin_nghi_cuoi = "DXN_1"
    Ngay_Bat_dau = request.form.get("Th_Ngay_Bat_dau")

    if len(Danh_sach_Don_xin_nghi) > 0:
        Ma_so_Don_xin_nghi_cuoi = "DXN_" + str((len(Danh_sach_Don_xin_nghi)+1))

    if Ngay_Bat_dau:
        Ngay_Bat_dau = Dinh_dang_Ngay(Ngay_Bat_dau, "%Y-%m-%d", "%d-%m-%Y")

    So_ngay = request.form.get("Th_So_ngay")
    Ly_do = request.form.get("Th_Ly_do")

    if Nhan_vien and Ngay_Bat_dau and So_ngay and Ly_do:
        T_Don_Xin_nghi = Don_Xin_nghi(Ma_so_Don_xin_nghi_cuoi,
                                      Ngay_Bat_dau, So_ngay, Ly_do, False, False, {}, {})
        Danh_sach_Don_xin_nghi.append(json.loads(
            json.dumps(T_Don_Xin_nghi.__dict__)))
        Nhan_vien["Danh_sach_Don_xin_nghi"] = Danh_sach_Don_xin_nghi
        Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Don_xin_nghi")
        session["Nhan_vien"] = Nhan_vien
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Danh_sach_Don_xin_nghi(
                Danh_sach_Don_xin_nghi, Quy_dinh_Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Cap_nhat_Don_xin_nghi", methods=["POST"])
def Cap_nhat_Don_xin_nghi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Nhan_vien = session["Nhan_vien"]
    Quy_dinh_Nhan_vien = Nhan_vien["Quy_dinh_Nhan_vien"]
    Danh_sach_Don_xin_nghi = Nhan_vien["Danh_sach_Don_xin_nghi"]
    Ma_so = request.form.get("Th_Ma_so")
    Ngay_Bat_dau = request.form.get("Th_Ngay_Bat_dau")

    if Ngay_Bat_dau:
        Ngay_Bat_dau = Dinh_dang_Ngay(Ngay_Bat_dau, "%Y-%m-%d", "%d-%m-%Y")

    So_ngay = request.form.get("Th_So_ngay")
    Ly_do = request.form.get("Th_Ly_do")

    for Don_xin_nghi in Danh_sach_Don_xin_nghi:
        if Don_xin_nghi["Ma_so"] == Ma_so:
            Don_xin_nghi["Ly_do"] = Ly_do
            Don_xin_nghi["Ngay_Bat_dau"] = Ngay_Bat_dau
            Don_xin_nghi["So_ngay"] = So_ngay
            break
    if Nhan_vien and Ngay_Bat_dau and So_ngay and Ly_do:

        Nhan_vien["Danh_sach_Don_xin_nghi"] = Danh_sach_Don_xin_nghi
        Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Don_xin_nghi")
        session["Nhan_vien"] = Nhan_vien
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Danh_sach_Don_xin_nghi(
                Danh_sach_Don_xin_nghi, Quy_dinh_Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML


@Ung_dung.route("/Xoa_Don_xin_nghi", methods=["POST"])
def Xoa_Don_xin_nghi():
    Chuoi_HTML_Khung = session["Chuoi_HTML_Khung"]
    Chuoi_HTML = ""
    Nhan_vien = session["Nhan_vien"]
    Quy_dinh_Nhan_vien = Nhan_vien["Quy_dinh_Nhan_vien"]
    Danh_sach_Don_xin_nghi = Nhan_vien["Danh_sach_Don_xin_nghi"]
    Ma_so = request.form.get("Th_Ma_so")

    Danh_sach = [Don_xin_nghi for Don_xin_nghi in Danh_sach_Don_xin_nghi
                 if Don_xin_nghi["Ma_so"] == Ma_so]
    Hop_le = any(Danh_sach)

    if Nhan_vien and Hop_le:
        Danh_sach_Don_xin_nghi.remove(Danh_sach[0])
        Nhan_vien["Danh_sach_Don_xin_nghi"] = Danh_sach_Don_xin_nghi
        Ghi_Nhan_vien(Nhan_vien, "Danh_sach_Don_xin_nghi")
        session["Nhan_vien"] = Nhan_vien
        Chuoi_HTML = Tao_Chuoi_HTML_Thuc_don_Nguoi_dung(Nhan_vien) \
            + Tao_Chuoi_HTML_Danh_sach_Don_xin_nghi(
                Danh_sach_Don_xin_nghi, Quy_dinh_Nhan_vien)
    else:
        Chuoi_HTML = Tao_Chuoi_HTML_Dang_nhap("NV_1", "NV_1")

    Chuoi_HTML = Chuoi_HTML_Khung.replace("Chuoi_HTML", Chuoi_HTML)
    return Chuoi_HTML
