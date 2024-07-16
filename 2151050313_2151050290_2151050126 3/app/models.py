from collections import defaultdict

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)


# Loại khách hàng
class LoaiKH(db.Model):
    # __tablename__ = 'LoaiKH'
    maLKH = Column(Integer, primary_key=True, autoincrement=True)
    tenLKH = Column(String(50))
    kh = relationship('KhachHang', backref='loaikhachhang', lazy=True)

    def __str__(self):
        return self.name


# Tài khoản
class TaiKhoan(db.Model, UserMixin):
    # __tablename__ = 'TaiKhoan'
    maTK = Column(Integer, primary_key=True, autoincrement=True)
    tenTK = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)

    # 1-1
    # kh_id = Column(Integer, ForeignKey(KhachHang.maKH), nullable=False)
    kh = relationship('KhachHang', backref='tk', uselist=False, lazy=True)
    nv = relationship('NhanVien', backref='tk', uselist=False, lazy=True)
    nguoiqt = relationship('NguoiQuanTri', backref='tk',uselist=False, lazy=True)
    # kh_id = Column(Integer, ForeignKey('khachhang.maKH'), nullable=False)
    # avatar = Column(String(100),
    #                 default='https://hoanghamobile.com/tin-tuc/wp-content/uploads/2023/07/avatar-dep-13-1.jpg')
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name

    def get_id(self):
        return str(self.maTK)


# Nhân viên
class NhanVien(db.Model):
    # __tablename__ = 'NhanVien'
    maNV = Column(Integer, primary_key=True, autoincrement=True)
    tenNV = Column(String(50))
    pdp = relationship('PhieuDatPhong', backref='NhanVien')
    ptp = relationship('PhieuThuePhong', backref='NhanVien')
    hd = relationship('HoaDon', backref='NhanVien')
    tk_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)
    def __str__(self):
        return self.name


# # Phiếu thuê phòng
class PhieuThuePhong(db.Model):
    # __tablename__ = 'PhieuThuePhong'
    maPTP = Column(Integer, primary_key=True, autoincrement=True)
    ngayNhanPhong = Column(DateTime)
    ngayTraPhong = Column(DateTime)
    phong = relationship('ChiTietPhieuThue', backref="phieuthuephong")
    nv_id = Column(Integer, ForeignKey(NhanVien.maNV), nullable=False)
    kh = relationship('KhachHang', backref='phieuthuephong')
    hd = relationship('HoaDon', backref='phieuthuephong')
    def __str__(self):
        return self.name


# Phiếu đặt phòng
class PhieuDatPhong(db.Model):
    # __tablename__ = 'PhieuDatPhong'
    maPDP = Column(Integer, primary_key=True, autoincrement=True)
    ngayNhanPhong = Column(DateTime)
    ngayTraPhong = Column(DateTime)
    phong = relationship('ChiTietPhieuDat', backref="phieudatphong")
    nv_id = Column(Integer, ForeignKey(NhanVien.maNV), nullable=False)
    kh = relationship('KhachHang', backref='phieudatphong')

    def __str__(self):
        return self.name





# Khách hàng
class KhachHang(db.Model):
    # __tablename__ = 'KhachHang'
    maKH = Column(Integer, primary_key=True, autoincrement=True)
    hoTenKH = Column(String(50))
    diaChi = Column(String(100))
    soCCCD = Column(String(20))
    loaikh_id = Column(Integer, ForeignKey(LoaiKH.maLKH), nullable=False)
    hd = relationship('HoaDon', backref='kh', lazy=True)

    ptp_id = Column(Integer, ForeignKey(PhieuThuePhong.maPTP), nullable=False)
    pdp_id = Column(Integer, ForeignKey(PhieuDatPhong.maPDP), nullable=False)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)

    def __str__(self):
        return self.hoTenKH

    def __str__(self):
        return self.maKH


# Hóa đơn
class HoaDon(db.Model):
    # __tablename__ = 'HoaDon'
    maHD = Column(Integer, primary_key=True, autoincrement=True)
    ngayVao = Column(DateTime)
    ngayRa = Column(DateTime)
    kh_id = Column(Integer, ForeignKey(KhachHang.maKH), nullable=False)
    nv_id = Column(Integer, ForeignKey(NhanVien.maNV), nullable=False)
    ptp = Column(Integer, ForeignKey(PhieuThuePhong.maPTP), nullable=False)
    # ptp_id
    def __str__(self):
        return self.maHD


# Loại Phòng
class LoaiPhong(db.Model):
    # __tablename__ = 'LoaiPhong'
    maLP = Column(Integer, primary_key=True, autoincrement=True)
    tenLP = Column(String(50), nullable=False, unique=True)
    phongs = relationship('Phong', backref='loaiphong', cascade='delete', lazy=True)

    def __str__(self):
        return self.tenLP


