from flask import Flask,request,render_template
from datetime import datetime
from icecream import ic

app = Flask(__name__)
valores={
    "compra":0,
    "venta":0
}
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/dolarapi/<valor>")
def valor(fecha=datetime.today().strftime('%d-%m-%Y'),valor='cv'):
    count=0
    with open('dolar2023.csv') as f:
        for line in f:
            count += 1
        lastline = line
    ic(fecha)
    _,valores["compra"],valores["venta"]=lastline.split(',')
    if valor== 'c':
        return valores["compra"]
    elif valor== 'v':
        return valores["venta"]  
    else : return valores
if __name__ == "__main__":
    app.run(debug=True)