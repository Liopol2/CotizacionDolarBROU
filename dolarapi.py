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
        if fecha=="" and valor == "cv":
            return render_template('dolarapi.html')
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
            
        with open('dolar.csv') as f:
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
        ic(fecha,fechacsv,valores,valor)
        
        if valor== 'c':
            return valores["compra"]
        elif valor== 'v':
            return valores["venta"]  
        else : return valores
        
    
@app.route("/grafica",methods=['GET', 'POST'])
def plotear():
    hoy=datetime.today().strftime('%d-%m-%Y')
    diahoy=datetime.today().day
    meshoy=datetime.today().month
    añohoy=datetime.today().year
    if request.method=="GET":
        return render_template("dolargrafica.html")
    
    if request.method=="POST":
        #Argumentos
        Fin=request.args.get('Fin',hoy) 
        FinS=Fin.split("-")
        #Uso el año y el mes de la fecha de cierre por defecto
        primerodelmes="1-"+str(FinS[1])+'-'+str(FinS[2])
        Inicio=request.args.get('Inicio',primerodelmes)
        InicioS=Inicio.split('-')
        ic(Inicio,InicioS,Fin,FinS)
        #Cargo el xlsx a un dataframe
        df = pd.read_excel('dolar.xlsx')
        ic(df)

        #Verificar que el inicio este en la lista
        primerafila=df.iloc[[0]].values[0].tolist()
        ultimafila = df.iloc[[-1]].values[0].tolist()

        primerafecha=primerafila[0].split('-')
        ic(primerafila,ultimafila,primerafecha)
        #leo el excel fila por fila
        for i in df.values[0].tolist():    
            if (int(FinS[0]) > diahoy and
                int(FinS[1]) > meshoy and
                int(FinS[2]) > añohoy):
                return "No se pueden encontrar valores futuros. Todavia!"
            if (int(InicioS[0]) < int(primerafecha[0]) and
                int(InicioS[1]) < int(primerafecha[0]) and
                int(InicioS[2]) < int(primerafecha[0])):
                return "Ese valor precede a la existencia de la base de datos"
            ic(98,i)
        print(Inicio,Fin)
        #usando inicio y fin pasar los valores a un dataframe
        #eje x
        df_selected = df[df['Fecha'].between(Inicio, Fin)]
        fechas=df_selected["Fecha"]
        ic("dataframe recortado",df_selected)
        #Valores en y
        compra=df_selected["Dolar Compra"]
        venta=df_selected["Dolar Venta"]

        plt.plot(fechas,compra,linewidth=3,label='Compra')
        plt.plot(fechas,venta,linewidth=3,linestyle="--",label='Venta')
        plt.xlabel('Fecha')
        plt.ylabel('Precio($UY)')
        plt.title('Valor Dolar Venta ($UY)')
        with pd.ExcelWriter('dolar.xlsx') as writer:
            df.insert(0, "Fecha")
            df.insert(1, "Dolar Compra")
            df.insert(2, "Dolar Venta")
            df.to_excel(writer,sheet_name="Sheet1",index=False)
        plt.savefig('static/dolar.png')
        return render_template("grafica.html")

if __name__ == "__main__":
    app.run(debug=True)