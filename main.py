import dolar,dolarapi,time,calendar
from threading import Thread
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

#repetir cada dia
while True:
    dolar.cargarpagina(driver)
    valorexistente=dolar.agregarATabla(valores['compra'],valores['venta'])
    while valorexistente==True:
        print("valor existe esperando 5 min")
        time.sleep(300)
        valorexistente=dolar.agregarATabla(valores['compra'],valores['venta'])
    if valorexistente == False:
        print("Valor de hoy actualizado esperando a mañana")
        time.sleep(86400) 
