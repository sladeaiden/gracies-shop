from flask import Flask, session, request, redirect, render_template_string
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "gracie-ruth-final-2026"

announcement = "Karibu! Leo tuna Pilau, Chapo, Ugali Beef na Chips! Orders 7am-8pm"
restock_info = "Pilau itarudi saa 1pm - Chips ziko!"
pochi = "0799587489"

# YOUR FULL 15 ITEMS FROM NOTEBOOK
MENU = {
    "Chapati": {"price": 20, "stock": 100, "emoji": "🫓", "id": 1},
    "Beans+Chapo": {"price": 80, "stock": 30, "emoji": "🍛", "id": 2},
    "Beans+Chapo Large": {"price": 100, "stock": 20, "emoji": "🍛", "id": 3},
    "Pilau Regular": {"price": 80, "stock": 15, "emoji": "🍚", "id": 4},
    "Pilau Large": {"price": 100, "stock": 15, "emoji": "🍚", "id": 5},
    "Mandazi": {"price": 10, "stock": 100, "emoji": "🍩", "id": 6},
    "Tea": {"price": 20, "stock": 100, "emoji": "☕", "id": 7},
    "Chapo Chipo": {"price": 60, "stock": 25, "emoji": "🥙", "id": 8},
    "Chips Small": {"price": 60, "stock": 30, "emoji": "🍟", "id": 9},
    "Chips Medium": {"price": 80, "stock": 30, "emoji": "🍟", "id": 10},
    "Chips Large": {"price": 100, "stock": 20, "emoji": "🍟", "id": 11},
    "Ugali Beef": {"price": 150, "stock": 15, "emoji": "🍖", "id": 12},
    "Soda (Fanta)": {"price": 50, "stock": 30, "emoji": "🥤", "id": 13},
    "Pepsi": {"price": 40, "stock": 30, "emoji": "🥤", "id": 14},
    "Predator": {"price": 70, "stock": 25, "emoji": "🧃", "id": 15},
    "Minute Maid": {"price": 80, "stock": 20, "emoji": "🧃", "id": 16},
    "Yoghurt": {"price": 60, "stock": 20, "emoji": "🥛", "id": 17},
    "Sausage": {"price": 40, "stock": 30, "emoji": "🌭", "id": 18},
    "Samosa": {"price": 40, "stock": 30, "emoji": "🥟", "id": 19},
}

ORDERS = []

STYLE = "<style>body{font-family:Arial; background:#fff8f0; margin:0; padding:15px;}.header{background:#fff9c4; padding:12px; border-radius:10px; border:2px solid #f0c040; margin-bottom:15px;}.pochi{background:#2d5016; color:white; padding:12px; border-radius:8px; text-align:center; font-size:18px; margin-bottom:15px;}.card{background:white; border-radius:15px; padding:12px; margin:8px; box-shadow:0 2px 8px #ccc; display:inline-block; width:165px; text-align:center; vertical-align:top;} button{background:#e65100; color:white; border:none; padding:7px 12px; border-radius:20px; cursor:pointer; font-weight:bold;}.top{display:flex; justify-content:space-between; background:white; padding:10px 15px; border-radius:10px; margin-bottom:10px;}</style>"

HOME_HTML = STYLE + """
<div class="top"><b>💖 Gracie-Ruth</b><div><a href='/kitchen?password=gracie123'>👩‍🍳 Boss</a> | <a href='/cart'>🛒 Cart ({{ count }})</a></div></div>
<div class="header">🔄 {{ restock }}<br>📢 {{ ann }}</div>
<div class="pochi">📱 Pochi: {{ pochi }} - Lipa na Mpesa 💚</div>
<h1 style="text-align:center; color:#bf360c;">Menu Leo - All Foods 🍽️</h1>
<div style="text-align:center;">
{% for name, data in menu.items() %}
  <div class="card">
    <div style="font-size:35px;">{{ data.emoji }}</div>
    <b style="font-size:13px;">{{ name }}</b><br>Ksh {{ data.price }}<br><small>{{ data.stock }} left</small><br>
    <a href="/add/{{ name }}"><button {% if data.stock==0 %}disabled style="background:grey"{% endif %}>Add</button></a>
  </div>
{% endfor %}
</div>
"""

