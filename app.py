from flask import Flask, request, render_template_string
app = Flask(__name__)

announcement = "Karibu! Leo tuna Pilau, Chapo na Ugali Beef! Orders 7am-8pm"
restock_info = "Pilau itarudi saa 1pm"
pochi = "0799587489"

# YOUR REAL PRICES FROM HANDWRITTEN PAPER
menu = {
    "Chapati": {"price": 20, "stock": 55},
    "Beans + Chapo (Ndengu Mini)": {"price": 80, "stock": 20},
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

orders = []

CUSTOMER = """
<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gracie-Ruth Food</title>
<style>
body{background:#f5f5f0;font-family:Arial;padding:12px;margin:0}
.header{background:#fff9c4;padding:10px;border-radius:8px;border:2px solid #f0c040;margin-bottom:10px;text-align:center}
.pochi{background:#2d5016;color:white;padding:12px;border-radius:8px;margin:10px 0;text-align:center;font-size:18px;font-weight:bold}
.item{background:white;display:flex;justify-content:space-between;align-items:center;padding:12px;margin:6px 0;border-radius:12px;box-shadow:0 2px 4px #ccc}
.add{background:#e65100;color:white;border:none;padding:8px 16px;border-radius:8px;font-weight:bold}
h1{color:#bf360c;margin:10px 0}
</style></head><body>
<div class="header">🔄 Restock: {{restock}}<br>📢 {{ann}}</div>
<div class="pochi">Pochi: {{pochi}}</div>
<h1>Menu Leo</h1>
{% for name, d in menu.items() %}
<div class="item"><span>{{name}} - Ksh {{d.price}} {% if d.stock==0 %}❌{% endif %}</span><button class="add">Add</button></div>
{% endfor %}
<p style="text-align:center;margin-top:20px"><a href="/kitchen">Boss Login</a></p>
</body></html>
"""

BOSS = """
<!doctype html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>GRACIE BOSS CONTROL</title>
<style>
body{background:#fff8e1;font-family:Arial;padding:10px}
.card{background:white;padding:12px;border-radius:10px;margin-bottom:10px;box-shadow:0 2px 4px #ccc}
.btn{padding:6px 10px;border:none;border-radius:6px;margin:2px;color:white;cursor:pointer;font-weight:bold}
.black{background:#212121}.green{background:#2e7d32}.red{background:#6d1b1b}
input{padding:8px;margin:4px;width:95%}
.update{background:#2e7d32;color:white;padding:12px;width:100%;border:none;border-radius:8px;margin-top:8px;font-size:16px}
.top{display:flex;justify-content:space-between;align-items:center}
</style></head><body>
<div class="card"><div class="top"><b>GRACIE BOSS CONTROL</b><span><a href="/">Menu</a> <button style="background:#e65100;color:white;border:none;padding:6px 10px;border-radius:6px">Refresh</button></span></div></div>
<div class="card" style="background:#fff9c4;border:2px solid #f0c040">
<h3>📌 Update Message for Students</h3>
<form method="post">
Cooking Today:<br><input type="text" name="ann" value="{{ann}}"><br>
Restock Info:<br><input type="text" name="restock" value="{{restock}}"><br>
<button class="update" type="submit">Update</button>
</form>
</div>
<h2>Food Control - Only Gracie Sees Stock</h2>
{% for name, d in menu.items() %}
<div class="card" style="display:flex;justify-content:space-between;align-items:center">
<div><b>{{name}} - Ksh {{d.price}} | Stock: {{d.stock}}</b></div>
<div>
<a href="/kitchen/decrease/{{name}}"><button class="btn black">-1</button></a>
<a href="/kitchen/increase/{{name}}"><button class="btn green">+5</button></a>
<a href="/kitchen/zero/{{name}}"><button class="btn red">Imeisha</button></a>
</div>
</div>
{% endfor %}
</body></html>
"""

@app.route('/')
def home(): return render_template_string(CUSTOMER, menu=menu, ann=announcement, restock=restock_info, pochi=pochi)

@app.route('/kitchen')
@app.route('/kitchen_dashboard')
def kitchen(): return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info)

@app.route('/kitchen', methods=['POST'])
@app.route('/kitchen_dashboard', methods=['POST'])
def kitchen_post():
    global announcement, restock_info
    announcement = request.form.get('ann', announcement)
    restock_info = request.form.get('restock', restock_info)
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info)

@app.route('/kitchen/increase/<name>')
def inc(name):
    if name in menu: menu[name]['stock'] += 5
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info)
@app.route('/kitchen/decrease/<name>')
def dec(name):
    if name in menu and menu[name]['stock']>0: menu[name]['stock'] -= 1
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info)
@app.route('/kitchen/zero/<name>')
def zero(name):
    if name in menu: menu[name]['stock'] = 0
    return render_template_string(BOSS, menu=menu, ann=announcement, restock=restock_info)

if __name__ == '__main__': app.run(host='0.0.0.0', port=5000, debug=True)
