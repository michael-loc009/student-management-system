# =======Khai báo sử dụng thư viện hàm
from pathlib import Path
import json
import requests
from random import randint
from datetime import datetime, timedelta


# =======Khai báo và khởi động biến toàn cục
Dia_chi_Dich_vu = "http://localhost:4001"
Dia_chi_Media = f"{Dia_chi_Dich_vu}/Media"


# ================Xử lý lưu trữ=======================================
def Doc_Khung_HTML():
    Chuoi_HTML = ""
    Doi_tuong_A = {}
    Ma_so_Xu_ly = "Doc_khung_HTML"
    Dia_chi_Xu_ly = f"{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}"
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A)
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B["Kq"]:
        Chuoi_HTML = Doi_tuong_B["Chuoi_HTML_Khung"]

    return Chuoi_HTML


def Doc_Du_lieu(Ten_Dang_nhap, Mat_khau, Loai_Nhan_vien):
    Du_lieu = {}
    Doi_tuong_A = {"Ten_Dang_nhap": Ten_Dang_nhap,
                   "Mat_khau": Mat_khau,
                   "Loai_Nhan_vien": Loai_Nhan_vien}
    Ma_so_Xu_ly = "Dang_nhap"
    Dia_chi_Xu_ly = f"{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}"
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A)
    Doi_tuong_B = json.loads(res.text)
    if Doi_tuong_B["Kq"]:
        Du_lieu["Cong_ty"] = Doi_tuong_B["Cong_ty"]
        Du_lieu["Danh_sach_Nhan_vien"] = Doi_tuong_B["Danh_sach_Nhan_vien"]
    else:
        Du_lieu = None

    return Du_lieu


def Ghi_Nhan_vien(Nhan_vien, Thuoc_tinh_can_thay_doi):
    Doi_tuong_A = {"Nhan_vien": Nhan_vien,
                   "Thuoc_tinh_can_thay_doi": Thuoc_tinh_can_thay_doi}
    Ma_so_Xu_ly = "Ghi_Nhan_vien"
    Dia_chi_Xu_ly = f"{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}"
    res = requests.post(Dia_chi_Xu_ly, json=Doi_tuong_A)
    Doi_tuong_B = json.loads(res.text)
    return Doi_tuong_B["Kq"]


def Ghi_Hinh_Nhan_vien(Nhan_vien, Hinh):
    Doi_tuong_A = {"Ma_Nhan_vien": Nhan_vien["Ma_so"]}
    Ma_so_Xu_ly = "Ghi_Hinh_Nhan_vien"
    File_Hinh = {'Th_Hinh': Hinh}
    Dia_chi_Xu_ly = f"{Dia_chi_Dich_vu}/{Ma_so_Xu_ly}"
    res = requests.post(Dia_chi_Xu_ly, data=Doi_tuong_A, files=File_Hinh)
    Doi_tuong_B = json.loads(res.text)
    return Doi_tuong_B["Kq"]
# ================Xử lý biến cố=======================================


class Don_Xin_nghi:
    def __init__(self, Ma_so, Ngay_Bat_dau, So_ngay, Ly_do, Duyet_boi_Quan_li_Chi_nhanh, Duyet_boi_Quan_li_Don_vi, Y_kien_Quan_ly_Chi_nhanh, Y_kien_Quan_ly_Don_vi):
        self.Ma_so = Ma_so
        self.Ngay_Bat_dau = Ngay_Bat_dau
        self.So_ngay = So_ngay
        self.Ly_do = Ly_do
        self.Duyet_boi_Quan_li_Chi_nhanh = Duyet_boi_Quan_li_Chi_nhanh
        self.Duyet_boi_Quan_li_Don_vi = Duyet_boi_Quan_li_Don_vi
        self.Y_kien_Quan_ly_Chi_nhanh = Y_kien_Quan_ly_Chi_nhanh
        self. Y_kien_Quan_ly_Don_vi = Y_kien_Quan_ly_Don_vi


