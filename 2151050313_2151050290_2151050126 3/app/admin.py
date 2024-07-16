from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app import app, db, dao
from app.models import LoaiPhong, Phong
from flask_login import logout_user, current_user
from flask import redirect, request

from app.models import UserRoleEnum


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_products_by_cate())


admin = Admin(app=app, name='KHÁCH SẠN MÂY TRẮNG', template_mode='bootstrap4', index_view=MyAdminIndex())


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class MyProductView(AuthenticatedAdmin):
    column_display_pk = True
    column_list = ['tenPhong', 'giaPhong', 'dienTich', 'loaiphong']
    column_searchable_list = ['tenPhong']
    column_filters = ['giaPhong', 'tenPhong', 'dienTich']
    can_export = True
    can_view_details = True

    def is_accessible(self):
        return current_user.is_authenticated


class MyCategoryView(AuthenticatedAdmin):
    column_list = ['tenLP', 'phongs']


class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        kw = request.args.get("kw")
        return self.render('admin/stats.html',
                           stats=dao.revenue_stats(),
                           month_stats = dao.revenue_stats_by_month())


class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(MyCategoryView(LoaiPhong, db.session, category='Quản Lý Danh Sách Phòng'))
admin.add_view(MyProductView(Phong, db.session, category='Quản Lý Danh Sách Phòng'))
admin.add_view(MyStatsView(name='Thống Kê Báo Cáo'))
admin.add_view(MyLogoutView(name='Đăng Xuất'))
