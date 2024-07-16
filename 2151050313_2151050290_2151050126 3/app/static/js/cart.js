function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity
    })
}

function updateCart(id, obj) {
    obj.disabled = true;
    fetch(`/api/cart/${id}`, {
        method: 'put',
        body: JSON.stringify({
            'quantity': obj.value
        }),  headers: {
            'Content-Type': "application/json"
        }
    }).then(res => res.json()).then(data => {
        obj.disabled = false;
        let c = document.getElementsByClassName('cart-counter');
        for (let d of c)
            d.innerText = data.total_quantity
    });
}

function deleteCart(id, obj) {
    if (confirm("Ban chac chan xoa khong?") === true) {
        obj.disabled = true;
        fetch(`/api/cart/${id}`, {
            method: 'delete'
        }).then(res => res.json()).then(data => {
            obj.disabled = false;
            let c = document.getElementsByClassName('cart-counter');
            for (let d of c)
                d.innerText = data.total_quantity

            let r = document.getElementById(`product${id}`);
            r.style.display = "none";
        });
    }
}

function pay() {
    if (confirm("Bạn chắc chắn đặt phòng!") === true) {
        fetch("/api/pay", {
            method: "post"
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert(data.err_msg);
        })
    }
}


function addComment(productId) {
    if (confirm("Bạn chắc chắn bình luận?") == true) {
        fetch(`/api/products/${productId}/comments`, {
            method: "post",
            body: JSON.stringify({
                "content": document.getElementById("comment").value
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(res => res.json()).then(data => {
            if (data.status === 200) {
                let d = document.getElementById("comments");
                let c = data.c;
                d.innerHTML = `
                 <div class="row alert alert-info">
                    <div class="col-md-1">
                        <img src="${c.user.avatar}" class="img-fluid rounded" />
                    </div>
                    <div class="col-md-11">
                        <p>${ c.content }</p>
                        <p>Bình luân lúc: <span class="my-date">${  moment(c.created_date).locale("vi").fromNow() }</span></p>
                    </div>
                </div>
                `  + d.innerHTML;
            }
        })
    }
}
