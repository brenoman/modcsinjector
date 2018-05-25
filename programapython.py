from threading import Thread
import subprocess
import thread
import time
import datetime
import numpy

# Define a function for the thread

def injetar_reparo_falha(tamanhofalha, escalafalha, tamanhoreparo, escalareparo, comandofalha, comandoreparo):
	while 1:
		tempofalha = numpy.random.exponential(tamanhofalha, escalafalha)
		print "Proxima falha: "+str(tempofalha)
		time.sleep(tempofalha)
		sinalizar("injecao de falha")
		output = subprocess.check_output(['bash','-c', comandofalha])
		temporeparo = numpy.random.exponential(tamanhoreparo, escalareparo)
		print "Proximo reparo: "+str(temporeparo)
		time.sleep(temporeparo)
		output = subprocess.check_output(['bash','-c', comandoreparo])
		sinalizar("injecao de reparo")

def monitorar(servicon,checagemservico):
	servico = 1
	while 1:
		print "AQUI: "+checagemservico
		import subprocess
		print(repr(checagemservico))
		output = subprocess.Popen(checagemservico, shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
		if servico==1 and output=='0':
			servico=0
			with open("monitoramento.txt", "a") as myfile:
				data = datetime.datetime.now()
				print str(data) +servicon+" D"
				myfile.write(str(data) + servicon+" D"+"\n")
		elif servico==0 and output=='1':
			servico=1
			with open("monitoramento.txt", "a") as myfile:
				data = datetime.datetime.now()
				print str(data) +servicon+" U"
				myfile.write(str(data) + servicon+"U"+"\n")

def sinalizar(string):
	with open("monitoramento.txt", "a") as myfile:
		data = datetime.datetime.now()
		myfile.write(str(data) + " ### "+string+"\n")



print """
    __  _______      __             ____        _           __            
   /  |/  / __ \____/ /_________   /  _/___    (_)__  _____/ /_____  _____
  / /|_/ / / / / __  / ___/ ___/   / // __ \  / / _ \/ ___/ __/ __ \/ ___/
 / /  / / /_/ / /_/ / /__(__  )  _/ // / / / / /  __/ /__/ /_/ /_/ / /    
/_/  /_/\____/\__,_/\___/____/  /___/_/ /_/_/ /\___/\___/\__/\____/_/     
                                         /___/                            """

def captura_inputs():
	try:
		nome = ""
		while nome != "k":
			print "Digite o nome do servico"
			nome = "mysql" #raw_input()
			if nome=="k":
				continue
			print "Digite o comando para verificar o servico"
			comandoverificarservico = raw_input()
			print "Digite o comando para derrubar o servico"
			comandoderrubarservico = raw_input()
			print "Digite o comando para levantar o servico"
			comandolevantarservico = raw_input()
			print "Digite a taxa de falha do servico"
			taxadefalha = raw_input()
			print "Digite a taxa de reparo do servico"
			taxadereparo = raw_input()
			try:
				t = Thread(target=monitorar, args=(nome, comandoverificarservico))
				t.daemon = True
				t.start()
				t2 = Thread(target=injetar_reparo_falha, args=(taxadefalha,1,taxadereparo,1,comandoderrubarservico,comandolevantarservico))
				t2.daemon = True
				t2.start()
			except e:
				print "erro" + str(e)
			nome='k'
		
	
	except Exception as e:
		print str(e)

	while 1:
		pass

def captura_csv():
	i=0
	with open("inputmi.txt", "r") as ins:
	    array = []
	    for line in ins:
		try:
			if i==0:
				next
			print str(i) + "\n"
			linha = line.split(",")
			print line
			nome = linha[0]
			comandoverificarservico = str(linha[1])
			comandoderrubarservico = str(linha[2])
			comandolevantarservico = str(linha[3])
			taxadefalha = float(linha[4])
			taxadereparo = float(linha[5])
			try:
				t = Thread(target=monitorar, args=(nome, comandoverificarservico))
				t.daemon = True
				t.start()
				t2 = Thread(target=injetar_reparo_falha, args=(taxadefalha,1,taxadereparo,1,comandoderrubarservico,comandolevantarservico))
				t2.daemon = True
				t2.start()
			except e:
				print "erro" + str(e)
		except Exception as e:
			pass

print "[A]rquivo ou [I]nput?"
resposta = raw_input()
if resposta == "A":
	captura_csv()
else:
	captura_inputs()
