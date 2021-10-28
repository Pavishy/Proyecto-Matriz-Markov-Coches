##uso de modulo pyserial
import serial as s
###################################

import sys

from PyQt5 import uic, QtWidgets, QtCore

qtCreatorFile = "ControlArduino_HalfDuplex-Markov.ui"  # Nombre del archivo

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.arduino = None

        self.btn_conexion.clicked.connect(self.conexion)

        self.SegundoPlano = QtCore.QTimer()
        self.SegundoPlano.timeout.connect(self.accion)

        self.btn_control.clicked.connect(self.control)

        self.valorSensor1 = -1
        self.valorSensor2 = -1
        self.valorSensor3 = -1

        self.btn_control.setText("ENVIAR ACCIÓN")

    def control(self):
        # OPERACION CON LOS VALORES DE LOS SENSORES PARA REALIZAR LA APLICACIÓN DE ALGUN PROCESO
        self.valorSensor1 /= 100
        self.valorSensor2 /= 100
        self.valorSensor3 /= 100
        print("v1: ", self.valorSensor1)
        print("v2: ", self.valorSensor2)
        print("v3: ", self.valorSensor3)

        # Aplicar cadenas de markov
        # respuesta = ....

        # supongamos ....
        if self.valorSensor1 + self.valorSensor2 + self.valorSensor3 > 1.5:
            self.arduino.write("1".encode())
        else:
            self.arduino.write("0".encode())

    def accion(self):

        while self.arduino.inWaiting():
            valor = self.arduino.readline().decode()

            valor = valor.replace("\n", "")
            valor = valor.replace("\r", "")
            print(valor)  # ejemplo: "I676R809R512F"

            auxiliar = ""

            if valor[0] == 'I':
                if valor[len(valor) - 1] == 'F':
                    print("La cadena esta completa")

                    # slicing
                    index = valor.find("R")
                    valor1 = valor[1:index]
                    print("valor1: ", valor1)
                    auxiliar += " Sensor1: " + valor1
                    self.valorSensor1 = int(valor1)

                    valorNuevo = valor[index + 1:]  # genera una cadena apartir del contenido que falta procesar
                    # de la cadena original
                    print("valor nuevo: ", valorNuevo)
                    index = valorNuevo.find("R")  # busca la R en la nueva cadena
                    valor2 = valorNuevo[0:index]  # = valorNuevo[:index]
                    print("valor2:", valor2)
                    auxiliar += " Sensor2: " + valor2
                    self.valorSensor2 = int(valor2)

                    valor3 = valorNuevo[index + 1:len(valorNuevo) - 1]
                    print("valor3:", valor3)
                    auxiliar += " Sensor3: " + valor3
                    self.valorSensor3 = int(valor3)

            #####################################

            self.datosSensor.addItem(auxiliar)

            self.datosSensor.setCurrentRow(self.datosSensor.count() - 1)

        ########################################################

    def conexion(self):
        v = self.btn_conexion.text()
        if v == "CONECTAR":  # pasa de desconectado a conectado
            self.btn_conexion.setText("DESCONECTAR")

            if self.arduino == None:  # SI NO SE HABIA CONECTADO ANTES
                com = "COM" + self.txt_com.text()
                self.arduino = s.Serial(com, baudrate=9600, timeout=1000)  ##realiza la conexion
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

    # Tarea X Operaciones con Strings (Cadenas de Caracteres) en Python
    # Tarea X+1 Operaciones con Strings (Cadenas de Caracteres) en Arduino

    # Tarea (Programa) X+2 Modificar la interfaz gráfica de usuario a conveniencia del equipo

    # valor1 + valor 2 + valor 3
