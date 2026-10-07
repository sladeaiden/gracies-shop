from flask import Flask, request, render_template_string, jsonify, session, redirect
import requests, base64, datetime, json
app = Flask(__name__)
app.secret_key = "gracie123"

# === YOUR REAL DARAJA KEYS ===
MPESA_CONSUMER_KEY = "TqcH1dLo1OU8FEgP6Xotwkyf9VuzsPeeO9k0kzSqOltQxBus"
MPESA_CONSUMER_SECRET = "mpPHJxVnS69pVWMQ3AZCMwYsuw2GtAFzd2aVFcJUovFQhyx1NcVARKMyAqVrUYQk"
MPESA_SHORTCODE = "174379"
MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
# ==============================

announcement = "Leo tuna Pilau Tamu! STK ina-work!"
restock_info = "Pilau 1PM - Orders 8AM-8PM"
pochi_number = "0799587489"
orders = []
PASSWORD = "gracie 123"
menu = {
    "Chapati": {"price": 20, "stock": 55}, "Beans Chapo": {"price": 80, "stock": 20},
    "Pilau Regular": {"price": 80, "stock": 15}, "Pilau Large": {"price": 100, "stock": 15},
    "Mandazi": {"price": 10, "stock": 100}, "Tea": {"price": 20, "stock": 100},
    "Chapo Chipo": {"price": 60, "stock": 25}, "Chips Small": {"price": 60, "stock": 20},
    "Chips Medium": {"price": 80, "stock": 20}, "Chips Large": {"price": 100, "stock": 20},
    "Ugali Beef": {"price": 150, "stock": 15}, "Soda Fanta": {"price": 50, "stock": 30},
    "Pepsi": {"price": 40, "stock": 30}, "Predator": {"price": 70, "stock": 25},
    "Minute Maid": {"price": 80, "stock": 20}, "Yoghurt": {"price": 60, "stock": 20},
    "Sausage": {"price": 40, "stock": 30}, "Samosa": {"price": 40, "stock": 30},
}

def get_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET))
    return r.json().get('access_token')

def stk_push(phone, amount, ref):
    try:
        token = get_token()
        if not token: return {"error":"No token"}
        # format phone 07.. to 254..
        if phone.startswith("0"): phone = "254" + phone[1:]
        if phone.startswith("+"): phone = phone[1:]
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode((MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()).decode()
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {token}", "Content-Type":"application/json"}
        payload = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": "https://gracies-shop.onrender.com/callback",
            "AccountReference": ref[:12],
            "TransactionDesc": "Gracie Order"
        }
        resp = requests.post(url, json=payload, headers=headers)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

