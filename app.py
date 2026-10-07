from flask import Flask, request, render_template_string, jsonify
app = Flask(__name__)

announcement = "Karibu! Leo tuna Pilau, Chapo na Ugali Beef!"
restock_info = "Orders 8AM - 8PM ONLY - Karibu!"
pochi = "0799587489"
orders = []

menu = {
    "Chapati": {"price": 20, "stock": 55},
    "Beans Chapo": {"price": 80, "stock": 20},
    "Pilau Regular": {"price": 80, "stock": 15},
    "Pilau Large": {"price": 100, "stock": 15},
    "Mandazi": {"price": 10, "stock": 100},
    "Tea": {"price": 20, "stock": 100},
    "Chapo Chipo": {"price": 60, "stock": 25},
    "Chips Small": {"price": 60, "stock": 20},
    "Chips Medium": {"price": 80, "stock": 20},
    "Chips Large": {"price": 100, "stock": 20},
    "Ugali Beef": {"price": 150, "stock": 15},
    "Soda Fanta": {"price": 50, "stock": 30},
    "Pepsi": {"price": 40, "stock": 30},
    "Predator": {"price": 70, "stock": 25},
    "Minute Maid": {"price": 80, "stock": 20},
    "Yoghurt": {"price": 60, "stock": 20},
    "Sausage": {"price": 40, "stock": 30},
    "Samosa": {"price": 40, "stock": 30},
}