class Y_kien_Don_xin_nghi:
    def __init__(self,  Ngay, Noi_dung):
        self.Ngay = Ngay
        self.Noi_dung = Noi_dung


def Dinh_dang_Ngay(Chuoi_ngay, Dinh_dang_goc, Dinh_dang_moi):
    Chuoi_ngay_theo_dinh_dang = datetime.strptime(
        Chuoi_ngay, Dinh_dang_goc).strftime(Dinh_dang_moi)
    return Chuoi_ngay_theo_dinh_dang


def Xu_ly_Ngay_Bat_dau_nghi(khoang_cach_ngay_toi_thieu=1):
    Ngay_Bat_dau_nghi = datetime.now() + timedelta(days=khoang_cach_ngay_toi_thieu)
    return Ngay_Bat_dau_nghi.strftime("%Y-%m-%d")


def Xu_ly_Boolean(v):
    if v:
        Ton_tai = v.lower() in ("yes", "Yes", "True", "true", "t", "1", "on")
        if Ton_tai:
            return True
        else:
            return False
    else:
        return False

# ================Xử lý nghiệp vụ=======================================


def Tra_cuu_Nhan_vien(Danh_sach_Nhan_vien=[], Chuoi_Tra_cuu=""):
    Danh_sach_Kq = []
    Chuoi_Tra_cuu = Chuoi_Tra_cuu.upper()
    if Chuoi_Tra_cuu:
        for Nhan_vien in Danh_sach_Nhan_vien:
            Ma_so = Nhan_vien["Ma_so"].upper()
            Ten = Nhan_vien["Ho_ten"].upper()

            if Chuoi_Tra_cuu in Ma_so or Chuoi_Tra_cuu in Ten:
                Danh_sach_Kq.append(Nhan_vien)
    else:
        Danh_sach_Kq = Danh_sach_Nhan_vien

    return Danh_sach_Kq


# ================Xử lý thể hiện=======================================

def Tao_Chuoi_HTML_Nhap_lieu_Tieu_chi_Tra_cuu_Nhan_vien(Danh_sach_Nhan_vien):
    Chuoi_HTML = f"""<div style="background-color:gray;margin:10px" >
                       <div class="btn">
                           <form action='/Tra_cuu_Nhan_vien' method='post'>
                                <input style="width:600px" placeholder="Nhập mã số hoặc tên của nhân viên..." name='Th_Chuoi_Tra_cuu' spellcheck="false" autocomplete='off'/>
                          </form>
                      </div>
                      <div class="alert alert-info  align-items-center align-items-center">
                      <div>Danh sách <strong> {len(Danh_sach_Nhan_vien)} </strong> nhân viên</div>
                      </div>
                    </div>"""
    return Chuoi_HTML


def Tao_Chuoi_HTML_Dang_nhap(Ten_Dang_nhap="", Mat_khau="", Thong_bao=""):
    Chuoi_HTML = f""" <form method="post" style="width:450px" action="/Dang_nhap">
  <div class="form-group">
    <label for="Th_Ten_Dang_nhap"><strong> Tên đăng nhập: </strong> </label>
    <input value='{Ten_Dang_nhap}' type="text" class="form-control" required  name="Th_Ten_Dang_nhap">
  </div>
  <div class="form-group">
    <label for="Th_Mat_khau"><strong> Mật khẩu: </strong> </label>
    <input value='{Mat_khau}' type="password" class="form-control" required name="Th_Mat_khau">
  </div>
  <div class="form-group form-check">
   <p class="text-danger">{Thong_bao}</p>
  </div>
  <button type="submit" class="btn btn-danger">Submit</button>
</form> """
    return Chuoi_HTML