CART_HTML = STYLE + """
<div class="top"><a href="/">← Menu</a><b>🛒 Cart</b><div></div></div>
<div style="max-width:500px; margin:auto; background:white; padding:20px; border-radius:15px;">
{% if not cart %}
  <p style="text-align:center;">Cart empty <a href="/">Shop now</a></p>
{% else %}
  {% for item in cart %}
    <p>{{ item.emoji }} {{ item.name }} x {{ item.qty }} = Ksh {{ item.price * item.qty }}</p>
  {% endfor %}
  <h3>Total: Ksh {{ total }}</h3><hr>
  <form method="post" action="/checkout">
    Name: <input name="name" required style="width:100%; padding:8px; margin:5px 0;"><br>
    Phone: <input name="phone" required style="width:100%; padding:8px; margin:5px 0;"><br>
    Pickup: <input type="time" name="pickup" required style="width:100%; padding:8px; margin:5px 0;"><br>
    Mpesa Code: <input name="mpesa_code" required placeholder="e.g. QHX123" style="width:100%; padding:8px; border:2px solid green; margin:5px 0;"><br>
    <button type="submit" style="width:100%; padding:12px; background:green; margin-top:10px;">✅ Place Order</button>
  </form>
{% endif %}
</div>
"""

KITCHEN_HTML = STYLE + """
<h1 style="text-align:center;">👩‍🍳 GRACIE BOSS CONTROL - ALL ORDERS</h1>
<div style="text-align:center;"><a href="/">Menu</a> | <a href="/kitchen?password=gracie123"><button>🔄 Refresh</button></a> | Orders: {{ orders|length }}</div>
<div class="header">
<h3>📌 Update Message for Students</h3>
<form method="post">Cooking:<br><input type="text" name="ann" value="{{ ann }}" style="width:95%; padding:8px;"><br>Restock:<br><input type="text" name="restock" value="{{ restock }}" style="width:95%; padding:8px;"><br><button type="submit" style="background:green; width:100%; margin-top:8px; padding:10px;">Update</button></form>
</div>
<h2>Food Stock Control (-1 +5 Imeisha)</h2>
{% for name, data in menu.items() %}
<div style="background:white; padding:8px; border-radius:10px; margin:6px 0; display:flex; justify-content:space-between; align-items:center; font-size:14px;">
<div><b>{{ data.emoji }} {{ name }} - Ksh {{ data.price }} | {{ data.stock }}</b></div>
<div><a href="/kitchen/decrease/{{ name }}?password=gracie123"><button style="background:#212121;">-1</button></a>
<a href="/kitchen/increase/{{ name }}?password=gracie123"><button style="background:#2e7d32;">+5</button></a>
<a href="/kitchen/zero/{{ name }}?password=gracie123"><button style="background:#b71c1c;">Imeisha</button></a></div>
</div>
{% endfor %}
<h2>🔥 LIVE ORDERS - Shows Food + Mpesa (FIXED!)</h2>
{% for order in orders[::-1] %}
<div style="border:3px solid #e65100; background:white; padding:15px; border-radius:15px; margin:15px 0;">
<b>{{ order.number }} - {{ order.name }} - 📞 {{ order.phone }}</b><br>Pickup: {{ order.pickup }} | {{ order.time }}<br><br>
<div style="background:#fff3e0; padding:10px; border-radius:10px;">
<b style="color:#bf360c;">🍽️ FOOD ORDERED:</b><br>
{% for food in order['items'] %}
  {{ food['emoji'] }} {{ food['name'] }} x {{ food['qty'] }} = Ksh {{ food['price'] * food['qty'] }}<br>
{% endfor %}
<b>Total: Ksh {{ order.total }}</b></div>
<p>Mpesa Code: <b style="color:green; background:#e8f5e9; padding:5px 10px; border-radius:5px; font-size:20px;">{{ order.mpesa_code }}</b></p>
<a href="/done/{{ loop.revindex0 }}?password=gracie123"><button style="background:green;">✅ DONE</button></a>
</div>
{% else %}<p>No orders ⏳</p>{% endfor %}
"""

