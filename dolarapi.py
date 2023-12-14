from flask import Flask,request,render_template
from datetime import datetime
from icecream import ic
import pandas as pd
from matplotlib import pyplot as plt
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/dolarapi",methods=['GET', 'POST'])
def valor():
    if request.method == "POST":            
        valores={
            "compra":0,
            "venta":0
        }
        count=0
        hoy=datetime.today().strftime('%d-%m-%Y')
        valor=request.args.get('valor',"cv")
        fecha=str(request.args.get('fecha',""))
        lfecha=len(fecha)
        fechadefault=False
        fechacsv=''
        if fecha=="":
            fechadefault=True
            fecha=str(datetime.today().day)
        #seleccionar fecha
        if lfecha<3:
            fecha += "-" +str(datetime.now().month) + "-"+ str(datetime.now().year)
        if lfecha > 2 and lfecha < 6:
            fecha += "-" + str(datetime.now().year)
        if lfecha > 10 :
            return "error de formato use algo como: " + hoy
            
        with open('dolar2023.csv') as f:
            for line in f:
                count += 1
                fechacsv,_,_=line.split(",")
                if fechacsv==fecha and fechadefault==False:
                    fechacsv,valores["compra"],valores["venta"]=line.split(',')
                    #quitar el newline de las lineas previas al final
                    valores["venta"]=valores["venta"][0:-1]                            
            if fechacsv == line.split(",")[0] and fechadefault==True:
                lastline = line
                fechacsv,valores["compra"],valores["venta"]=lastline.split(',')
            if fechadefault==False and valores["compra"] == 0:
                    ic(fecha,fechacsv,valores)
                    return "No se encontro el valor para la fecha"
        ic(fecha,fechacsv,valores)
        
        if valor== 'c':
            return valores["compra"]
        elif valor== 'v':
            return valores["venta"]  
        else : return valores
    elif request.method=="GET":
        return render_template('dolarapi.html')
@app.route("/grafica",methods=['GET', 'POST'])
def plotear():
    if request.method=="GET":
        return render_template("dolargrafica.html")
    if request.method=="POST":
        nombre=request.args.get('year',"dolar"+str(datetime.today().year))
        df = pd.read_csv(nombre+'.csv')
        df.head()
        print(nombre,df.head())
        fecha=df["Fecha"]
        compra=df["Dolar Compra"]
        venta=df["Dolar Venta"]
        #plt.ion()
        plt.plot(fecha,compra,linewidth=3,label='Compra')
        plt.plot(fecha,venta,linewidth=3,linestyle="--",label='Venta')
        plt.xlabel('Fecha')
        plt.ylabel('Precio($UY)')
        plt.title('Valor Dolar Venta ($UY)')
        plt.savefig(nombre+'.png')
        plt.show()
        return nombre

if __name__ == "__main__":
    app.run(debug=True)