from flask import Flask, request, render_template_string
app = Flask(__name__)
announcement = "Karibu! Leo tuna Pilau, Chapo na Ugali Beef! Orders 7am-8pm"
restock_info = "Pilau itarudi saa 1pm"
pochi = "0799587489"
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
CUSTOMER="""<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Gracie</title><style>
body{background:#f5f5f0;font-family:Arial;padding:10px;padding-bottom:100px}
.h{background:#fff9c4;padding:10px;border-radius:8px;border:2px solid gold;text-align:center}
.p{background:#2d5016;color:#fff;padding:12px;border-radius:8px;margin:10px 0;text-align:center;font-size:18px;font-weight:bold}
.i{background:#fff;display:flex;justify-content:space-between;align-items:center;padding:14px;margin:7px 0;border-radius:12px;box-shadow:0 2px 4px #ccc}
.b{background:#e65100;color:#fff;border:none;padding:10px 18px;border-radius:8px;font-weight:bold}
.cart{position:fixed;bottom:0;left:0;right:0;background:#2d5016;color:#fff;padding:18px;text-align:center;font-size:20px;font-weight:bold;display:none;z-index:100}
.m{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);padding:15px;overflow:auto;z-index:9999;display:none}
.box{background:#fff;padding:20px;border-radius:12px;max-width:400px;margin:30px auto}
input{width:92%;padding:12px;margin:6px 0;border:1px solid #ccc;border-radius:6px}
</style></head><body>
<div class="h">Restock: {{restock}}<br>{{ann}}</div>
<div class="p">Pochi: {{pochi}}</div>
<h1 style="color:#bf360c">Menu Leo</h1>
{% for n,d in menu.items() %}<div class="i"><span><b>{{n}}</b> - Ksh {{d.price}}</span><button class="b" onclick="addCart('{{n}}',{{d.price}})">Add</button></div>{% endfor %}
<div class="cart" id="cartBar" onclick="openCart()">🛒 Cart (<span id="cartCount">0</span>) - Ksh <span id="cartTotal">0</span></div>
<div class="m" id="cartModal"><div class="box"><h2>Your Cart</h2><div id="cartItems"></div><hr><h3>Total: Ksh <span id="modalTotal">0</span></h3>
<input id="custName" placeholder="Your Name"><input id="custPhone" placeholder="Phone 07.."><input id="custRoom" placeholder="Hostel/Room">
<button onclick="placeOrder()" style="background:#2d5016;color:white;padding:14px;width:100%;border:none;border-radius:8px;font-size:18px;margin-top:10px">Order via WhatsApp</button>
<button onclick="closeCart()" style="width:100%;padding:12px;margin-top:10px">Continue</button></div></div>
<script>
var cart=[];
function addCart(n,p){var found=null;for(var i=0;i<cart.length;i++){if(cart[i].name==n)found=cart[i]}if(found){found.qty++}else{cart.push({name:n,price:p,qty:1})}upd()}
function upd(){var c=0,t=0,h='';for(var i=0;i<cart.length;i++){c+=cart[i].qty;t+=cart[i].price*cart[i].qty;h+='<div style="display:flex;justify-content:space-between;margin:8px 0"><span>'+cart[i].name+' x'+cart[i].qty+'</span><span>Ksh '+(cart[i].price*cart[i].qty)+' <button onclick="rem('+i+')">x</button></span></div>'}document.getElementById('cartCount').innerText=c;document.getElementById('cartTotal').innerText=t;document.getElementById('modalTotal').innerText=t;document.getElementById('cartItems').innerHTML=h||'Empty';document.getElementById('cartBar').style.display=c>0?'block':'none';}
function rem(i){cart.splice(i,1);upd()}
function openCart(){document.getElementById('cartModal').style.display='block'}
function closeCart(){document.getElementById('cartModal').style.display='none'}
function placeOrder(){var name=document.getElementById('custName').value;var phone=document.getElementById('custPhone').value;var room=document.getElementById('custRoom').value;if(!name||!phone){alert('Weka Name na Phone');return}var total=document.getElementById('modalTotal').innerText;var items='';for(var i=0;i<cart.length;i++){items+=cart[i].name+' x'+cart[i].qty+', '}var msg='*NEW ORDER*%0AName: '+name+'%0APhone: '+phone+'%0ARoom: '+room+'%0AOrder: '+items+'%0ATotal: Ksh '+total;fetch('/order',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:name,phone:phone,room:room,items:items,total:total})});window.open('https://wa.me/254799587489?text='+msg,'_blank');alert('Asante! Sent to WhatsApp');cart=[];upd();closeCart();}
</script></body></html>"""
BOSS="""<!doctype html><html><body><h2>BOSS</h2><a href="/">Menu</a><form method="post"><input name="ann" value="{{ann}}"><input name="restock" value="{{restock}}"><button>Update</button></form>{% for n,d in menu.items() %}<p>{{n}} {{d.stock}} <a href="/kitchen/decrease/{{n}}">-1</a> <a href="/kitchen/increase/{{n}}">+5</a></p>{% endfor %}<h3>Orders {{orders|length}}</h3>{% for o in orders %}<p>{{o.name}} {{o.items}} {{o.total}}</p>{% endfor %}</body></html>"""
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
def order(): d=request.get_json(); orders.append(d) if d else None; return "ok"
@app.route('/kitchen/increase/<name>')
def inc(name):
    if name in menu: menu[name]['stock']+=5
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
@app.route('/kitchen/decrease/<name>')
def dec(name):
    if name in menu and menu[name]['stock']>0: menu[name]['stock']-=1
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info, orders=orders)
if __name__=='__main__': app.run(host='0.0.0.0', port=5000)