# Người quản trị
class NguoiQuanTri(db.Model):
    # __tablename__ = 'NguoiQuanTri'
    maQT = Column(Integer, primary_key=True, autoincrement=True)
    tenQT = Column(String(50))
    phong = relationship('Phong', backref='nguoiQT', lazy=True)
    quydinh = relationship('QuyDinh', backref='nguoiQT', lazy=True)
    tk_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)
    def __str__(self):
        return self.tenQT


# Phòng
class Phong(db.Model):
    # __tablename__ = 'Phong'
    maPhong = Column(Integer, primary_key=True, autoincrement=True)
    tenPhong = Column(String(50), nullable=False, unique=True)
    giaPhong = Column(Float, default=0)
    hinhAnh = Column(String(100))
    dienTich = Column(Float, default=0)
    # tinhTrang=Column(String(50))
    loaiphong_id = Column(Integer, ForeignKey(LoaiPhong.maLP), nullable=False)
    nguoiqt_id = Column(Integer, ForeignKey(NguoiQuanTri.maQT), nullable=False)
    # n-n
    ptp = relationship('ChiTietPhieuThue', cascade='delete', backref='phong')
    pdp = relationship('ChiTietPhieuDat', cascade='delete', backref='phong')

    receipt_details = relationship('ReceiptDetails', cascade='delete', backref='phong', lazy=True)
    comments = relationship('Comment', cascade='delete', backref='phong', lazy=True)

    def __str__(self):
        return self.tenPhong


# Chi tiết phiếu thuê
class ChiTietPhieuThue(db.Model):
    # __tablename__ = 'ChiTietPTP'
    id = Column(Integer, primary_key=True, autoincrement=True)
    left_id = Column(ForeignKey(PhieuThuePhong.maPTP), nullable=False)
    right_id = Column(ForeignKey(Phong.maPhong), nullable=False)

    # def __str__(self):
    #     return self.id


# Chi tiết phiếu đặt
class ChiTietPhieuDat(db.Model):
    # __tablename__ = 'ChiTietPDP'
    id = Column(Integer, primary_key=True, autoincrement=True)
    left_id = Column(ForeignKey(PhieuDatPhong.maPDP), nullable=False)
    right_id = Column(ForeignKey(Phong.maPhong),nullable=False)

    # def __str__(self):
    #     return self.name


# Quy định
class QuyDinh(db.Model):
    # __tablename__ = 'QuyDinh'
    maQD = Column(Integer, primary_key=True, autoincrement=True)
    tenQD = Column(String(100))
    noiDungQD = Column(String(200))
    nguoiQT_id = Column(Integer, ForeignKey(NguoiQuanTri.maQT), nullable=False)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    user_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Phong.maPhong), nullable=False)


class Interaction(BaseModel):
    __abstract__ = True

    room_id = Column(Integer, ForeignKey(Phong.maPhong), nullable=False)
    user_id = Column(Integer, ForeignKey(TaiKhoan.maTK), nullable=False)


class Comment(Interaction):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()

