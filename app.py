from flask import Flask, request, render_template_string
app = Flask(__name__)
announcement = "Karibu! Leo tuna Pilau, Chapo na Ugali Beef! Orders 7am-8pm"
restock_info = "Pilau itarudi saa 1pm"
pochi = "0799587489"
menu = {
    "Chapati": {"price": 20, "stock": 55},
    "Beans + Chapo": {"price": 80, "stock": 20},
    "Pilau Regular": {"price": 80, "stock": 15},
    "Pilau Large": {"price": 100, "stock": 15},
    "Mandazi": {"price": 10, "stock": 100},
    "Tea": {"price": 20, "stock": 100},
    "Chapo Chipo": {"price": 60, "stock": 25},
    "Chips Small": {"price": 60, "stock": 20},
    "Chips Medium": {"price": 80, "stock": 20},
    "Chips Large": {"price": 100, "stock": 20},
    "Ugali Beef": {"price": 150, "stock": 15},
    "Soda (Fanta)": {"price": 50, "stock": 30},
    "Pepsi": {"price": 40, "stock": 30},
    "Predator": {"price": 70, "stock": 25},
    "Minute Maid": {"price": 80, "stock": 20},
    "Yoghurt": {"price": 60, "stock": 20},
    "Sausage": {"price": 40, "stock": 30},
    "Samosa": {"price": 40, "stock": 30},
}
orders=[]
CUSTOMER="""<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gracie-Ruth</title><style>
body{background:#f5f5f0;font-family:Arial;padding:12px;margin:0;padding-bottom:80px}
.header{background:#fff9c4;padding:10px;border-radius:8px;border:2px solid #f0c040;text-align:center}
.pochi{background:#2d5016;color:white;padding:12px;border-radius:8px;margin:10px 0;text-align:center;font-size:18px;font-weight:bold}
.item{background:white;display:flex;justify-content:space-between;align-items:center;padding:12px;margin:6px 0;border-radius:12px;box-shadow:0 2px 4px #ccc}
.add{background:#e65100;color:white;border:none;padding:8px 16px;border-radius:8px;font-weight:bold}
h1{color:#bf360c}.cart-bar{position:fixed;bottom:0;left:0;right:0;background:#2d5016;color:white;padding:15px;text-align:center;font-size:18px;font-weight:bold;display:none;cursor:pointer}
#cartModal{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);padding:20px;overflow:auto;z-index:999}
.cart-box{background:white;padding:20px;border-radius:12px;max-width:400px;margin:20px auto}
input{width:90%;padding:10px;margin:5px 0}.order-btn{background:#2d5016;color:white;padding:12px;width:100%;border:none;border-radius:8px;font-size:18px;margin-top:10px}
</style></head><body>
<div class="header">Restock: {{restock}}<br>{{ann}}</div>
<div class="pochi">Pochi: {{pochi}} - Lipa na Pochi</div>
<h1>Menu Leo</h1>
{% for name, d in menu.items() %}
<div class="item"><span><b>{{name}}</b> - Ksh {{d.price}} {% if d.stock==0 %} Imeisha {% endif %}</span><button class="add" onclick="addToCart('{{name}}',{{d.price}})" {% if d.stock==0 %}disabled{% endif %}>Add</button></div>
{% endfor %}
<div class="cart-bar" id="cartBar" onclick="openCart()">View Cart (<span id="cartCount">0</span>) - Ksh <span id="cartTotal">0</span></div>
<div id="cartModal"><div class="cart-box"><h2>Your Cart</h2><div id="cartItems"></div><hr><h3>Total: Ksh <span id="modalTotal">0</span></h3>
<input id="custName" placeholder="Your Name"><input id="custPhone" placeholder="Phone"><input id="custRoom" placeholder="Hostel/Room">
<button class="order-btn" onclick="placeOrder()">Order Now via WhatsApp</button>
<button onclick="closeCart()" style="width:100%;padding:10px;margin-top:10px">Continue Shopping</button></div></div>
<script>
let cart=[];function addToCart(n,p){let f=cart.find(i=>i.name==n);if(f){f.qty++}else{cart.push({name:n,price:p,qty:1})}updateCart()}
function updateCart(){let c=0,t=0,h='';cart.forEach((it,i)=>{c+=it.qty;t+=it.price*it.qty;h+=`<div style="display:flex;justify-content:space-between;margin:8px 0"><span>${it.name} x${it.qty}</span><span>Ksh ${it.price*it.qty} <button onclick="removeItem(${i})">x</button></span></div>`});
document.getElementById('cartCount').innerText=c;document.getElementById('cartTotal').innerText=t;document.getElementById('modalTotal').innerText=t;
document.getElementById('cartItems').innerHTML=h||'Empty';document.getElementById('cartBar').style.display=c>0?'block':'none';}
function removeItem(i){cart.splice(i,1);updateCart()}function openCart(){document.getElementById('cartModal').style.display='block'}function closeCart(){document.getElementById('cartModal').style.display='none'}
function placeOrder(){let name=document.getElementById('custName').value;let phone=document.getElementById('custPhone').value;let room=document.getElementById('custRoom').value;if(!name||!phone){alert('Weka Name na Phone');return}
let total=document.getElementById('modalTotal').innerText;let items=cart.map(i=>`${i.name} x${i.qty}`).join(', ');let msg=`*NEW ORDER*%0AName: ${name}%0APhone: ${phone}%0ARoom: ${room}%0AOrder: ${items}%0ATotal: Ksh ${total}`;
fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name,phone:phone,room:room,items:items,total:total})});
window.open(`https://wa.me/254799587489?text=${msg}`,'_blank');alert('Asante! Order sent!');cart=[];updateCart();closeCart();}
</script></body></html>"""
BOSS="""<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>BOSS</title>
<style>body{background:#fff8e1;font-family:Arial;padding:10px}.card{background:white;padding:12px;border-radius:10px;margin-bottom:10px;box-shadow:0 2px 4px #ccc}
.btn{padding:6px 10px;border:none;border-radius:6px;margin:2px;color:white;font-weight:bold}.black{background:#212121}.green{background:#2e7d32}.red{background:#6d1b1b}
input{padding:8px;margin:4px;width:95%}.update{background:#2e7d32;color:white;padding:12px;width:100%;border:none;border-radius:8px;margin-top:8px}</style></head><body>
<div class="card"><b>GRACIE BOSS CONTROL</b> | <a href="/">View Menu</a></div>
<div class="card" style="background:#fff9c4;border:2px solid #f0c040"><h3>Update Message</h3><form method="post">
Cooking:<br><input type="text" name="ann" value="{{ann}}"><br>Restock:<br><input type="text" name="restock" value="{{restock}}"><br><button class="update">Update</button></form></div>
<h2>Stock Control</h2>{% for name, d in menu.items() %}<div class="card" style="display:flex;justify-content:space-between;align-items:center"><div><b>{{name}} - Ksh {{d.price}} | Stock: {{d.stock}}</b></div>
<div><a href="/kitchen/decrease/{{name}}"><button class="btn black">-1</button></a><a href="/kitchen/increase/{{name}}"><button class="btn green">+5</button></a><a href="/kitchen/zero/{{name}}"><button class="btn red">Imeisha</button></a></div></div>{% endfor %}
<div class="card"><h3>Orders: {{orders|length}}</h3>{% for o in orders %}<p>{{o.name}} - {{o.phone}} - {{o.items}} - Ksh {{o.total}}</p>{% endfor %}</div></body></html>"""
@app.route('/')
def home(): return render_template_string(CUSTOMER, menu=menu, ann=announcement, restock=restock_info, pochi=pochi)
@app.route('/kitchen')
def kitchen(): return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/kitchen', methods=['POST'])
def kitchen_post():
    global announcement, restock_info
    announcement=request.form.get('ann',announcement);restock_info=request.form.get('restock',restock_info)
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/order', methods=['POST'])
def order(): data=request.get_json();
    if data: orders.append(data)
    return "ok"
@app.route('/kitchen/increase/<name>')
def inc(name):
    if name in menu: menu[name]['stock']+=5
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/kitchen/decrease/<name>')
def dec(name):
    if name in menu and menu[name]['stock']>0: menu[name]['stock']-=1
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/kitchen/zero/<name>')
def zero(name):
    if name in menu: menu[name]['stock']=0
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
if __name__=='__main__': app.run(host='0.0.0.0', port=5000, debug=True)
