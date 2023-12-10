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
hoy = datetime.now().day
esteMes = datetime.now().month
esteaño = datetime.now().year
#la primer variable es el primer dia habil del mes, ese nombre es porque no lo pienso usar
_,diasenmes = calendar.monthrange(esteaño, esteMes)
valores=dict()

compraXpath='/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[1]/td[3]/div/p'
ventaXpath='/html/body/div[2]/div[5]/div/div/div/div/div[1]/div/div/div/table/tbody/tr[2]/td[3]/div/p' 
def cargarpagina(driver):
    driver.get("https://www.brou.com.uy/cotizaciones")        
    valores['compra'],valores['comprafloat'] = fetchValor(driver,compraXpath)
    valores['venta'],valores['ventafloat']=fetchValor(driver,ventaXpath)

def fetchValor(driver,xpath):
    valstr=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,xpath)))
    valstr=valstr.text[0:5]
    valstr=valstr.replace(',','.')
    valfloat=float(valstr)    
    return valstr,valfloat
    
def agregarATabla(compra,venta,año):
   fecha=datetime.today().strftime('%d-%m-%Y')
   nombrecsv='dolar'+str(esteaño)+'.csv' 
   with open(nombrecsv,'a+') as tabla:
       if tabla.tell() == 0:
           tabla.write('Fecha, Dolar Compra, Dolar Venta\n')
       tabla.write('\n')
       tabla.write(fecha + " , ")
       tabla.write(compra + " , ")
       tabla.write(venta)
       tabla.close()    

while hoy == diasenmes :
    cargarpagina(driver)
    agregarATabla(valores['compra'],valores['venta'])
    hoy += 1
    ic("esperando hasta mañana, hoy es: ", hoy) 
    time.sleep(300) 
else:
    hoy = datetime.now().day
    ic('Se actualizo la fecha a: ',hoy)
driver.quit()