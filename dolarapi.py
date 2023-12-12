from flask import Flask,request,render_template
from datetime import datetime
from icecream import ic

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/dolarapi")
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
    if fecha=="":
        fechadefault=True
    #seleccionar fecha
    if lfecha<3:
        fecha += "-" +str(datetime.now().month) + "-"+ str(datetime.now().year)
        if int(fecha)>hoy:
            return "Todavia no es "+ fecha +"para ver el valor de "+ fecha + "en otro mes agregue el mes ej: <valoractual>-12" 
    if lfecha > 2 and lfecha < 6:
        fecha += "-" + str(datetime.now().year)
    if lfecha > 10 :
        return "error de formato use algo como: " + hoy
        
    with open('dolar2023.csv') as f:
        for line in f:
            count += 1
            fechacsv,_,_=line.split(",")
            if fechacsv==fecha:
                fechacsv,valores["compra"],valores["venta"]=line.split(',')
                #quitar el newline de las lineas previas al final
                valores["venta"]=valores["venta"][0:-1]                            
        if fechacsv != line.split(",")[0] and fechadefault==True:
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

if __name__ == "__main__":
    app.run(debug=True)