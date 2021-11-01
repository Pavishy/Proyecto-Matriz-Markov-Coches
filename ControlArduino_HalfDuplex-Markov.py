import serial as s
import numpy as n
import sys
from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "ControlArduino_HalfDuplex-Markov.ui"  # Nombre del archivo de pyqt

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) # la carga del archivo en ventana

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow): #es la clase de los widgets
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.arduino = None #cargamos la libreria de arduino para la conexion

        self.btn_conexion.clicked.connect(self.conexion) #es el boton con la funcion de conexion

        self.SegundoPlano = QtCore.QTimer() # esto es un timer de el widget que mostrara los datos
        self.SegundoPlano.timeout.connect(self.accion) #

        self.btn_control.clicked.connect(self.control)

        self.valorSensor1 = -1 #sensores inicializados en -1
        self.valorSensor2 = -1
        self.valorSensor3 = -1

        self.btn_control.setText("ENVIAR ACCIÓN") #boton de control con su texto de envio de accion

    def control(self):
        self.valorSensor1 /= 1000 #682 / 1000 = 0.682
        self.valorSensor2 /= 1000
        self.valorSensor3 /= 1000

        T = [0.6, 0.2, 0.2], [0.3, 0.4, 0.3], [0.1, 0.4, 0.5] # nuestra matris de carros

        P_inicial = [float(self.valorSensor1), float(self.valorSensor2), float(self.valorSensor3)] # el p0

        matrizT = n.array(T) # se convierte en matriz
        matriz_P0 = n.array(P_inicial) # tambien pero de p0

        estadoDeseado = int(self.txt_P0.text()) #se muestra el estado deseado (lo que ingresamos de teclado en qt)

        estadoActual = matriz_P0 # la matriz se guarda, en estado actual
        for i in range(estadoDeseado): # se hace la operacion del for por el estado deseado = "2"
            estadoActual = estadoActual.dot(matrizT) # se multiplica el estado actual por la matriz con "dot"

        self.txt_resP0.setText(str(estadoActual)) # se manda el estado actual como una cadena de texto al label del p0

        #estadoActual [0] 0.87  [1] 0.0 [2] 0.1 ---> un ejemplo de como se muestra el estado actual en el label

        estadoActual=str(estadoActual).replace('[','').replace(']','') # se eliminan los CORCHETES CUADRATICOS y se remplazan por nada
        estadoActual=str(estadoActual).replace(' ',',').replace(' ',',') # cada espacio es reemplazado por una coma
        self.arduino.write(str(estadoActual).encode()) # se envia a arduino el string, con comas: "0.24,0.87,0.11"

    def accion(self): #funcion de envio de datos de arduino/proteus al listwidget

        while self.arduino.inWaiting(): # este es el modo de recibir datos desde la "terminal de arduino"
            valor = self.arduino.readline().decode() # lectura

            valor = valor.replace("\n", "") # salto de linea
            valor = valor.replace("\r", "") # tambien
            #print(valor)  # ejemplo: "I676R809R512F"

            auxiliar = "" # valor auxiliar string

            if valor[0] == 'I': #arreglo valor en 0
                if valor[len(valor) - 1] == 'F': # len es la cantidad de los datos en el ejemplo anterior

                    # slicing
                    index = valor.find("R") # la busqueda de los datos antes del char R
                    valor1 = valor[1:index]
                    #print("valor1: ", valor1)
                    auxiliar += " Sensor1: " + valor1
                    self.valorSensor1 = float(valor1)

                    valorNuevo = valor[index + 1:]
                    # genera una cadena apartir del contenido que falta procesar
                    # de la cadena original

                    index = valorNuevo.find("R")  # busca la R en la nueva cadena
                    valor2 = valorNuevo[0:index]  # = valorNuevo[:index]

                    auxiliar += " Sensor2: " + valor2
                    self.valorSensor2 = float(valor2)

                    valor3 = valorNuevo[index + 1:len(valorNuevo) - 1]

                    auxiliar += " Sensor3: " + valor3
                    self.valorSensor3 = float(valor3)

            self.datosSensor.addItem(auxiliar)

            self.datosSensor.setCurrentRow(self.datosSensor.count() - 1)

    def conexion(self):
        v = self.btn_conexion.text()
        if v == "CONECTAR":  # pasa de desconectado a conectado
            self.btn_conexion.setText("DESCONECTAR")

            if self.arduino == None:  # SI NO SE HABIA CONECTADO ANTES
                com = "COM" + self.txt_com.text()
                self.arduino = s.Serial(com, baudrate=9600, timeout=1000)  ##realiza la conexion con virtual serial
                # y la iniciliza

                self.txt_estado.setText("INICIALIZADO")

                self.SegundoPlano.start(100)

            elif not self.arduino.isOpen():
                self.arduino.open()
                self.txt_estado.setText("REESTABLECIDO")

                self.SegundoPlano.start(100)

        else:  # pasa de conectado a desconectado
            self.btn_conexion.setText("CONECTAR")

            self.arduino.close()
            self.txt_estado.setText("CERRADO")

            self.SegundoPlano.stop()

    def mensaje(self, msj):
        m = QtWidgets.QMessageBox()
        m.setText(msj)
        m.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