def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dien_thoai(Nhan_vien):
    Chuoi_Click = f"""<button style="width:200px" type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown">
    Cập nhật điện thoại</button>"""
    Chuoi_Dropdown = f"""<div style="width:300px" class="dropdown-menu"><form action="/Cap_nhat_Dien_thoai" method="post" class="px-1 py-1"><div class="input-group"><input type="hidden" name="Th_Ma_so" value="{Nhan_vien["Ma_so"]}"/> <input type="text" class="form-control" required name="Th_Dien_thoai" value="{Nhan_vien["Dien_thoai"]}"></div></form></div>"""
    Chuoi_Chuc_nang = f"""<div class="dropdown">{Chuoi_Click}{Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang


def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dia_chi(Nhan_vien):
    Chuoi_Click = f"""<button style="width:200px" type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown">
    Cập nhật địa chỉ</button>"""
    Chuoi_Dropdown = f"""<div style="width:300px" class="dropdown-menu"><form action="/Cap_nhat_Dia_chi" method="post" class="px-1 py-1"><div class="input-group"><input type="hidden" name="Th_Ma_so" value="{Nhan_vien["Ma_so"]}"/><textarea type="text" col="20" row="3" class="form-control" required name="Th_Dia_chi">{Nhan_vien["Dia_chi"]}</textarea></div> <button class="my-2 btn btn-danger" type="submit">Lưu</button></form></div>"""
    Chuoi_Chuc_nang = f"""<div class="dropdown">{Chuoi_Click}{Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang


def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Ngoai_ngu(Nhan_vien, Danh_sach_Ngoai_ngu):
    Chuoi_Click = f"""<button style="width:200px" type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown">
    Cập nhật ngoại ngữ</button>"""

    Chuoi_Danh_sach_Ngoai_ngu = f"""<label for="sel2">Nhấn phím shift để chọn nhiều ngoại ngữ</label>
    <select name="Th_Ngoai_ngu" required multiple class="form-control" id="sel2">"""

    Ton_tai = False
    for Ngoai_ngu in Danh_sach_Ngoai_ngu:
        Ton_tai = False
        for Nhan_vien_Ngoai_ngu in Nhan_vien["Danh_sach_Ngoai_ngu"]:
            if Ngoai_ngu["Ma_so"] == Nhan_vien_Ngoai_ngu["Ma_so"]:
                Chuoi_Danh_sach_Ngoai_ngu += f"""<option selected checked value="{Ngoai_ngu["Ma_so"]}">{Ngoai_ngu["Ten"]}</option>"""
                Ton_tai = True
                break
        if not Ton_tai:
            Chuoi_Danh_sach_Ngoai_ngu += f"""<option value="{Ngoai_ngu["Ma_so"]}">{Ngoai_ngu["Ten"]}</option>"""

    Chuoi_Danh_sach_Ngoai_ngu += f"""</select>"""

    Chuoi_Dropdown = f"""<div style="width:300px" class="dropdown-menu">
    <form  action="/Cap_nhat_Ngoai_ngu" method="post" class="px-1 py-1">
    <input type="hidden" name="Th_Ma_so" value="{Nhan_vien["Ma_so"]}"/>
    {Chuoi_Danh_sach_Ngoai_ngu}
    <button class="my-2 btn btn-danger" type="submit">Lưu</button>
    </form>
    </div>"""
    Chuoi_Chuc_nang = f"""<div class="dropdown">{Chuoi_Click}{Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang


def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Hinh(Nhan_vien):
    Chuoi_Click = f"""<button style="width:200px" type="button" class="btn btn-danger dropdown-toggle" data-toggle="dropdown">
    Cập nhật hình</button>"""
    Chuoi_Dropdown = f"""<div style="width:370px" class="dropdown-menu"><form action="/Cap_nhat_Hinh" enctype="multipart/form-data" method="post" class="px-1 py-1"><div class="input-group"><input type="hidden" name="Th_Ma_so" value="{Nhan_vien["Ma_so"]}"/>
    <input type="file" name="Th_Hinh" id="Th_Hinh" accept="image/png" required name="Th_hinh">
    <button class="btn btn-danger" type="submit">Lưu</button></div>
    </form>
    </div>"""
    Chuoi_Chuc_nang = f"""<div class="dropdown">{Chuoi_Click}{Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang


def Tao_Chuoi_HTML_Danh_sach_Nhan_vien(Danh_sach_Nhan_vien, Danh_sach_Ngoai_ngu):

    Chuoi_Danh_sach = f"""<div class="container-fluid">"""

    for Nhan_vien in Danh_sach_Nhan_vien:

        Ma_so = Nhan_vien["Ma_so"]
        Ho_ten = Nhan_vien["Ho_ten"]
        CMND = Nhan_vien["CMND"]
        Gioi_tinh = Nhan_vien["Gioi_tinh"]
        Ngay_sinh = Nhan_vien["Ngay_sinh"]
        Muc_luong = Nhan_vien["Muc_luong"]
        Dien_thoai = Nhan_vien["Dien_thoai"]
        Mail = Nhan_vien["Mail"]
        Dia_chi = Nhan_vien["Dia_chi"]
        Don_vi = Nhan_vien["Don_vi"]["Ten"]
        Danh_sach_Don_xin_nghi = Nhan_vien["Danh_sach_Don_xin_nghi"]

        Chuoi_Hinh = f"""<img src="{Dia_chi_Media}/{Ma_so}.png?x={randint(0,10000)}" class="mx-auto d-block" width="150" height="150" alt="{Ma_so}">"""
        Chuoi_Ngoai_ngu = ", ".join([Ngoai_ngu['Ten']
                                     for Ngoai_ngu in Nhan_vien['Danh_sach_Ngoai_ngu']])
        Chuoi_Thong_tin = f"""<p><strong>Họ tên: </strong> {Ho_ten} <strong>Giới tính:</strong> {Gioi_tinh} </p> <p><strong>CMND: </strong> {CMND} <strong>Ngày sinh:</strong> {Ngay_sinh} <strong>Mức lương:</strong> {Muc_luong} </p> <p><strong>Điện thoại: </strong> {Dien_thoai} <strong>Mail:</strong> {Mail} </p><p><strong>Địa chỉ: </strong> {Dia_chi} <strong>Đơn vị:</strong> {Don_vi} </p> <p><strong>Ngoại ngữ:</strong> {Chuoi_Ngoai_ngu} </p> """

        Chuoi_Thuc_don = f"""
        <div class="col-3 col-offset-2">{Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dien_thoai(Nhan_vien)}</div>
        <div class="col-3 col-offset-2">{Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Dia_chi(Nhan_vien)}</div>
        <div class="col-3 col-offset-2">{Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Hinh(Nhan_vien)}</div>
        <div class="col-3 col-offset-2">{Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Ngoai_ngu(Nhan_vien, Danh_sach_Ngoai_ngu)}</div> """

        Chuoi_Nhan_vien = f"""<div href=".{Ma_so}" data-toggle="collapse"  class="row my-3 alert-primary">
        <div class="row mx-4 mt-3 {Ma_so} collapse">
        {Chuoi_Thuc_don}
        </div>
        <div class="row mx-1 my-3">
        <div class="col-3 mx-auto d-flex flex-wrap align-items-center text-center">{Chuoi_Hinh}</div>
        <div class="col-9">{Chuoi_Thong_tin}</div>
        </div>
        <div class="row mx-4 mt-2 {Ma_so} collapse">
        <div class="col-12" style="width:1000px">
        <h5>Danh sách đơn xin nghỉ</h5>
        {Tao_Chuoi_HTML_Danh_sach_Don_xin_nghi(Ma_so,Danh_sach_Don_xin_nghi)}
        </div>
        </div>
        </div>
        """
        Chuoi_Danh_sach += Chuoi_Nhan_vien

    Chuoi_Danh_sach += f"""</div>"""
    Chuoi_HTML = f"""{Tao_Chuoi_HTML_Nhap_lieu_Tieu_chi_Tra_cuu_Nhan_vien(Danh_sach_Nhan_vien)}{Chuoi_Danh_sach}"""
    return Chuoi_HTML


def Tao_Chuoi_Dropdown_Chuc_nang_Them_Y_kien_cho_Don_xin_nghi(Ma_Nhan_vien, Don_xin_nghi):
    Ma_so = Don_xin_nghi["Ma_so"]
    Ngay_hien_tai = datetime.now().strftime("%Y-%m-%d")

    Chuoi_Click = f"""<button style="width:200px" type="button" class="my-2 btn btn-danger dropdown-toggle" data-toggle="dropdown">Thêm ý kiến</button>"""
    Chuoi_Dropdown = f"""<div style="width:300px" class="dropdown-menu">
    <form action="/Them_Y_kien_cho_Don_xin_nghi" method="post" class="px-1 py-1">
    <input type="hidden" value="{Ma_Nhan_vien}"  name="Th_Ma_Nhan_vien"/>
    <input type="hidden" value="{Ma_so}"  name="Th_Ma_Don_xin_nghi"/>
    <div class="checkbox">
      <label><input type="checkbox" name="Th_Duyet_Don_xin_nghi" checked>Duyệt đơn xin nghỉ</label>
    </div>
    <div class="form-group"><label for="Th_Ngay_Tao">Ngày tạo</label><input type="date" class="form-control" required name="Th_Ngay_tao" readonly value="{Ngay_hien_tai}"/></div>
    <div class="form-group"><label for="Th_Y_kien">Ý kiến</label><textarea col="2" row="20" class="form-control" required name="Th_Y_kien"></textarea> </div>
    <button class="my-2 btn btn-danger" type="submit">Lưu</button>
    </form>
    </div>"""
    Chuoi_Chuc_nang = f"""<div class="dropdown">{Chuoi_Click}{Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang


def Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Y_kien_cho_Don_xin_nghi(Ma_Nhan_vien, Don_xin_nghi):
    Ma_so = Don_xin_nghi["Ma_so"]
    Y_kien_Quan_ly_Don_vi = Don_xin_nghi["Y_kien_Quan_ly_Don_vi"]
    Duyet_boi_Quan_li_Don_vi = Don_xin_nghi["Duyet_boi_Quan_li_Don_vi"]
    Ngay_tao = Dinh_dang_Ngay(
        Y_kien_Quan_ly_Don_vi["Ngay"], "%d-%m-%Y", "%Y-%m-%d")
    Noi_dung = Y_kien_Quan_ly_Don_vi["Noi_dung"]

    Chuoi_Duyet_boi_Quan_li_Don_vi = f"""<label><input type="checkbox" name="Th_Duyet_Don_xin_nghi">Duyệt đơn xin nghỉ</label>"""
    if Duyet_boi_Quan_li_Don_vi:
        Chuoi_Duyet_boi_Quan_li_Don_vi = f"""<label><input type="checkbox" name="Th_Duyet_Don_xin_nghi" checked>Duyệt đơn xin nghỉ</label>"""

    Chuoi_Click = f"""<button style="width:200px" type="button" class="my-2 btn btn-danger dropdown-toggle" data-toggle="dropdown">Sửa ý kiến</button>"""
    Chuoi_Dropdown = f"""<div style="width:300px" class="dropdown-menu">
    <form action="/Sua_Y_kien_cho_Don_xin_nghi" method="post" class="px-1 py-1">
    <input type="hidden" value="{Ma_Nhan_vien}"  name="Th_Ma_Nhan_vien"/>
    <input type="hidden" value="{Ma_so}"  name="Th_Ma_Don_xin_nghi"/>
    <div class="checkbox">
      {Chuoi_Duyet_boi_Quan_li_Don_vi}
    </div>
    <div class="form-group"><label for="Th_Ngay_Tao">Ngày tạo</label><input type="date" class="form-control" required name="Th_Ngay_tao" readonly value="{Ngay_tao}"/></div>
    <div class="form-group"><label for="Th_Y_kien">Ý kiến</label><textarea col="2" row="20" class="form-control" required name="Th_Y_kien">{Noi_dung}</textarea> </div>
    <button class="my-2 btn btn-danger" type="submit">Lưu</button>
    </form>
    </div>"""
    Chuoi_Chuc_nang = f"""<div class="dropdown">{Chuoi_Click}{Chuoi_Dropdown}</div>"""
    return Chuoi_Chuc_nang


def Tao_Chuoi_HTML_Danh_sach_Don_xin_nghi(Ma_Nhan_vien, Danh_sach_Don_xin_nghi):
    Chuoi_HTML_Danh_sach = f""" <div class="my-4 list-group">"""

    for Don_xin_nghi in Danh_sach_Don_xin_nghi:
        Ngay_Bat_dau = Don_xin_nghi["Ngay_Bat_dau"]
        So_ngay = Don_xin_nghi["So_ngay"]
        Ly_do = Don_xin_nghi["Ly_do"]
        Y_kien_Quan_ly_Chi_nhanh = "Chưa có"
        Y_kien_Quan_ly_Don_vi = "Chưa có"
        Duyet_boi_Quan_li_Don_vi = Don_xin_nghi["Duyet_boi_Quan_li_Don_vi"]

        if Don_xin_nghi["Y_kien_Quan_ly_Chi_nhanh"]:
            Y_kien_Quan_ly_Chi_nhanh = f"""{Don_xin_nghi["Y_kien_Quan_ly_Chi_nhanh"]["Noi_dung"]} <i>({Don_xin_nghi["Y_kien_Quan_ly_Chi_nhanh"]["Ngay"]})</i>"""
        if Don_xin_nghi["Y_kien_Quan_ly_Don_vi"]:
            Y_kien_Quan_ly_Don_vi = f"""{Don_xin_nghi["Y_kien_Quan_ly_Don_vi"]["Noi_dung"]} <i>({Don_xin_nghi["Y_kien_Quan_ly_Don_vi"]["Ngay"]})</i>"""

        if Y_kien_Quan_ly_Don_vi == "Chưa có":
            Chuoi_HTML_Thuc_don = f"""<div class="row">
            <div class="col-12">{Tao_Chuoi_Dropdown_Chuc_nang_Them_Y_kien_cho_Don_xin_nghi(Ma_Nhan_vien,Don_xin_nghi)}</div>
            </div>"""
        else:
            Chuoi_HTML_Thuc_don = f"""<div class="row">
            <div class="col-12">{Tao_Chuoi_Dropdown_Chuc_nang_Cap_nhat_Y_kien_cho_Don_xin_nghi(Ma_Nhan_vien,Don_xin_nghi)}</div>
            </div>"""

        if Duyet_boi_Quan_li_Don_vi:
            Chuoi_HTML_Thuc_don = ""

        Chuoi_HTML = f"""<div class="list-group-item">
        {Chuoi_HTML_Thuc_don}
        <p><strong>Ngày bắt đầu: </strong>{Ngay_Bat_dau}</p>
        <p><strong>Số ngày: </strong>{So_ngay} </p>
        <p><strong>Lý do: </strong>{Ly_do} </p>
        <p><strong>Ý kiến của Quản lý đơn vị: </strong> {Y_kien_Quan_ly_Don_vi} </p>
        <p><strong>Ý kiến của Quản lý chi nhánh: </strong> {Y_kien_Quan_ly_Chi_nhanh} </p>
        </div>"""

        Chuoi_HTML_Danh_sach += Chuoi_HTML

    Chuoi_HTML_Danh_sach += f"""</div>"""
    return Chuoi_HTML_Danh_sach