@app.route("/")
def home():
    cart=session.get("cart",[]); count=sum(i["qty"] for i in cart)
    return render_template_string(HOME_HTML, menu=MENU, count=count, ann=announcement, restock=restock_info, pochi=pochi)

@app.route("/add/<name>")
def add(name):
    if name not in MENU or MENU[name]["stock"]<=0: return redirect("/")
    cart=session.get("cart",[])
    for c in cart:
        if c["name"]==name: c["qty"]+=1; break
    else: cart.append({"name":name, "price":MENU[name]["price"], "emoji":MENU[name]["emoji"], "qty":1})
    session["cart"]=cart; return redirect("/cart")

@app.route("/cart")
def cart_page():
    cart=session.get("cart",[]); total=sum(i["price"]*i["qty"] for i in cart)
    return render_template_string(CART_HTML, cart=cart, total=total)

@app.route("/checkout", methods=["POST"])
def checkout():
    cart=session.get("cart",[])
    if not cart: return redirect("/")
    total=sum(i["price"]*i["qty"] for i in cart)
    number=f"GR-{random.randint(100,999)}"
    order={"number":number, "name":request.form["name"], "phone":request.form["phone"], "pickup":request.form["pickup"], "mpesa_code":request.form["mpesa_code"], "items":cart, "total":total, "time":datetime.now().strftime("%I:%M %p")}
    ORDERS.append(order)
    for item in cart:
        if item["name"] in MENU and MENU[item["name"]]["stock"]>=item["qty"]: MENU[item["name"]]["stock"]-=item["qty"]
    session["cart"]=[]
    return STYLE + f"<div style='max-width:500px; margin:50px auto; background:white; padding:30px; border-radius:15px; text-align:center;'><h1>✅ Asante {order['name']}!</h1><h2>Order {number}</h2><p>Total Ksh {total}</p><a href='/'><button>Order More</button></a> <a href='/kitchen?password=gracie123'><button style='background:green;'>Kitchen</button></a></div>"

@app.route("/kitchen", methods=["GET","POST"])
def kitchen():
    global announcement, restock_info
    pwd=request.args.get("password","") or request.form.get("password","")
    if request.method=="POST": announcement=request.form.get("ann",announcement); restock_info=request.form.get("restock",restock_info)
    if pwd!="gracie123" and pwd!="gracie 123": return STYLE + '<div style="max-width:400px; margin:100px auto; background:white; padding:30px; border-radius:15px; text-align:center;"><h1>🔒 Kitchen Login</h1><form>Password: <input type="password" name="password" style="padding:8px;"><button>Login</button></form></div>'
    return render_template_string(KITCHEN_HTML, menu=MENU, orders=ORDERS, ann=announcement, restock=restock_info)

@app.route("/kitchen/<action>/<name>")
def stock_action(action,name):
    if name in MENU:
        if action=="increase": MENU[name]["stock"]+=5
        elif action=="decrease" and MENU[name]["stock"]>0: MENU[name]["stock"]-=1
        elif action=="zero": MENU[name]["stock"]=0
    return redirect("/kitchen?password=gracie123")

@app.route("/done/<int:index>")
def done(index):
    if 0 <= index < len(ORDERS): ORDERS.pop(index)
    return redirect("/kitchen?password=gracie123")

if __name__=="__main__": app.run(debug=True)