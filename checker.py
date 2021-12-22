# Importing libraries
import time
import hashlib
import re
import pywhatkit as pw
from re import sub
from decimal import Decimal
from difflib import SequenceMatcher as SM
from urllib.request import urlopen, Request
from datetime import datetime

def strHoy():
  return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def printLog(str):
	print(strHoy() + " " + str)

def removeFLChar(s):
    return s[1 : -1]

url = Request('https://www.kavak.com/orden-menor-precio/compra-de-autos',
			headers={'User-Agent': 'Mozilla/5.0'})


targets={"Mazda 3", "Fiesta"}

montoMaximo=Decimal(130000)

newHash = hashlib.sha224("".encode('utf-8')).hexdigest()

minutosEspera = 5

i=0

while True:
	try:
		
		i += 1

		printLog("Iteration: " + str(i))

		response = urlopen(url).read()

		currentHash = hashlib.sha224(response).hexdigest()

		if newHash != currentHash:

			printLog("Page changed")

			newHash = currentHash

			cards = re.findall("car-name.*?app-card-car", response.decode("utf8").replace('\n', ' ').replace('\r', ' '))

			founded = []
			for card in cards:

				noTags = re.findall(">.*?<", card)
				
				for noTag in noTags:
					noTags[noTags.index(noTag)]=removeFLChar(noTag).strip()
					

				noTags = list(filter(None, noTags))

				printLog(' : '.join(noTags))

				for target in targets:
					posibilidad = SM(None, noTags[0], target).ratio()
					printLog("Posibilidad " + target + " : " + str(round(posibilidad,2)))

					if posibilidad > 0.5 or str(target) in str(noTags):
						printLog("Founded!")
						monto = Decimal(sub(r'[^\d.]', '', noTags[2]))
						
						if len(noTags) > 3:
							monto = Decimal(sub(r'[^\d.]', '', noTags[3])) if monto > Decimal(sub(r'[^\d.]', '', noTags[3])) else monto
						printLog("Monto: " + str(monto))

						if monto < montoMaximo :
							founded.append(noTags)

				print('')
			
			if founded:
				printLog("Founded : ")
				print(founded)
				print()

				mensaje = "Autos de interes :\n\n"
				for itemFound in founded:
					for i in itemFound:
						mensaje += i + "\n"
					mensaje += "\n\n"

				dt = datetime.now()
				min = 0 if dt.minute >= 59 else dt.minute + 1
				hour = hour + 1 if dt.minute >= 59 else dt.hour
				printLog("El mensaje se entregara a las " + str(hour) + ":" + str(min) + " con el mensaje:")
				print(mensaje)
				whats = pw.sendwhatmsg(
					"+5215610174752", 
					mensaje, 
					hour, 
					min)
				printLog(str(whats))

		print()
		printLog("Tiempo de espera siguiente Iteracion: " + str(minutosEspera) + " mins")
		time.sleep(minutosEspera * 60)
	
	except Exception as e:
		print(e)