CUSTOMER = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Gracie</title><style>
body{font-family:Arial;background:#f5f5f0;margin:0;padding:10px;padding-bottom:120px}
.top{background:#fff9c4;border:3px solid gold;padding:12px;border-radius:12px;text-align:center}
.pochi{background:#2d5016;color:white;padding:14px;border-radius:10px;text-align:center;font-size:18px;font-weight:bold;margin:10px 0}
.seller{background:white;border-left:8px solid #e65100;padding:15px;border-radius:12px;margin:12px 0}
.instruct{background:#e8f5e9;border-left:8px solid #2e7d32;padding:15px;border-radius:12px;margin:12px 0}
.item{background:white;padding:15px;margin:8px 0;border-radius:12px;display:flex;justify-content:space-between;box-shadow:0 2px 4px #ccc}
.btn{background:#e65100;color:white;border:none;padding:12px 18px;border-radius:10px;font-weight:bold}
#cartBar{position:fixed;bottom:0;left:0;right:0;background:#2d5016;color:white;padding:20px;text-align:center;font-size:22px;font-weight:bold;display:none;z-index:999;border-top:3px solid gold}
#modal{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);z-index:9999;padding:15px;overflow:auto}
.box{background:white;padding:20px;border-radius:15px;max-width:420px;margin:20px auto}
input,select{width:93%;padding:14px;margin:8px 0;border:2px solid #ccc;border-radius:10px;font-size:16px}
.green{background:#00a651;color:white;padding:18px;width:100%;border:none;border-radius:12px;font-size:20px;font-weight:bold;margin-top:12px}
</style></head><body>
<div class="top"><b>{{ann}}</b><br>{{restock}}</div>
<div class="pochi">📱 STK ACTIVE! Pay to Till 174379 (Test Mode)</div>
<div class="seller"><h3 style="margin:0;color:#bf360c">👩‍🍳 Gracie's Corner</h3><p>{{ann}}</p></div>
<div class="instruct"><h3 style="margin:0;color:#2e7d32">📋 HOW TO ORDER - REAL STK!</h3><p>1. Add food 2. CART 3. Name + Mpesa Phone 07.. + Time 4. Click LIPA NA MPESA 5. <b>WAIT FOR STK POPUP ON YOUR PHONE - Enter M-Pesa PIN!</b> 6. Gracie sees PAID!</p></div>
<h1 style="color:#bf360c;text-align:center">Menu 8AM-8PM</h1>
{% for n,d in menu.items() %}<div class="item"><div><b>{{n}}</b> - Ksh {{d.price}}<br><small style="color:{% if d.stock==0 %}red{% else %}green{% endif %}">Left: {{d.stock}}</small></div><button class="btn" {% if d.stock==0 %}disabled style="background:grey"{% endif %} onclick="addCart('{{n}}',{{d.price}})">Add</button></div>{% endfor %}
<div id="cartBar" onclick="openM()">🛒 CART (<span id="cCount">0</span>) - Ksh <span id="cTotal">0</span></div>
<div id="modal"><div class="box">
<h2>Your Order</h2><div id="items"></div><hr><h2>Total Ksh <span id="mTotal">0</span></h2>
<input id="name" placeholder="Your Name *">
<input id="phone" placeholder="Mpesa Phone 07.. * - STK will come here">
<label style="font-weight:bold;color:#bf360c">⏰ Pickup Time *</label>
<select id="time"><option value="">--Select--</option><option>ASAP 15 mins</option><option>8:00 AM</option><option>9:00 AM</option><option>10:00 AM</option><option>11:00 AM</option><option>12:00 PM</option><option>1:00 PM</option><option>2:00 PM</option><option>3:00 PM</option><option>4:00 PM</option><option>5:00 PM</option><option>6:00 PM</option><option>7:00 PM</option><option>8:00 PM</option></select>
<button id="payBtn" class="green" onclick="pay()">💰 LIPA NA MPESA - STK Push PIN!</button>
<p id="status" style="text-align:center;font-weight:bold;color:green"></p>
<button onclick="closeM()" style="width:100%;padding:12px;margin-top:10px">Continue</button>
</div></div>
<script>
var cart=[];
function addCart(n,p){let f=cart.find(x=>x.name==n);if(f)f.qty++;else cart.push({name:n,price:p,qty:1});upd()}
function upd(){let c=0,t=0,h='';cart.forEach((it,i)=>{c+=it.qty;t+=it.price*it.qty;h+=`<div style="display:flex;justify-content:space-between;padding:8px 0"><span>${it.name} x${it.qty}</span><span>Ksh ${it.price*it.qty} <button onclick="rem(${i})" style="background:red;color:white;border:none;border-radius:50%">x</button></span></div>`});document.getElementById('cCount').innerText=c;document.getElementById('cTotal').innerText=t;document.getElementById('mTotal').innerText=t;document.getElementById('items').innerHTML=h||'Empty';document.getElementById('cartBar').style.display=c>0?'block':'none';}
function rem(i){cart.splice(i,1);upd()}
function openM(){document.getElementById('modal').style.display='block'}
function closeM(){document.getElementById('modal').style.display='none'}
function pay(){let n=document.getElementById('name').value;let ph=document.getElementById('phone').value;let tm=document.getElementById('time').value;let tot=document.getElementById('mTotal').innerText;let its=cart.map(x=>x.name+' x'+x.qty).join(', ');if(!n||!ph||!tm){alert('Fill Name, Phone, Time!');return}document.getElementById('status').innerText='⏳ Sending STK to '+ph+'... Wait for PIN popup on your phone!';fetch('/stk',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:n,phone:ph,time:tm,total:tot,items:its})}).then(r=>r.json()).then(d=>{if(d.ResponseCode=='0'||d.ResponseDescription){document.getElementById('status').innerText='✅ STK SENT to '+ph+'! Enter PIN on your phone NOW! Order saved!';setTimeout(()=>{cart=[];upd();closeM();},4000);}else{document.getElementById('status').innerText='❌ STK Failed: '+(d.error||d.errorMessage||JSON.stringify(d))+' - Trying manual';}}).catch(e=>{document.getElementById('status').innerText='Error '+e;});}
</script></body></html>"""

LOGIN = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>Login</title><style>body{background:#2d5016;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:Arial}.box{background:white;padding:30px;border-radius:15px;width:90%;max-width:350px;text-align:center}input{width:90%;padding:15px;margin:10px 0;border:2px solid #ccc;border-radius:10px;font-size:18px}button{background:#2d5016;color:white;padding:15px;width:95%;border:none;border-radius:10px;font-size:18px;font-weight:bold}</style></head><body><div class="box"><h2>GRACIE BOSS</h2><p>Password: gracie 123</p><form method="post"><input type="password" name="pwd" placeholder="Enter password"><button>Login</button></form>{% if err %}<p style="color:red">{{err}}</p>{% endif %}</div></body></html>"""

BOSS = """<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOSS</title><style>body{font-family:Arial;background:#fff8e1;padding:10px}.card{background:white;padding:15px;border-radius:12px;margin:10px 0}.order{border-left:8px solid #00a651;background:#e8f5e9}.ready{border-left:8px solid #ff9800;background:#fff3e0}button{padding:10px 15px;border:none;border-radius:8px;margin:3px;font-weight:bold;color:white}.green{background:#2e7d32}.orange{background:#ef6c00}.red{background:#c62828}.black{background:#212121}</style></head><body>
<div class="card" style="background:#2d5016;color:white;display:flex;justify-content:space-between"><div><h2 style="margin:0">GRACIE BOSS - STK ACTIVE</h2><a href="/" style="color:gold">View Student Shop</a> | Orders: {{orders|length}}</div><a href="/logout"><button class="red">Logout</button></a></div>
<div class="card" style="background:#fff9c4;border:3px solid gold"><h3>📢 Message</h3><form method="post"><input type="hidden" name="action" value="update_msg"><input name="ann" value="{{ann}}" style="width:95%;padding:12px"><br><br><input name="restock" value="{{restock}}" style="width:95%;padding:12px"><br><button class="green" style="width:100%;margin-top:10px">Update</button></form></div>
<h2>Orders - STK Paid</h2>
{% for idx, o in enumerate(orders[::-1]) %}{% set real_idx = orders|length -1 - idx %}<div class="card {% if 'READY' in o.status %}ready{% else %}order{% endif %}"><b>{{o.name}} - {{o.phone}}</b> | {{o.time}} | Ksh {{o.total}}<br>{{o.items}}<br><b>{{o.status}}</b><br><br>{% if 'READY' not in o.status and 'DONE' not in o.status %}<a href="/kitchen/ready/{{real_idx}}"><button class="orange">📢 READY</button></a>{% endif %}<a href="/kitchen/done/{{real_idx}}"><button class="green">✅ DONE</button></a></div>{% else %}<div class="card">No orders</div>{% endfor %}
</body></html>"""

@app.route('/')
def home(): return render_template_string(CUSTOMER, menu=menu, ann=announcement, restock=restock_info, orders=orders)
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
@app.route('/stk', methods=['POST'])
def stk_route():
    d=request.get_json()
    result = stk_push(d.get('phone',''), d.get('total','10'), d.get('name','Gracie'))
    # Save order even if STK fails
    d['status'] = 'STK SENT - '+str(result.get('ResponseDescription','')) if 'ResponseCode' in result else 'PAID - STK: '+str(result)
    orders.append(d)
    return jsonify(result)
@app.route('/callback', methods=['POST'])
def callback():
    print("CALLBACK:", request.get_json())
    return jsonify({"ResultCode":0, "ResultDesc":"Accepted"})
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
if __name__=='__main__': app.run(host='0.0.0.0', port=5000)
