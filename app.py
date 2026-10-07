from flask import Flask, request, render_template_string, jsonify
import requests, base64
from datetime import datetime
app = Flask(__name__)

announcement = "Karibu! Leo tuna Pilau, Chapo na Ugali Beef! Orders 8am-8pm"
restock_info = "Pilau itarudi saa 1pm"
pochi = "0799587489"

MPESA_CONSUMER_KEY = "YOUR_CONSUMER_KEY"
MPESA_CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
MPESA_SHORTCODE = "174379"
MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
MPESA_CALLBACK_URL = "https://gracies-shop.onrender.com/mpesa/callback"

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
orders=[]

def get_mpesa_token():
    try:
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(url, auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET), timeout=10)
        return r.json().get('access_token')
    except: return None

CUSTOMER="""<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Gracie-Ruth</title><style>
body{background:#f5f5f0;font-family:Arial;padding:10px;padding-bottom:110px;margin:0}
.h{background:#fff9c4;padding:10px;border-radius:8px;border:2px solid gold;text-align:center}
.p{background:#2d5016;color:#fff;padding:12px;border-radius:8px;margin:10px 0;text-align:center;font-size:18px;font-weight:bold}
.i{background:#fff;display:flex;justify-content:space-between;align-items:center;padding:14px;margin:7px 0;border-radius:12px;box-shadow:0 2px 4px #ccc}
.b{background:#e65100;color:#fff;border:none;padding:10px 18px;border-radius:8px;font-weight:bold}
.cart{position:fixed;bottom:0;left:0;right:0;background:#2d5016;color:#fff;padding:18px;text-align:center;font-size:20px;font-weight:bold;display:none;z-index:100}
.m{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.88);padding:15px;overflow:auto;z-index:9999;display:none}
.box{background:#fff;padding:20px;border-radius:12px;max-width:420px;margin:20px auto}
input,select{width:92%;padding:12px;margin:6px 0;border:1px solid #ccc;border-radius:8px;font-size:16px}
.pay{background:#00a651;color:white;padding:15px;width:100%;border:none;border-radius:10px;font-size:18px;font-weight:bold;margin-top:10px}
.order{background:#2d5016;color:white;padding:15px;width:100%;border:none;border-radius:10px;font-size:18px;font-weight:bold;margin-top:8px}
</style></head><body>
<div class="h">Restock: {{restock}}<br>{{ann}}</div>
<div class="p">Pochi: {{pochi}} - Lipa na M-Pesa</div>
<h1 style="color:#bf360c">Menu Leo</h1>
{% for n,d in menu.items() %}<div class="i"><span><b>{{n}}</b> - Ksh {{d.price}}</span><button class="b" onclick="addCart('{{n}}',{{d.price}})">Add</button></div>{% endfor %}
<div class="cart" id="cartBar" onclick="openCart()">🛒 Cart (<span id="cartCount">0</span>) - Ksh <span id="cartTotal">0</span></div>
<div class="m" id="cartModal"><div class="box">
<h2>Checkout</h2><div id="cartItems"></div><hr>
<h3>Total: Ksh <span id="modalTotal">0</span></h3>
<input id="custName" placeholder="Your Full Name *">
<input id="custPhone" placeholder="Your Phone 07.. *">
<input id="custMpesa" placeholder="M-Pesa Phone to Pay (07..) *">
<label style="font-weight:bold;margin-top:10px;display:block">Pickup Time (8AM - 8PM) *</label>
<select id="pickupTime">
<option value="">-- Select Pickup Time --</option>
<option>ASAP - 15 mins</option>
<option>8:00 AM</option><option>8:30 AM</option>
<option>9:00 AM</option><option>9:30 AM</option>
<option>10:00 AM</option><option>10:30 AM</option>
<option>11:00 AM</option><option>11:30 AM</option>
<option>12:00 PM</option><option>12:30 PM</option>
<option>1:00 PM</option><option>1:30 PM</option>
<option>2:00 PM</option><option>2:30 PM</option>
<option>3:00 PM</option><option>3:30 PM</option>
<option>4:00 PM</option><option>4:30 PM</option>
<option>5:00 PM</option><option>5:30 PM</option>
<option>6:00 PM</option><option>6:30 PM</option>
<option>7:00 PM</option><option>7:30 PM</option>
<option>8:00 PM</option>
</select>
<input id="custRoom" placeholder="Hostel / Room / Note">
<button class="pay" onclick="payMpesa()">💰 Lipa na M-Pesa - STK Push</button>
<button class="order" onclick="placeOrder()">✅ Order - Pay on Pickup</button>
<p id="payStatus" style="text-align:center;font-weight:bold;color:green"></p>
<button onclick="closeCart()" style="width:100%;padding:12px;margin-top:12px;border-radius:8px">Continue Shopping</button>
</div></div>
<script>
var cart=[];
function addCart(n,p){var f=null;for(var i=0;i<cart.length;i++){if(cart[i].name==n)f=cart[i]}if(f){f.qty++}else{cart.push({name:n,price:p,qty:1})}upd()}
function upd(){var c=0,t=0,h='';for(var i=0;i<cart.length;i++){c+=cart[i].qty;t+=cart[i].price*cart[i].qty;h+='<div style="display:flex;justify-content:space-between;margin:8px 0"><span>'+cart[i].name+' x'+cart[i].qty+'</span><span>Ksh '+(cart[i].price*cart[i].qty)+' <button onclick="rem('+i+')">x</button></span></div>'}document.getElementById('cartCount').innerText=c;document.getElementById('cartTotal').innerText=t;document.getElementById('modalTotal').innerText=t;document.getElementById('cartItems').innerHTML=h||'Empty';document.getElementById('cartBar').style.display=c>0?'block':'none';}
function rem(i){cart.splice(i,1);upd()}
function openCart(){document.getElementById('cartModal').style.display='block'}
function closeCart(){document.getElementById('cartModal').style.display='none'}
function getData(){var name=document.getElementById('custName').value;var phone=document.getElementById('custPhone').value;var mpesa=document.getElementById('custMpesa').value;var room=document.getElementById('custRoom').value;var time=document.getElementById('pickupTime').value;var total=document.getElementById('modalTotal').innerText;var items='';for(var i=0;i<cart.length;i++){items+=cart[i].name+' x'+cart[i].qty+', '}return {name:name,phone:phone,mpesa:mpesa,room:room,time:time,total:total,items:items}}
function placeOrder(){var d=getData();if(!d.name||!d.phone||!d.time){alert('Weka Name, Phone na Pickup Time (8AM-8PM)');return}fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(()=>{document.getElementById('payStatus').innerText='✅ Order Received! Pickup: '+d.time;setTimeout(()=>{cart=[];upd();closeCart();document.getElementById('payStatus').innerText='';},3000)});}
function payMpesa(){var d=getData();if(!d.name||!d.mpesa||!d.time){alert('Weka Name, M-Pesa Phone na Pickup Time (8AM-8PM)');return}document.getElementById('payStatus').innerText='⏳ Sending STK to '+d.mpesa+'...';fetch('/mpesa/stk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(r=>r.json()).then(res=>{if(res.ok){document.getElementById('payStatus').innerText='📱 Check phone '+d.mpesa+' - Enter PIN! Pickup '+d.time;fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});}else{document.getElementById('payStatus').innerText='❌ STK Failed - will save as Cash order';fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});}}).catch(()=>{document.getElementById('payStatus').innerText='Order saved - Pay on pickup';fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});});}
</script></body></html>"""

