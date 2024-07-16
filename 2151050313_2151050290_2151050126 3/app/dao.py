from app.models import LoaiPhong, Phong, TaiKhoan, Receipt, ReceiptDetails, Enum, UserRoleEnum, Comment
from app import app, db
import hashlib
import cloudinary.uploader
from flask_login import current_user
from sqlalchemy import func


def load_categories():
    return LoaiPhong.query.all()


def load_products(kw=None, cate_id=None, page=None):
    products = Phong.query

    if kw:
        products = products.filter(Phong.tenPhong.contains(kw))

    if cate_id:
        products = products.filter(Phong.loaiphong_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1) * page_size
        return products.slice(start, start + page_size)

    return products.all()


def count_product():
    return Phong.query.count()


def get_user_by_id(id):
    return TaiKhoan.query.get(id)


def get_comments_by_prod_id(id):
    return Comment.query.filter(Comment.room_id.__eq__(id)).all()


def add_comment(room_id, content):
    c = Comment(user=current_user, room_id=room_id, content=content)
    db.session.add(c)
    db.session.commit()
    return c


def get_product_by_id(id):
    return Phong.query.get(id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                                 TaiKhoan.password.__eq__(password)).first()


def auth_admin(username, password, role=UserRoleEnum.ADMIN):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                                 TaiKhoan.password.__eq__(password),
                                 TaiKhoan.user_role.__eq__(role)).first()


# def add_user(name, username, password, avatar):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#     u = TaiKhoan(TenTK=name, username=username, password=password)
#     if avatar:
#         res = cloudinary.uploader.upload(avatar)
#         print(res)
#         u.avatar = res['secure_url']
#
#     db.session.add(u)
#     db.session.commit()

def count_products_by_cate():
    return db.session.query(LoaiPhong.maLP, LoaiPhong.tenLP, func.count(Phong.maPhong)) \
        .join(Phong, Phong.loaiphong_id == LoaiPhong.maLP, isouter=True).group_by(LoaiPhong.maLP).all()


def revenue_stats(kw=None):
    query = db.session.query(Phong.maPhong, Phong.tenPhong, func.sum(ReceiptDetails.price * ReceiptDetails.quantity)) \
        .join(ReceiptDetails, ReceiptDetails.product_id == Phong.maPhong).group_by(Phong.maPhong)
    if kw:
        query = query.filter(Phong.tenPhong.contains(kw))

    return query


def revenue_stats_by_month(year=2024):
    return db.session.query(func.extract('month', Receipt.created_date),
                            func.sum(ReceiptDetails.price * ReceiptDetails.quantity)) \
        .join(ReceiptDetails, ReceiptDetails.receipt_id == Receipt.id) \
        .filter(func.extract('year', Receipt.created_date) == year) \
        .group_by(func.extract('month', Receipt.created_date)).all()


def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()
