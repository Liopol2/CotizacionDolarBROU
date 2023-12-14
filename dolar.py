from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time,calendar
from datetime import datetime
from icecream import ic
#import pandas as pd
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
ventaXpath='/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[2]/td[3]/div/p' 

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

def ultimalinea(nombrecsv): 
    count=0    
    with open(nombrecsv) as f:
        for line in f:
            count += 1
        lastline = line
        return lastline,count


def agregarATabla(compra,venta,dia,mes):  
    lineas=0 
    #Esta es una cantidad desagradable de variables pero por el momento son necesarias
    fecha=datetime.today().strftime('%d-%m-%Y')
    año = datetime.now().year
    nombrecsv='dolar'+str(año)+'.csv' 

    with open(nombrecsv,'a+') as tabla: 
            if tabla.tell() == 0:
                tabla.write('Fecha,Dolar Compra,Dolar Venta\n')
            if dia == 1:
                tabla.write('\n'+str(mes))
            last_line,lineas = ultimalinea(nombrecsv)
            if lineas > 1:
                ucompra = str(last_line[11:16])
                uventa = str(last_line[17:23])  
                ic(nombrecsv,lineas,last_line,ucompra,compra,uventa,venta)
                if ucompra == compra and uventa == venta:           
                    print('este valor ya existe')
                    return True                        
                row=str('\n'+ fecha + "," + str(compra) + ","+ str(venta))
                ic(row)
                tabla.write(row)
                tabla.close()     
                return False
    #repetir cada dia
while True:
    cargarpagina(driver)
    valorexistente=agregarATabla(valores['compra'],valores['venta'],dia,mes)
    while valorexistente==True:
        print("valor existe esperando 5 min")
        time.sleep(300)
        valorexistente=agregarATabla(valores['compra'],valores['venta'],dia,mes)
    if valorexistente == False:
        print("Valor de hoy actualizado esperando a mañana")
        time.sleep(86400) 