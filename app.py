from flask import Flask, request, render_template_string
app = Flask(__name__)
announcement = "Karibu! Leo tuna Pilau, Chapo na Ugali Beef! Orders 7am-8pm"
restock_time = "Pilau itarudi saa 1pm"
stock = {"Pilau": {"price": 300, "available": True}, "Chapo": {"price": 100, "available": True}, "Ugali Beef": {"price": 350, "available": True}, "Chips": {"price": 450, "available": False}}
orders = []
CUSTOMER = """<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>Gracie-Ruth Food</title><style>body{background:#fdf6e3;font-family:Arial;text-align:center;padding:20px}.box{background:white;padding:10px 20px;margin:10px;display:inline-block;border-radius:8px;box-shadow:0 2px 5px #ccc}.unavailable{opacity:.4}.announce{background:#4CAF50;color:white;padding:15px;border-radius:10px;margin:20px}input{padding:10px;margin:5px;width:200px}button{background:#2d5016;color:white;padding:10px 20px;border:none}</style></head><body><h1>Gracie-Ruth Food</h1><div class="announce">{{announcement}}<br><small>{{restock}}</small></div><div>{% for n,i in stock.items() %}<div class="box {{'unavailable' if not i.available}}">{{n}} {{i.price}} {{'❌' if not i.available else '✅'}}</div>{% endfor %}</div><h3>Order</h3><form method="post" action="/order"><input name="name" placeholder="Name" required><br><input name="phone" placeholder="Phone" required><br><input name="food" placeholder="Food" required><br><button>Book</button></form></body></html>"""
BOSS = """<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><title>GRACIE BOSS CONTROL</title><style>body{background:#fff9db;font-family:Arial;padding:20px}.card{background:white;border:2px solid #2d5016;padding:20px;border-radius:12px;max-width:700px;margin:auto;margin-bottom:20px}h1{color:#2d5016;text-align:center}label{font-weight:bold;display:block;margin-top:10px}input[type=text]{width:100%;padding:10px;margin:5px 0;box-sizing:border-box}button{background:#2d5016;color:white;padding:12px;width:100%;border:none;margin-top:10px;font-size:16px}.item{display:flex;justify-content:space-between;padding:8px;border-bottom:1px solid #eee}</style></head><body><h1>GRACIE BOSS CONTROL</h1><div class="card"><h2>Update Message for Students</h2><form method="post"><label>Cooking Today:</label><input type="text" name="announcement" value="{{announcement}}"><label>Restock Info:</label><input type="text" name="restock" value="{{restock}}"><h2 style="margin-top:20px">Stock Control</h2>{% for n,i in stock.items() %}<div class="item"><span>{{n}} - {{i.price}} KES</span><label><input type="checkbox" name="avail_{{n}}" {{'checked' if i.available}}> Available</label></div>{% endfor %}<button>SAVE & UPDATE PUBLIC SITE</button></form></div><div class="card"><h3>Orders Today: {{orders|length}}</h3>{% for o in orders %}<p>{{o.name}} - {{o.phone}} - {{o.food}}</p>{% endfor %}</div><p style="text-align:center"><a href="/">View Customer Site</a><br>gracies-shop.onrender.com/kitchen_dashboard</p></body></html>"""
@app.route('/')
def home(): return render_template_string(CUSTOMER, stock=stock, announcement=announcement, restock=restock_time)
@app.route('/order', methods=['POST'])
def order(): orders.append({"name": request.form.get('name'), "phone": request.form.get('phone'), "food": request.form.get('food')}); return "<h1>Asante! Order Received!</h1><a href='/'>Back</a>"
@app.route('/kitchen_dashboard', methods=['GET','POST'])
def kitchen():
    global announcement, restock_time
    if request.method == 'POST':
        announcement = request.form.get('announcement', announcement); restock_time = request.form.get('restock', restock_time)
        for n in stock: stock[n]['available'] = f'avail_{n}' in request.form
    return render_template_string(BOSS, stock=stock, announcement=announcement, restock=restock_time, orders=orders)
if __name__ == '__main__': app.run(debug=True)
