from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time,calendar
from datetime import datetime
#import pandas as pd

driver_path= "C:\\Users\\leong\\Downloads\\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
inicio=datetime.now().second
hoy = datetime.now().day
esteMes = datetime.now().month
esteaño = datetime.now().year
#la primer variable es el primer dia habil del mes, ese nombre es porque no lo pienso usar
_,diasenmes = calendar.monthrange(esteaño, esteMes)
compra=''
venta=''

def cargarpagina():
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.brou.com.uy/cotizaciones")        
    fetchValores(driver)
    driver.quit()
    #print('valores',datetime.now().second - inicio)

def fetchValores(driver):
    #compra
    dolar_compra=WebDriverWait(driver,3).until(EC.presence_of_element_located(
            (By.XPATH,'/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[1]/td[3]/div/p')))
    dolar_compra=dolar_compra.text[0:5]
    dolar_compra=dolar_compra.replace(',','.')
    floatdolar_compra=float(dolar_compra)
    venta=dolar_compra

    #venta
    dolar_venta=WebDriverWait(driver,3).until(EC.presence_of_element_located((
            By.XPATH,'/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[2]/td[3]/div/p')))
    dolar_venta=dolar_venta.text[0:5]
    dolar_venta=dolar_venta.replace(',','.')
    floatdolar_venta=float(dolar_venta)
    venta=dolar_venta

def agregarATabla(compra,venta):
   fecha=datetime.today().strftime('%d-%m-%Y') 
   with open('dolar.csv','a+') as tabla:
       if tabla.tell() == 0:
           tabla.write('Fecha, Dolar Compra, Dolar Venta\n')
       tabla.write(fecha + " , ")
       tabla.write(compra + " , ")
       tabla.write(venta + "\n")
       tabla.close()    
   #print("tabla ", datetime.now().second - inicio)

while hoy < diasenmes :
    cargarpagina()
    agregarATabla(compra,venta)
    hoy += 1
    print("esperando hasta mañana, hoy es: ", hoy)    
    time.sleep(86400)
else:
    hoy = datetime.now().day

