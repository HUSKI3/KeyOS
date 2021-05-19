# This Python file uses the following encoding: utf-8
import sys
import ezconf
import subprocess
import os

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


# Setting up other parts
def setup_others():
	print("You are about to install the themes additional packages")
	# Configs & other parts
	os.system("cp -r configs/* ~/.config/")
	os.system("mkdir ~/.keyos")
	os.system("cp -r Console/ ~/.keyos/")
	os.system("cp -r keyos/* ~/.keyos/")
	# git clone --depth=1 https://github.com/adi1090x/rofi.git
	cmd = "git clone --depth=1 https://github.com/adi1090x/rofi.git && cd rofi && chmod +x setup.sh && bash setup.sh".split(" ")
	cmd = subprocess.run(cmd, text=True)
	if cmd.returncode != 0:
		print(red+"[Warn] An error occured while installing the rofi theme! But it is not required by the system"+reset)
	# Touchegg
	cmd = "sudo add-apt-repository ppa:touchegg/stable".split(" ")
	cmd = subprocess.run(cmd, text=True)
	if cmd.returncode != 0:
		print(red+"[Warn] An error occured while adding the touchegg repo, but it's not important!"+reset)
	# uhubctl
	#cmd = "git clone https://github.com/mvp/uhubctl".split(" ")
	#cmd = subprocess.run(cmd, text=True)
	#if cmd.returncode != 0:
	#	print(red+"[Error] An error occured while cloning uhubctl!"+reset)
	#os.system("cd uhubctl && make")
	print("Finished!")

# Installation

def install(app):
	command = "sudo apt install {} -y".format(app).split(" ")
	cmd = subprocess.run(command, text=True)


print('''Welcome to the KeyOS alpha, before you proceed please read the following:
This is a development build, if things go wrong they make break your system.
You are about to install {} packages and {} tool/s
Packages: {}
Tools: {}
'''.format(dep_count,tool_count, deps, tools))

input("Press enter to continue...")
# Open progress bar
# install(stuff)
for dep in deps:
	install(dep)
for tool in tools:
	install(tool)
setup_others()
