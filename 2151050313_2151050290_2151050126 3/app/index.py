import math
from flask import render_template, request, redirect, session, jsonify, url_for
import dao
import utils
from app import app, login
from flask_login import login_user, logout_user, login_required



@app.route('/')
def index():
    kw = request.args.get('kw')
    cate_id = request.args.get('cate_id')
    page = request.args.get("page")
    products = dao.load_products(kw=kw, cate_id=cate_id, page=page)

    total = dao.count_product()

    return render_template('index.html',
                           products=products,
                           pages=math.ceil(total/app.config['PAGE_SIZE']))




@app.route("/login", methods=['get', 'post'])
def login_user_process():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

        next = request.args.get('next')
        return redirect("/" if next is None else next)

    return render_template('login.html')


@app.route('/logout')
def process_logout_user():
    logout_user()
    return redirect("/login")


@app.route('/admin/login', methods=['post'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_admin(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@app.route('/api/cart', methods=['post'])
def add_cart():
    """
    {
    "cart": {
            "1": {
                "id": 1,
                "name": "ABC",
                "price": 12,
                "quantity": 2
            }, "2": {
                "id": 2,
                "name": "ABC",
                "price": 12,
                "quantity": 2
            }
        }
    }
    :return:
    """
    cart = session.get('cart')
    if cart is None:
        cart = {}

    data = request.json
    id = str(data.get("id"))

    if id in cart: # Phòng đã chọn trong gio
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else: # phong chua co trong gio
        cart[id] = {
            "id": id,
            "name": data.get("name"),
            "price": data.get("price"),
            "quantity": 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<product_id>", methods=['put'])
def update_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        quantity = request.json.get('quantity')
        cart[product_id]['quantity'] = int(quantity)

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/cart/<product_id>", methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')
    if cart and product_id in cart:
        del cart[product_id]

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/pay', methods=['post'])
def pay():
    try:
        dao.add_receipt(session.get('cart'))
    except:
        return jsonify({'status': 500, 'err_msg': 'Hệ thống đang có lỗi!'})
    else:
        del session['cart']
        return jsonify({'status': 200})


@app.route('/cart')
def cart_list():
    return render_template('cart.html')

@app.context_processor
def common_resp():
    return {
        'categories': dao.load_categories(),
        'cart': utils.count_cart(session.get('cart'))
    }


@app.route('/products/<id>')
def details(id):
    comments = dao.get_comments_by_prod_id(id)
    return render_template('details.html', product=dao.get_product_by_id(id), comments=comments)


@app.route("/api/products/<id>/comments", methods=['post'])
@login_required
def add_comment(id):
    content = request.json.get('content')

    try:
        c = dao.add_comment(room_id=id, content=content)
    except:
        return jsonify({'status': 200, "c": {'content': c.content, "user": {"avatar": c.user.avatar}}})
    else:
        return jsonify({'status': 500, 'err_msg': 'Hệ thống đang có lỗi!'})


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)