BOSS="""<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>BOSS</title><style>
body{background:#fff8e1;font-family:Arial;padding:10px}.card{background:white;padding:12px;border-radius:10px;margin-bottom:10px;box-shadow:0 2px 4px #ccc}
.order{background:#e8f5e9;border-left:6px solid #2e7d32}
</style></head><body>
<div class="card"><b>GRACIE BOSS</b> | <a href="/">Shop</a> | Orders: {{orders|length}}</div>
<div class="card" style="background:#fff9c4;border:2px solid gold"><form method="post"><input name="ann" value="{{ann}}"><input name="restock" value="{{restock}}"><button>Update</button></form></div>
<h2>📦 ORDERS - 8AM to 8PM Pickup</h2>
{% for o in orders[::-1] %}<div class="card order"><b>{{o.name}} - {{o.phone}}</b> | ⏰ <b style="color:#e65100">{{o.time}}</b><br>📱 M-Pesa: {{o.mpesa}}<br>🏠 {{o.room}}<br>🍛 {{o.items}}<br><h3>Ksh {{o.total}}</h3></div>{% else %}<p>No orders</p>{% endfor %}
<h2>Stock</h2>{% for n,d in menu.items() %}<div class="card">{{n}} - {{d.stock}} <a href="/kitchen/decrease/{{n}}">-1</a> <a href="/kitchen/increase/{{n}}">+5</a></div>{% endfor %}
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
@app.route('/mpesa/stk', methods=['POST'])
def stk():
    data=request.get_json()
    amount=data.get('total','10').replace('Ksh','').strip()
    try: amount=int(float(amount))
    except: amount=10
    phone=data.get('mpesa','')
    phone=phone.replace(' ','').replace('+','')
    if phone.startswith('0'): phone='254'+phone[1:]
    if not phone.startswith('254'): phone='254'+phone[-9:]
    token=get_mpesa_token()
    if not token: return jsonify({"ok":False,"error":"Add Daraja keys"}),500
    timestamp=datetime.now().strftime('%Y%m%d%H%M%S')
    pwd=base64.b64encode((MPESA_SHORTCODE+MPESA_PASSKEY+timestamp).encode()).decode()
    headers={"Authorization":f"Bearer {token}"}
    payload={"BusinessShortCode":MPESA_SHORTCODE,"Password":pwd,"Timestamp":timestamp,"TransactionType":"CustomerPayBillOnline","Amount":amount,"PartyA":phone,"PartyB":MPESA_SHORTCODE,"PhoneNumber":phone,"CallBackURL":MPESA_CALLBACK_URL,"AccountReference":"Gracie","TransactionDesc":"Food"}
    try:
        r=requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers, timeout=15)
        j=r.json()
        if j.get('ResponseCode')=='0': return jsonify({"ok":True,"data":j})
        else: return jsonify({"ok":False,"error":str(j)})
    except Exception as e: return jsonify({"ok":False,"error":str(e)}),500
@app.route('/mpesa/callback', methods=['POST'])
def cb(): return jsonify({"ok":True})
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
if __name__=='__main__': app.run(host='0.0.0.0', port=5000)
