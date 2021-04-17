# This Python file uses the following encoding: utf-8
import sys
import ezconf
import subprocess
from PyQt5 import QtWidgets, uic

# Colours + elems
reset = "\u001b[0m"
red = "\u001b[31m"
green = "\u001b[32m"
blue = "\u001b[34m"
dot = "•"
tick = "✓"
cross = "✖"

# Configuration
config = ezconf.config()
try:
	config.read("config.pak")
	print(green+tick+" Loaded configuration, preparing package list and etc..."+reset)
except IOError:
	print(red+cross+" Configuration file not accessible, contact support."+reset)
deps = config.get("packages")
dep_count = len(config.get("packages"))
tools = config.get("tools")
tool_count =  len(config.get("tools"))

print('''==========================
Required deps  : {}
Required tools : {}
=========================='''.format(dep_count,tool_count))

print("Starting UI...")

# Installation

def install(app):
	command = "sudo apt install {}".format(app).split(" ")
	cmd = subprocess.run(command, text=True)

# UI
class win(QtWidgets.QMainWindow):
	def __init__(self):
		super(win, self).__init__()
		uic.loadUi('main.ui', self)
		self.setWindowTitle("KeyOS")
		self.show()
		# Podge#0930
		self.button = self.findChild(QtWidgets.QPushButton, 'b1')
		self.button.clicked.connect(self.ContinueButtonPressed)
	def ContinueButtonPressed(self):
		# This is executed when the button is pressed
		print('printButtonPressed')
		dialog = DialogUi()
		dialog.exec_()
		try:
			if proceeded:
				# Open progress bar
				# install(stuff)
				for dep in deps:
					install(dep)
				for tool in tools:
					install(tool)
				self.close()
		except Exception as e:
			print(e)
			quit()

class DialogUi(QtWidgets.QDialog):
	def __init__(self):
		super(DialogUi, self).__init__()
		uic.loadUi('dialog.ui', self)
		self.setWindowTitle("KeyOS | Proceed")
		self.edit = self.findChild(QtWidgets.QPlainTextEdit, 'plainTextEdit')
		self.edit.setReadOnly(True)
		self.edit.setPlainText('''Welcome to the KeyOS alpha, before you proceed please read the following:
This is a development build, if things go wrong they make break your system.
You are about to install {} packages and {} tool/s
Packages: {}
Tools: {}
'''.format(dep_count,tool_count, deps, tools))
		self.button = self.findChild(QtWidgets.QPushButton, 'accept')
		self.button.clicked.connect(self.acceptButtonPressed)
		self.button2 = self.findChild(QtWidgets.QPushButton, 'cancel')
		self.button2.clicked.connect(self.cancelButtonPressed)
		self.show()

	def acceptButtonPressed(self):
		global proceeded
		proceeded = True
		self.close()

	def cancelButtonPressed(self):
		self.close()
		quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = win()
    app.exec_()