# Thêm tài khoản admin
#     import hashlib
#
#     u = TaiKhoan(tenTK='Admin',
#                  username='admin',
#                  password=str(hashlib.md5('1234567'.encode('utf-8')).hexdigest()),
#                  user_role=UserRoleEnum.ADMIN)
#
#     db.session.add(u)
#     db.session.commit()

            # import hashlib
            #
            # u = TaiKhoan(tenTK='MyNhan',
            #              username='mynhan',
            #              password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
            #              user_role=UserRoleEnum.USER)
            #
            # db.session.add(u)
            # db.session.commit()
            # import hashlib
            #
            # u = TaiKhoan(tenTK='MinhNhut',
            #              username='minhnhut',
            #              password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
            #              user_role=UserRoleEnum.USER)
            #
            # db.session.add(u)
            # db.session.commit()
            # import hashlib
            #
            # u = TaiKhoan(tenTK='ThuHien',
            #              username='thuhien',
            #              password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
            #              user_role=UserRoleEnum.USER)
            #
            # db.session.add(u)
            # db.session.commit()

            # import hashlib
            #
            # u = TaiKhoan(tenTK='NhanVien1',
            #              username='nhanvien1',
            #              password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
            #              user_role=UserRoleEnum.USER)
            #
            # db.session.add(u)
            # db.session.commit()
            # Thêm người quản trị
            #     qt1 = NguoiQuanTri(tenQT='admin1', tk_id=1)
            #
            #     db.session.add(qt1)
            #     db.session.commit()

            # Thêm loại phòng
            #         l1 = LoaiPhong(tenLP='Phòng 1 giường')
            #         l2 = LoaiPhong(tenLP='Phòng 2 giường')
            #
            #         db.session.add(l1)
            #         db.session.add(l2)
            #         db.session.commit()

            # Thêm nhân viên
            #     nv1 = NhanVien(tenNV='Nguyen Van A', tk_id=6)
            #     db.session.add(nv1)
            #     db.session.commit()
                # nv2 = NhanVien(tenNV='Tran Thi B')
                # db.session.add(nv2)
                # db.session.commit()

    # Thêm phòng
    #         p1 = Phong(tenPhong='Phòng 1 giường đôi cao cấp', giaPhong=1300000,
    #                    hinhAnh="https://www.cet.edu.vn/wp-content/uploads/2018/01/cac-loai-giuong-trong-khach-san.jpg",
    #                    dienTich=20.2,
    #                    loaiphong_id=1,
    #                    nguoiqt_id=1)
    #
    #         p2 = Phong(tenPhong='Phòng 2 giường ', giaPhong=2000000,
    #                    hinhAnh="https://noithatmyhouse.net/wp-content/uploads/2019/10/giuong-ngu-khach-san_11.jpg",
    #                    dienTich=27.0,
    #                    loaiphong_id=2,
    #                    nguoiqt_id=1)
    #         p3 = Phong(tenPhong='Phòng 1 giường đơn', giaPhong=850000,
    #                    hinhAnh="https://chefjob.vn/wp-content/uploads/2020/07/tieng-anh-loai-phong-khach-san.jpg",
    #                    dienTich=15.5,
    #                    loaiphong_id=1,
    #                    nguoiqt_id=1)
    #         p4 = Phong(tenPhong='Phòng 2 giường cao cấp ', giaPhong=2500000,
    #                    hinhAnh="https://decoxdesign.com/upload/images/hotel-caitilin-1952m2-phong-ngu-06-decox-design.jpg",
    #                    dienTich=25.2,
    #                    loaiphong_id=2,
    #                    nguoiqt_id=1)
    #         p5 = Phong(tenPhong='Phòng 1 giường đôi view biển', giaPhong=1500000,
    #                    hinhAnh="https://www.hoteljob.vn/files/Anh-HTJ-Hong/tieu-chi-can-co-trong-thiet-ke-phong-khach-san-1.jpg",
    #                    dienTich=12.5,
    #                    loaiphong_id=1,
    #                    nguoiqt_id=1)
    #         p6 = Phong(tenPhong='Phòng 1 giường đôi đầy đủ nội thất', giaPhong=1200000,
    #                    hinhAnh="https://tubepfurniture.com/wp-content/uploads/2020/09/phong-mau-khach-san-go-cong-nghiep-01.jpg",
    #                    dienTich=15.2,
    #                    loaiphong_id=1,
    #                    nguoiqt_id=1)
    #         p7 = Phong(tenPhong='Phòng 2 giường đơn', giaPhong=1300000,
    #                    hinhAnh="https://everon.com/upload_images/images/noi-that-phong-ngu-khach-san/phong-ngu-khach-san-2.jpg",
    #                    dienTich=20.2,
    #                    loaiphong_id=2,
    #                    nguoiqt_id=1)
    #         p8 = Phong(tenPhong='Phòng 2 giường đôi và đơn', giaPhong=1800000,
    #                    hinhAnh="https://www.hoteljob.vn/files/VB2-%E1%BA%A3nh%20HTJ/cac-loai-phong-trong-khach-san-2.jpg",
    #                    dienTich=23.2,
    #                    loaiphong_id=2,
    #                    nguoiqt_id=1)
    #
    #         db.session.add_all([p1,p2, p3, p4, p5, p6, p7, p8])
    #         db.session.commit()

    # Thêm loại khách hàng
    #     kh1 = LoaiKH(tenLKH='Trong nước')
    #     kh2 = LoaiKH(tenLKH='Nước ngoài')
    #     db.session.add(kh1)
    #     db.session.add(kh2)
    #     db.session.commit()


# Phiếu đặt phòng
#                 pdp1 = PhieuDatPhong(ngayNhanPhong='2023-11-11 12:00:00', ngayTraPhong='2023-11-15 13:00:00',
#                                     nv_id=1)
#                 db.session.add(pdp1)
#                 db.session.commit()


# Phiếu thuê phòng
#                 pdp1 = PhieuThuePhong(ngayNhanPhong='2023-11-11 12:00:00', ngayTraPhong='2023-11-15 13:00:00',
#                                     nv_id=1)
#                 db.session.add(pdp1)
#                 db.session.commit()

                # Thêm khách hàng
                # kh1 = KhachHang(hoTenKH='Tran Thi B', diaChi='TP.HCM', soCCCD='123456789987', loaikh_id=1, ptp_id=1,pdp_id=1,tk_id=2)
                # db.session.add(kh1)
                # db.session.commit()

                # Thêm HoaDon
                # hd1 = HoaDon(ngayVao='2023-11-11 12:00:00', ngayRa='2023-11-15 13:00:00', kh_id=1, nv_id=1,ptp=1)
                # db.session.add(hd1)
                # db.session.commit()

                # Chi tiết phiếu đặt
                # ctpd1 = ChiTietPhieuDat(left_id=1,right_id=1)
                # db.session.add(ctpd1)
                # db.session.commit()

                # Chi tiết phiếu thuê
                # ctpt1 = ChiTietPhieuThue(left_id=1,right_id=1)
                # db.session.add(ctpt1)
                # db.session.commit()