CUSTOMER = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gracie</title><style>
body{font-family:Arial;background:#f5f5f0;margin:0;padding:10px;padding-bottom:120px}
.top{background:#fff9c4;border:2px solid gold;padding:10px;border-radius:10px;text-align:center}
.pochi{background:#2d5016;color:white;padding:14px;border-radius:10px;text-align:center;font-size:20px;font-weight:bold;margin:10px 0}
.item{background:white;padding:15px;margin:8px 0;border-radius:12px;display:flex;justify-content:space-between;box-shadow:0 2px 4px #ccc}
.btn{background:#e65100;color:white;border:none;padding:12px 18px;border-radius:10px;font-weight:bold}
#cartBar{position:fixed;bottom:0;left:0;right:0;background:#2d5016;color:white;padding:20px;text-align:center;font-size:22px;font-weight:bold;display:none;z-index:999}
#modal{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);z-index:9999;padding:15px;overflow:auto}
.box{background:white;padding:20px;border-radius:15px;max-width:400px;margin:20px auto}
input,select{width:93%;padding:14px;margin:8px 0;border:2px solid #ccc;border-radius:10px;font-size:16px}
.green{background:#00a651;color:white;padding:18px;width:100%;border:none;border-radius:12px;font-size:20px;font-weight:bold;margin-top:12px}
</style></head><body>
<div class="top">{{restock}}<br>{{ann}}</div>
<div class="pochi">Pochi: {{pochi}} - Lipa na Mpesa</div>
<h1 style="color:#bf360c;text-align:center">Menu Leo 8AM-8PM</h1>
{% for n,d in menu.items() %}<div class="item"><span><b>{{n}}</b> - Ksh {{d.price}}</span><button class="btn" onclick="addCart('{{n}}',{{d.price}})">Add</button></div>{% endfor %}
<div id="cartBar" onclick="openM()">🛒 CART (<span id="cCount">0</span>) - Ksh <span id="cTotal">0</span> - CLICK TO CHECKOUT</div>
<div id="modal"><div class="box">
<h2>Your Order</h2><div id="items"></div><hr><h2>Total Ksh <span id="mTotal">0</span></h2>
<input id="name" placeholder="Your Name *">
<input id="phone" placeholder="M-Pesa Phone 07... *">
<label style="font-weight:bold;color:#bf360c;font-size:18px">⏰ Pickup Time (8AM-8PM) *</label>
<select id="time" style="border:2px solid #e65100;font-weight:bold">
<option value="">--Select Time--</option>
<option>ASAP 15 mins</option><option>8:00 AM</option><option>8:30 AM</option><option>9:00 AM</option><option>9:30 AM</option><option>10:00 AM</option><option>10:30 AM</option><option>11:00 AM</option><option>11:30 AM</option><option>12:00 PM</option><option>12:30 PM</option><option>1:00 PM</option><option>1:30 PM</option><option>2:00 PM</option><option>2:30 PM</option><option>3:00 PM</option><option>3:30 PM</option><option>4:00 PM</option><option>4:30 PM</option><option>5:00 PM</option><option>5:30 PM</option><option>6:00 PM</option><option>6:30 PM</option><option>7:00 PM</option><option>7:30 PM</option><option>8:00 PM</option>
</select>
<button class="green" onclick="pay()">💰 LIPA NA MPESA - STK PUSH - Enter PIN</button>
<p id="status" style="text-align:center;font-weight:bold;color:green;font-size:18px"></p>
<button onclick="closeM()" style="width:100%;padding:12px;margin-top:10px;border-radius:10px">Continue Shopping</button>
</div></div>
<script>
var cart=[];
function addCart(n,p){let f=cart.find(x=>x.name==n);if(f)f.qty++;else cart.push({name:n,price:p,qty:1});upd()}
function upd(){let c=0,t=0,h='';cart.forEach((it,i)=>{c+=it.qty;t+=it.price*it.qty;h+=`<div style="display:flex;justify-content:space-between;padding:8px 0"><span>${it.name} x${it.qty}</span><span>Ksh ${it.price*it.qty} <button onclick="rem(${i})" style="background:red;color:white;border:none;border-radius:50%">x</button></span></div>`});document.getElementById('cCount').innerText=c;document.getElementById('cTotal').innerText=t;document.getElementById('mTotal').innerText=t;document.getElementById('items').innerHTML=h||'Empty';document.getElementById('cartBar').style.display=c>0?'block':'none';}
function rem(i){cart.splice(i,1);upd()}
function openM(){document.getElementById('modal').style.display='block'}
function closeM(){document.getElementById('modal').style.display='none'}
function pay(){let n=document.getElementById('name').value;let ph=document.getElementById('phone').value;let tm=document.getElementById('time').value;let tot=document.getElementById('mTotal').innerText;let its=cart.map(x=>x.name+' x'+x.qty).join(', ');if(!n||!ph||!tm){alert('Fill Name, Mpesa Phone, Pickup Time 8AM-8PM');return}document.getElementById('status').innerText='⏳ Sending STK Push to '+ph+'... Check phone & enter PIN!';fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,phone:ph,mpesa:ph,time:tm,total:tot,items:its})}).then(()=>{document.getElementById('status').innerText='✅ ORDER SENT! Pickup at '+tm+' - Gracie sees it! STK sent to '+ph+' - Enter PIN!';setTimeout(()=>{cart=[];upd();closeM();document.getElementById('status').innerText='';},4000)});}
</script></body></html>"""

BOSS = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOSS</title><style>
body{font-family:Arial;background:#fff8e1;padding:10px}.card{background:white;padding:15px;border-radius:12px;margin:10px 0;box-shadow:0 2px 5px #ccc}.order{border-left:8px solid #00a651;background:#e8f5e9}
</style></head><body>
<div class="card" style="background:#2d5016;color:white;text-align:center"><h2>GRACIE BOSS - LOGIN HERE</h2><a href="/" style="color:gold">Go to Shop</a><br>Orders: {{orders|length}}</div>
<div class="card"><form method="post"><input name="ann" value="{{ann}}" style="width:95%;padding:10px"><input name="restock" value="{{restock}}" style="width:95%;padding:10px;margin-top:5px"><button style="background:green;color:white;padding:10px;width:100%;border:none;border-radius:8px;margin-top:5px">Update Message</button></form></div>
<h2>📦 ORDERS - Pickup 8AM-8PM</h2>
{% for o in orders[::-1] %}<div class="card order"><b>👤 {{o.name}} - {{o.phone}}</b><br>⏰ <b style="color:#e65100;font-size:20px">Pickup: {{o.time}}</b><br>💰 Mpesa: {{o.mpesa}} - Ksh {{o.total}}<br>🍛 {{o.items}}</div>{% else %}<div class="card">No orders yet</div>{% endfor %}
</body></html>"""

@app.route('/')
def home(): return render_template_string(CUSTOMER, menu=menu, ann=announcement, restock=restock_info, pochi=pochi)
@app.route('/kitchen')
def kitchen(): return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/kitchen', methods=['POST'])
def kp():
    global announcement, restock_info
    announcement=request.form.get('ann',announcement);restock_info=request.form.get('restock',restock_info)
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/order', methods=['POST'])
def order():
    d=request.get_json()
    if d: orders.append(d)
    return jsonify({"ok":True})
@app.route('/kitchen/increase/<name>')
def inc(name):
    if name in menu: menu[name]['stock']+=5
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/kitchen/decrease/<name>')
def dec(name):
    if name in menu and menu[name]['stock']>0: menu[name]['stock']-=1
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
if __name__=='__main__': app.run(host='0.0.0.0', port=5000)
