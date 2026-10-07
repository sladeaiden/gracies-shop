from flask import Flask, request, render_template_string, jsonify, session, redirect
app = Flask(__name__)
app.secret_key = "gracie123"
announcement = "Leo tuna Pilau Tamu, Chapo Soft na Ugali Beef! Karibu!"
restock_info = "Pilau itarudi 1PM - Orders 8AM-8PM"
pochi_number = "0799587489"
orders = []
PASSWORD = "gracie 123"
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
.top{background:#fff9c4;border:3px solid gold;padding:12px;border-radius:12px;text-align:center}
.pochi{background:#2d5016;color:white;padding:14px;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;margin:10px 0}
.seller{background:white;border-left:8px solid #e65100;padding:15px;border-radius:12px;margin:12px 0}
.instruct{background:#e8f5e9;border-left:8px solid #2e7d32;padding:15px;border-radius:12px;margin:12px 0}
.item{background:white;padding:15px;margin:8px 0;border-radius:12px;display:flex;justify-content:space-between;box-shadow:0 2px 4px #ccc}
.btn{background:#e65100;color:white;border:none;padding:12px 18px;border-radius:10px;font-weight:bold}
#cartBar{position:fixed;bottom:0;left:0;right:0;background:#2d5016;color:white;padding:20px;text-align:center;font-size:22px;font-weight:bold;display:none;z-index:999;border-top:3px solid gold}
#modal{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);z-index:9999;padding:15px;overflow:auto}
.box{background:white;padding:20px;border-radius:15px;max-width:420px;margin:20px auto}
input,select{width:93%;padding:14px;margin:8px 0;border:2px solid #ccc;border-radius:10px;font-size:16px}
.green{background:#00a651;color:white;padding:18px;width:100%;border:none;border-radius:12px;font-size:20px;font-weight:bold;margin-top:12px}
.mpesaBox{background:#e8f5e9;border:2px solid #00a651;padding:15px;border-radius:12px;margin-top:15px}
</style></head><body>
<div class="top"><b>📢 {{ann}}</b><br><b>⏰ {{restock}}</b></div>
<div class="pochi">📱 Pochi: {{pochi}} - Lipa na Mpesa</div>
<div class="seller"><h3 style="margin:0;color:#bf360c">👩‍🍳 Gracie's Corner Today</h3><p>{{ann}}</p><p><b>Restock:</b> {{restock}} | Orders Today: {{orders|length}}</p></div>
<div class="instruct"><h3 style="margin:0;color:#2e7d32">📋 HOW TO ORDER</h3><p>1. Add food → 2. Click CART → 3. Name + Mpesa Phone + Pickup Time 8AM-8PM → 4. Click LIPA NA MPESA → 5. <b>Send money to Pochi {{pochi}}</b> → 6. Enter Mpesa Code → 7. Gracie will mark READY!</p></div>
<h1 style="color:#bf360c;text-align:center">Menu 8AM-8PM</h1>
{% for n,d in menu.items() %}<div class="item"><div><b>{{n}}</b> - Ksh {{d.price}}<br><small style="color:{% if d.stock==0 %}red{% else %}green{% endif %}">Left: {{d.stock}}</small></div><button class="btn" {% if d.stock==0 %}disabled style="background:grey"{% endif %} onclick="addCart('{{n}}',{{d.price}})">Add</button></div>{% endfor %}
<div class="seller"><h3>🔍 Check Order READY?</h3><input id="checkPhone" placeholder="Your Phone 07.."><button onclick="checkStatus()" style="width:100%;padding:12px;background:#2d5016;color:white;border:none;border-radius:8px">Check</button><p id="orderStatus"></p></div>
<div id="cartBar" onclick="openM()">🛒 CART (<span id="cCount">0</span>) - Ksh <span id="cTotal">0</span></div>
<div id="modal"><div class="box">
<h2>Your Order</h2><div id="items"></div><hr><h2>Total Ksh <span id="mTotal">0</span></h2>
<input id="name" placeholder="Your Name *">
<input id="phone" placeholder="Your M-Pesa Phone 07.. *">
<label style="font-weight:bold;color:#bf360c">⏰ Pickup Time 8AM-8PM *</label>
<select id="time" style="border:2px solid #e65100;font-weight:bold"><option value="">--Select--</option><option>ASAP 15 mins</option><option>8:00 AM</option><option>8:30 AM</option><option>9:00 AM</option><option>9:30 AM</option><option>10:00 AM</option><option>10:30 AM</option><option>11:00 AM</option><option>11:30 AM</option><option>12:00 PM</option><option>12:30 PM</option><option>1:00 PM</option><option>1:30 PM</option><option>2:00 PM</option><option>2:30 PM</option><option>3:00 PM</option><option>3:30 PM</option><option>4:00 PM</option><option>4:30 PM</option><option>5:00 PM</option><option>5:30 PM</option><option>6:00 PM</option><option>6:30 PM</option><option>7:00 PM</option><option>7:30 PM</option><option>8:00 PM</option></select>
<div id="mpesaStep" style="display:none" class="mpesaBox">
<h3 style="margin:0;color:#2e7d32">💰 LIPA NA MPESA</h3>
<p style="font-size:18px">Send <b>Ksh <span id="payAmount">0</span></b> to:</p>
<p style="font-size:26px;font-weight:bold;color:#bf360c;text-align:center">Pochi: {{pochi}}<br>Gracie-Ruth</p>
<p>Go to M-Pesa → Send Money → Enter number {{pochi}} → Amount <span id="payAmount2">0</span> → PIN → You get SMS with Code like <b>QGH7K...</b></p>
<input id="mpesaCode" placeholder="Enter Mpesa Code e.g QGH7K... *">
<button class="green" onclick="confirmPay()">✅ Confirm Payment - Send Order to Gracie</button>
</div>
<button id="payBtn" class="green" onclick="showMpesa()">💰 LIPA NA MPESA - Show Pochi Number</button>
<p id="status" style="text-align:center;font-weight:bold;color:green"></p>
<button onclick="closeM()" style="width:100%;padding:12px;margin-top:10px">Continue Shopping</button>
</div></div>
<script>
var cart=[];
function addCart(n,p){let f=cart.find(x=>x.name==n);if(f)f.qty++;else cart.push({name:n,price:p,qty:1});upd()}
function upd(){let c=0,t=0,h='';cart.forEach((it,i)=>{c+=it.qty;t+=it.price*it.qty;h+=`<div style="display:flex;justify-content:space-between;padding:8px 0"><span>${it.name} x${it.qty}</span><span>Ksh ${it.price*it.qty} <button onclick="rem(${i})" style="background:red;color:white;border:none;border-radius:50%">x</button></span></div>`});document.getElementById('cCount').innerText=c;document.getElementById('cTotal').innerText=t;document.getElementById('mTotal').innerText=t;document.getElementById('payAmount').innerText=t;document.getElementById('payAmount2').innerText=t;document.getElementById('items').innerHTML=h||'Empty';document.getElementById('cartBar').style.display=c>0?'block':'none';}
function rem(i){cart.splice(i,1);upd()}
function openM(){document.getElementById('modal').style.display='block'}
function closeM(){document.getElementById('modal').style.display='none';document.getElementById('mpesaStep').style.display='none';document.getElementById('payBtn').style.display='block';}
function showMpesa(){let n=document.getElementById('name').value;let ph=document.getElementById('phone').value;let tm=document.getElementById('time').value;if(!n||!ph||!tm){alert('Fill Name, Phone, Pickup Time 8AM-8PM first!');return}document.getElementById('mpesaStep').style.display='block';document.getElementById('payBtn').style.display='none';}
function confirmPay(){let n=document.getElementById('name').value;let ph=document.getElementById('phone').value;let tm=document.getElementById('time').value;let tot=document.getElementById('mTotal').innerText;let code=document.getElementById('mpesaCode').value;let its=cart.map(x=>x.name+' x'+x.qty).join(', ');if(!code){alert('Enter Mpesa Code after paying to {{pochi}}');return}document.getElementById('status').innerText='✅ Order Sent! Gracie sees Mpesa Code '+code+' - Pickup at '+tm;fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,phone:ph,mpesa:ph,time:tm,total:tot,items:its,code:code,status:'PAID - '+code})}).then(()=>{setTimeout(()=>{cart=[];upd();closeM();document.getElementById('status').innerText='';document.getElementById('mpesaCode').value='';},3000)});}
function checkStatus(){let ph=document.getElementById('checkPhone').value;fetch('/check/'+ph).then(r=>r.json()).then(d=>{let el=document.getElementById('orderStatus');if(d.found){el.innerHTML='<div style=background:#c8e6c9;padding:10px;border-radius:8px>'+d.items+'<br>Ksh '+d.total+' | '+d.time+'<br><b>'+d.status+'</b><br>'+(d.status.includes('READY')?'✅ Come now!':'⏳ Preparing')+'</div>';}else{el.innerText='No order for '+ph;}});}
</script></body></html>"""

LOGIN = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Login</title><style>body{background:#2d5016;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:Arial}.box{background:white;padding:30px;border-radius:15px;width:90%;max-width:350px;text-align:center}input{width:90%;padding:15px;margin:10px 0;border:2px solid #ccc;border-radius:10px;font-size:18px}button{background:#2d5016;color:white;padding:15px;width:95%;border:none;border-radius:10px;font-size:18px;font-weight:bold}</style></head><body><div class="box"><h2>GRACIE BOSS</h2><p>Password: gracie 123</p><form method="post"><input type="password" name="pwd" placeholder="Enter password"><button>Login</button></form>{% if err %}<p style="color:red">{{err}}</p>{% endif %}</div></body></html>"""

BOSS = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOSS</title><style>body{font-family:Arial;background:#fff8e1;padding:10px}.card{background:white;padding:15px;border-radius:12px;margin:10px 0}.order{border-left:8px solid #00a651;background:#e8f5e9}.ready{border-left:8px solid #ff9800;background:#fff3e0}button{padding:10px 15px;border:none;border-radius:8px;margin:3px;font-weight:bold;color:white}.green{background:#2e7d32}.orange{background:#ef6c00}.red{background:#c62828}.black{background:#212121}</style></head><body>
<div class="card" style="background:#2d5016;color:white;display:flex;justify-content:space-between"><div><h2 style="margin:0">GRACIE BOSS</h2><a href="/" style="color:gold">View Student Shop</a> | Orders: {{orders|length}}</div><a href="/logout"><button class="red">Logout</button></a></div>
<div class="card" style="background:#fff9c4;border:3px solid gold"><h3>📢 What Students See</h3><form method="post"><input type="hidden" name="action" value="update_msg"><input name="ann" value="{{ann}}" style="width:95%;padding:12px;border:2px solid gold"><br><br><input name="restock" value="{{restock}}" style="width:95%;padding:12px;border:2px solid orange"><br><button class="green" style="width:100%;margin-top:10px;padding:14px">Update</button></form></div>
<div class="card"><h3>Stock Left - Students see</h3>{% for n,d in menu.items() %}<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee"><span>{{n}} - {{d.stock}} left</span><span><a href="/kitchen/decrease/{{n}}"><button class="black">-1</button></a><a href="/kitchen/increase/{{n}}"><button class="green">+5</button></a><a href="/kitchen/zero/{{n}}"><button class="red">0</button></a></span></div>{% endfor %}</div>
<h2>Orders - With Mpesa Code</h2>
{% for idx, o in enumerate(orders[::-1]) %}{% set real_idx = orders|length -1 - idx %}<div class="card {% if 'READY' in o.status %}ready{% else %}order{% endif %}"><b>{{o.name}} - {{o.phone}}</b> | {{o.time}} | Ksh {{o.total}}<br>{{o.items}}<br>Mpesa Code: <b style="color:green;font-size:18px">{{o.code}}</b><br><b>{{o.status}}</b><br><br>{% if 'READY' not in o.status and 'DONE' not in o.status %}<a href="/kitchen/ready/{{real_idx}}"><button class="orange">📢 Mark READY</button></a>{% endif %}<a href="/kitchen/done/{{real_idx}}"><button class="green">✅ DONE</button></a></div>{% else %}<div class="card">No orders</div>{% endfor %}
</body></html>"""

@app.route('/')
def home(): return render_template_string(CUSTOMER, menu=menu, ann=announcement, restock=restock_info, pochi=pochi_number, orders=orders)
@app.route('/kitchen', methods=['GET','POST'])
def kitchen():
    global announcement, restock_info
    if 'logged' not in session:
        if request.method=='POST' and request.form.get('pwd'):
            if request.form.get('pwd')==PASSWORD: session['logged']=True
            else: return render_template_string(LOGIN, err="Wrong! Use gracie 123")
        if 'logged' not in session: return render_template_string(LOGIN)
    if request.method=='POST' and request.form.get('action')=='update_msg':
        announcement=request.form.get('ann',announcement); restock_info=request.form.get('restock',restock_info)
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders, enumerate=enumerate)
@app.route('/logout')
def logout(): session.pop('logged',None); return redirect('/kitchen')
@app.route('/order', methods=['POST'])
def order():
    d=request.get_json()
    if d: orders.append(d)
    return jsonify({"ok":True})
@app.route('/check/<phone>')
def check(phone):
    for o in orders[::-1]:
        if o.get('phone')==phone: return jsonify({"found":True, "items":o.get('items'), "total":o.get('total'), "time":o.get('time'), "status":o.get('status')})
    return jsonify({"found":False})
@app.route('/kitchen/ready/<int:idx>')
def ready(idx):
    if 'logged' not in session: return redirect('/kitchen')
    if 0<=idx<len(orders): orders[idx]['status']='READY FOR PICKUP'
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders, enumerate=enumerate)
@app.route('/kitchen/done/<int:idx>')
def done(idx):
    if 'logged' not in session: return redirect('/kitchen')
    if 0<=idx<len(orders): orders[idx]['status']='DONE'
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders, enumerate=enumerate)
@app.route('/kitchen/increase/<name>')
def inc(name):
    if 'logged' not in session: return redirect('/kitchen')
    if name in menu: menu[name]['stock']+=5
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders, enumerate=enumerate)
@app.route('/kitchen/decrease/<name>')
def dec(name):
    if 'logged' not in session: return redirect('/kitchen')
    if name in menu and menu[name]['stock']>0: menu[name]['stock']-=1
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders, enumerate=enumerate)
@app.route('/kitchen/zero/<name>')
def zero(name):
    if 'logged' not in session: return redirect('/kitchen')
    if name in menu: menu[name]['stock']=0
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders, enumerate=enumerate)
if __name__=='__main__': app.run(host='0.0.0.0', port=5000)
