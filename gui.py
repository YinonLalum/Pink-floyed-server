import socket
import datetime
import data
import sys
from re import findall
from time import sleep
from PyQt5.uic import loadUi
from PyQt5 import QtGui
from PyQt5 import QtCore 
from PyQt5 import QtWidgets 

PARAM_TYPES = {'2': 'name of the album', '3': 'name of the song', '4': 'name of the song', '5': 'name of the song', '6': 'word that appears in songs', '7': "word that appears in song's name"}
#SERVER_IP = "10.100.102.16"
SERVER_IP = "127.0.0.1"
SERVER_PORT = 49060
choice = 0
socket = None
auth = False
param = ''

app = QtWidgets.QApplication(sys.argv)
widget = loadUi('main menu.ui')

def main():

	widget.show()
	
	widget.pushButton_3.clicked.connect(attempt_login)
	widget.pushButton.clicked.connect(choose_option)
	widget.pushButton_2.clicked.connect(get_param)
	widget.pushButton_4.clicked.connect(send_and_get_resp)
	widget.pushButton_6.clicked.connect(end)
	
	sys.exit(app.exec_())

def send_and_get_resp():
	answer_window = loadUi("answer.ui")
	answer_window.show()
	socket.sendall((str(choice)+"#"+param).encode())
	server_msg = socket.recv(2048).decode()
	answer_window.textBrowser.clear()
	answer_window.textBrowser.insertPlainText(server_msg)
	answer_window.buttonBox.accepted.connect(lambda: answer_window.accept())
	
def end():
	try:
		socket.sendall("10".encode())
		socket.close()
	except:
		pass
	widget.close()
	
def get_param():
	param_window = loadUi("param.ui")
	param_window.show()
	param_window.accepted.connect(lambda: assign(param_window))
	widget.pushButton_4.setEnabled(True)
	widget.pushButton_2.setEnabled(False)

def assign(param_window):
	global param
	param = param_window.lineEdit.text()
	
def attempt_login():
	global socket
	while True:
		if not socket:
			try:
				socket = data.establish_connection(SERVER_IP,SERVER_PORT)
				update_connection()
			except:
				continue
		break
	
	loginScreen = loadUi("login.ui")
	loginScreen.show()
	
	loginScreen.buttonBox.accepted.connect(lambda: send_login(loginScreen))
	loginScreen.buttonBox.accepted.connect(update_connection)
	
def send_login(loginScreen):
	global auth
	name = loginScreen.lineEdit_2.text()
	pas = loginScreen.lineEdit.text()
	socket.sendall((name+'#'+pas).encode())
	server_msg = socket.recv(1024).decode()
	if server_msg == "TRUE":
		auth = True
	loginScreen.accept()
	
def update_param_button():
	if choice == 1 or choice == 8 or choice == 9:
		widget.pushButton_2.setEnabled(False)
		widget.pushButton_2.setText("select an option with a param slot!")
		widget.pushButton_4.setEnabled(True)
	else:
		widget.pushButton_4.setEnabled(False)
		widget.pushButton_2.setEnabled(True)
		widget.pushButton_2.setText("Enter param")

		
def update_connection():
	if socket:
		if auth:
			widget.label_2.setText("Authorized")
			widget.pushButton_3.setEnabled(False)
			widget.pushButton_3.setText("Allready logged in!")
			widget.pushButton.setEnabled(True)
		else:
			widget.label_2.setText("Connected")
	else:
		widget.label_2.setText("Not connected")

def choose_option():
	options = loadUi("choose option.ui")
	options.show()
	options.buttonBox.accepted.connect(lambda: set_choice(options))
	options.buttonBox.rejected.connect(lambda: options.reject())
	
def set_choice(options):
	global choice
	global param
	param = ''
	n = options.buttonGroup.checkedButton().objectName()
	choice = int(findall("_(.+)",n)[0]) - 18
	update_param_button()
	options.accept()
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main()
