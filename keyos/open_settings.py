from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import uic
import sys
import ezconf
from pathlib import Path
import glob
import re
import subprocess
from subprocess import call
import os

device_re = re.compile(b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
df = subprocess.check_output("lsusb")

config = ezconf.config()
home_path = str(Path.home())
config.read(home_path+"/.keyos/config.json")

def get_devices():
	devices = []
	#for i in df.split(b'\n'):
	#	if i:
	#		info = device_re.match(i)
	#		if info:
	#			dinfo = info.groupdict()
	#			dinfo['device'] = '/dev/bus/usb/%s/%s' % (dinfo.pop('bus'), dinfo.pop('device'))
	#			devices.append(dinfo)
	# ls /sys/bus/usb/devices/*/product
	for elem in glob.glob("/sys/bus/usb/devices/*/product"):
		with open(elem, "r") as f:
			name = f.readline()
		device = {
			"location":elem.split("/")[5],
			"name":name
		}
		devices.append(device)
	return devices

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		# Qt5 Base
		super(MainWindow,self).__init__(*args, **kwargs)
		uic.loadUi(home_path+'/.keyos/settings.ui', self)
		self.setWindowTitle("Configure Key OS")

		# Config
		## Base
		print(config.pretty())
		user_name = config.get('user')
		curr_theme = config.get('current_theme')
		theme_path = config.get('themes')
		themes = glob.glob(home_path+"/.keyos/"+theme_path+"*")

		## Settings
		settings = config.get('settings')

		# General Page
		## Nothing here yet

		# Appearence Page
		## Display themes in listView
		self.themeList = self.findChild(QtWidgets.QListView, 'listView_2')
		self.model_theme = QtGui.QStandardItemModel()
		self.themeList.setModel(self.model_theme)
		for elem in themes:
			item = QtGui.QStandardItem(elem)
			item.setCheckable(True)
			if elem == curr_theme:
				item.setCheckState(QtCore.Qt.Checked)
			self.model_theme.appendRow(item)

		# Usb Page
		## Display themes in listView
		self.themeList = self.findChild(QtWidgets.QListView, 'listView')
		self.model_usb = QtGui.QStandardItemModel()
		self.themeList.setModel(self.model_usb)
		global devices_l
		devices_l = get_devices()
		for elem in devices_l:
			print(elem)
			name = elem['name']
			dev_loc_id = elem['location']
			item = QtGui.QStandardItem(name)
			item.setCheckable(True)
			if os.path.exists("/sys/bus/usb/devices/{0}/driver".format(dev_loc_id)):
				item.setCheckState(QtCore.Qt.Checked)
			self.model_usb.appendRow(item)
		
		# Buttons
		## Accept button
		self.AcceptButton = self.findChild(QtWidgets.QPushButton, 'pushButton')
		self.AcceptButton.clicked.connect(self.accept)

		## Exit button
		self.AcceptButton = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
		self.AcceptButton.clicked.connect(self.exit)
		self.show()

	def accept(self):
		print("accepted")
		for index in range(self.model_theme.rowCount()):
			item = self.model_theme.item(index)
			if item.checkState() == QtCore.Qt.Checked:
				# Set theme to the last checked element (if user checks more than one)
				# print(item.text(),"is checked")
				config.update('current_theme',item.text())
		print(config.pretty())

		for index in range(self.model_usb.rowCount()):
			item = self.model_usb.item(index)
			if item.checkState() == QtCore.Qt.Checked:
				name = item.text()
				for device in devices_l:
					if device['name'] == name:
						dev_loc_id = device['location']
				if not os.path.exists("/sys/bus/usb/devices/{0}/driver".format(dev_loc_id)):
					check = self.enable_usb_device(dev_loc_id)
					if check:
						os.system('''DISPLAY=:0.0 notify-send "KeyOS Debugger" -t 6000 "Enabled device: {}"'''.format(name))
					else:
						os.system('''DISPLAY=:0.0 notify-send "KeyOS Debugger" -t 6000 "Failed to enable device: {}"'''.format(name))
				

		self.close()

	def exit(self):
		print("Exiting")
		self.close()

	def disable_usb_device(self,usb_node):
		subprocess.run("echo \'{0}\' | sudo tee /sys/bus/usb/drivers/usb/unbind".format(usb_node).split(" "))

	def enable_usb_device(self,usb_node):
		subprocess.call("echo \'{0}\' | sudo tee /sys/bus/usb/drivers/usb/bind".format(usb_node).split(" ")) 
		if os.path.exists("/sys/bus/usb/devices/{0}/driver".format(usb_node)):
			return True
		else:
			os.system("ls -l /sys/bus/usb/devices/{0}/driver".format(usb_node))
			return False

app = QApplication(sys.argv)
window = MainWindow()

app.exec_()
