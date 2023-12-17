from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time,calendar
from datetime import datetime
#from icecream import ic

#webdriver
driver_path= "C:\\Users\\leong\\Downloads\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
driver = webdriver.Chrome(options=options)
#variables
inicio=datetime.now().second
dia = datetime.now().day
mes = datetime.now().month
#la primer variable es el primer dia habil del mes, ese nombre es porque no lo pienso usar
_,diasenmes = calendar.monthrange(datetime.now().year, mes)
valores={
    'compra' : 0,
    'venta': 0
}
valorexistente=False
compraXpath='/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[1]/td[3]/div/p'
ventaXpath='/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[1]/td[5]/div/p' 

#Refresca los valores desde las paginas y los escribe en valores
def cargarpagina(driver):
    driver.get("https://www.brou.com.uy/cotizaciones")
    #obtener ultimos valores
    valores['compra'] = fetchValor(driver,compraXpath)
    valores['venta']= fetchValor(driver,ventaXpath)

#Consigue los valores mediante Xpath y los devuelve como string 
def fetchValor(driver,xpath):
    valstr=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,xpath)))
    valstr=valstr.text[0:5]
    valstr=valstr.replace(',','.')
    return valstr

def agregarATabla(compra,venta):  
    #Esta es una cantidad desagradable de variables pero por el momento son necesarias
    fecha=datetime.today().strftime('%d-%m-%Y')
    año = str(datetime.now().year)
    try:
        df = pd.read_excel('dolar.xlsx')   
    except(FileNotFoundError):
        #Escribir Header y datos si no existe
        new_data = pd.DataFrame({
        'Fecha': [fecha],
        'Dolar Compra': [compra],
        'Dolar Venta': [venta]
        })
        #ic("escribiendo en xlsx vacio",new_data)
        with pd.ExcelWriter('dolar.xlsx') as writer:
            new_data.to_excel(writer,index=False,sheet_name=año)
        return False       
    #primerafila=df.iloc[[0]].values[0].tolist()
    ultimafila = df.iloc[[-1]].values[0].tolist()
    nuevafila=[fecha,float(compra),float(venta)]

    #ic(primerafila,ultimafila,nuevafila)

    if ultimafila==nuevafila:
        #ic("El valor obtenido es el ultimo valor de la tabla")
        return True
    else:
        df.loc[len(df.index)] = [fecha,compra,venta]   
        return False


#repetir cada dia
while True:
    cargarpagina(driver)
    valorexistente=agregarATabla(valores['compra'],valores['venta'])
    while valorexistente==True:
        print("valor existe esperando 5 min")
        time.sleep(300)
        valorexistente=agregarATabla(valores['compra'],valores['venta'])
    if valorexistente == False:
        print("Valor de hoy actualizado esperando a mañana")
        time.sleep(86400) 