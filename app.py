from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    phone = request.form['phone']
    food = request.form['food']
    return f"Thanks {name}! Your order for {food} received. We will call {phone}"

if __name__ == '__main__':
    app.run(debug=True)