from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time,calendar
from datetime import datetime
import pandas as pd

driver_path= "C:\\Users\\leong\\Downloads\\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
hoy = datetime.now().day
esteMes = datetime.now().month
esteaño = datetime.now().year
#la primer variable es el primer dia habil del mes, ese nombre es porque no lo pienso usar
_,diasenmes = calendar.monthrange(esteaño, esteMes)
valores=dict()
def cargarpagina():
    driver = webdriver.Chrome(options=options)
    time.sleep(1)
    driver.get("https://www.brou.com.uy/cotizaciones")
    WebDriverWait(driver,3)    
    fetchValores(driver)
    driver.quit()

def fetchValores(driver):
    #compra
    dolar_compra=driver.find_element(By.XPATH,'/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[1]/td[3]/div/p')
    dolar_compra=dolar_compra.text[0:5]
    dolar_compra=dolar_compra.replace(',','.')
    floatdolar_compra=float(dolar_compra)
    print('Dolar compra: ',dolar_compra)
    valores['compra']=dolar_compra

    #venta
    dolar_venta= driver.find_element(By.XPATH,'/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[2]/td[3]/div/p')
    dolar_venta=dolar_venta.text[0:5]
    dolar_venta=dolar_venta.replace(',','.')
    floatdolar_venta=float(dolar_venta)
    print('Dolar venta: ',dolar_venta)
    valores['venta']=dolar_venta

def agregarATabla(compra,venta):
    fecha=datetime.today().strftime('%d-%m-%Y') 
    if(open('dolar.csv','r')==False):
        tabla=open('dolar.csv','a')
        tabla.write('Fecha, Dolar Compra, Dolar Venta')
    else:
        tabla = open('dolar.csv',"a")
    tabla.write('\n')
    tabla.write(fecha + " , ")
    tabla.write(str(compra) + " , ")
    tabla.write(str(venta))
    tabla.close()

while hoy < diasenmes :
    cargarpagina()
    agregarATabla( valores['compra'],valores['venta'])
    hoy += 1
    print("esperando hasta mañana, hoy es: ", hoy)    
    time.sleep(86400)
else:
    hoy = datetime.now().day

