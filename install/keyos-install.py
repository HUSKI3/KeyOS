# This Python file uses the following encoding: utf-8
import sys
import ezconf
import subprocess
import os
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

# Presetup
print("=========================")
cmd = "sudo add-apt-repository ppa:kgilmer/speed-ricer".split(" ")
cmd = subprocess.run(cmd, text=True)
if cmd.returncode != 0:
	print(blue+"[Warn] An error occured while doing pre-setup, but it's not important!"+reset)


print('''==========================
Required deps  : {}
Required tools : {}
=========================='''.format(dep_count,tool_count))

print("Starting UI...")

# Setting up other parts
def setup_others():
	print("You are about to install the themes additional packages")
	# Configs
	os.system("cp -r configs/* ~/.config/")
	# git clone --depth=1 https://github.com/adi1090x/rofi.git
	cmd = "git clone --depth=1 https://github.com/adi1090x/rofi.git && cd rofi && chmod +x setup.sh && bash setup.sh".split(" ")
	cmd = subprocess.run(cmd, text=True)
	if cmd.returncode != 0:
		print(red+"[Error] An error occured while installing the rofi theme! Quitting"+reset)
		quit()
	# Touchegg
	cmd = "sudo add-apt-repository ppa:touchegg/stable".split(" ")
	cmd = subprocess.run(cmd, text=True)
	if cmd.returncode != 0:
		print(red+"[Warn] An error occured while adding the touchegg repo, but it's not important!"+reset)
	# uhubctl
	cmd = "git clone https://github.com/mvp/uhubctl".split(" ")
	cmd = subprocess.run(cmd, text=True)
	if cmd.returncode != 0:
		print(red+"[Error] An error occured while cloning uhubctl!"+reset)
	os.system("cd uhubctl && make")
	print("Finished!")

# Installation

def install(app):
	command = "sudo apt install {} -y".format(app).split(" ")
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
				setup_others()
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

THE INSTALLER WILL FREEZE DURING THE INSTALL, DO NOT CLOSE THE INSTALLER
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
