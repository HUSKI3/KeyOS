from flask import render_template, session, request, redirect, url_for, flash
from . import home
import os
import subprocess
from wtforms import Form, StringField, SelectField
import sqlite3
from sqlite3 import Error
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import subprocess
import socket
from socket import *
import requests
import subprocess
import glob
# Packing themes
import packer

from pathlib import Path
import sys
sys.path.append("..")

from merrors import merrors
import conf
from flask import app

Merrors=merrors()
Merrors.error("Test")

# Configs
config = conf.config()
home_path = str(Path.home())
config.read(home_path+"/.keyos/config.json")

##########################################################################
# Themes, for information on creating a theme please refer to the guides.
#
#
#
#
#
##########################################################################

glob_themes = []
current_theme = None

theme_path = config.get("themes")
print(glob.glob(home_path+"/.keyos/"+theme_path+"*"))

for theme in glob.glob(home_path+"/.keyos/"+theme_path+"*"):
    theme_config = conf.config()
    #print(theme)
    theme_config.read(theme+"/config.json")
    print("Loaded theme:",theme_config.get('name'),'at',theme_config.get('location'))
    # Here we build a theme dictionary
    # Check if the theme has a sample image
    if "image" not in theme_config.datajson:
        print("No image found for the theme, is this intended?")
        os.system('''DISPLAY=:0.0 notify-send "KeyOS Debugger" -t 6000 "Warning: {0} has no preview."'''.format(theme_config.get('name')))
    # Check for css
    if "css_loc" not in theme_config.datajson:
        print("No css found for the theme, has the extraction previosly failed?")
        os.system('''DISPLAY=:0.0 notify-send "KeyOS Debugger" -t 6000 "Warning: {0} has no css file for it."'''.format(theme_config.get('name')))
    # [TODO] JS Support, safe?
    glob_themes.append(theme_config)
    if theme_config.get('name') == config.get("current_theme"):
        current_theme = theme_config.datajson

# Theme loading
def load_theme(new_theme=None,new=False):
    if new_theme:
        with open(home_path+"/.keyos/themes/"+new_theme['css_loc'],'r') as f:
            theme_lines = f.readlines()
    with open(home_path+"/.keyos/themes/"+current_theme['css_loc'],'r') as f:
        theme_lines = f.readlines()
    with open('app/static/css/cur_style.css','w+') as f:
        f.writelines(theme_lines)
        print("wrote lines!")

# Sessions
global ses_str
ses_str = {}
ses_str['launch_current'] = {"name":"None","command":"none"}

global debug
debug = True

'''
#Database stuff
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_post(conn, post):
    """
    Create a new post into the posts table
    :param conn:
    :param post:
    :return: post id
    """
    sql = ''INSERT INTO posts(title,contents,imageurl)
              VALUES(?,?,?) ''
    cur = conn.cursor()
    cur.execute(sql, post)
    conn.commit()
    return cur.lastrowid

def select_post(conn,postid):
    """
    Query a post in the posts table
    :param conn: the Connection object
    :param postid: the ID of the post
    :return:
    """
    cur = conn.cursor()
    cur.execute(str("SELECT * FROM posts WHERE id ="+postid))

    post = cur.fetchall()

    return post

def select_all_posts(conn):
    """
    Query a post in the posts table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")

    posts = cur.fetchall()

    return posts
'''

def genapps():
    apps = []
    last = None
    try:
        if ses_str['last']:
            last = ses_str['last']
    except:
        print("No last app")
    for file in glob.glob("/usr/share/applications/*.desktop"):
        with open(file, "r") as f:
            app = {}
            filebits = f.readlines()
            for filebit in filebits:
                if "Name=" in filebit:
                    if "GenericName" in filebit:
                        continue
                    else:
                        app['name'] = filebit.replace("Name=","")
                if "Exec" in filebit:
                    app['command'] = filebit.replace("Exec=","")
        #print(app)
        #input()
        apps.append(app)
    return apps

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    "/usr/share/applications"
    apps = genapps()
    load_theme()
    #print(apps)
    ses_str['apps'] = apps
    return render_template('page/home/index.html', title="Home Page", theme=current_theme, last=ses_str['launch_current'],apps=apps)

@home.route('/settings')
def settings():
    """
    Render the settings template on the /settings route
    """

    return render_template('page/home/general-settings.html', title="General Settings")

@home.route('/transparent')
def transparent():
    """
    Render the settings template on the /settings route
    """
    return render_template('page/home/transparent.html', title="Transparent")


# API
@home.route('/api/launch/piped/')
def launch():
  command = ses_str['launch_current']['command']
  os.system('''DISPLAY=:0.0 notify-send "KeyOS App Launcher" -t 6000 "{} might take a few seconds to start"'''.format(command))
  myip = gethostbyname(gethostname())
  cmd = str("bash switch "+str(command)).split(" ")
  #os.system("bspc desktop --focus ^9 && python3 qtlaunch.py&")
  cmd = subprocess.run(cmd, text=True)
  return str(cmd.returncode)

@home.route('/app/<appname>')
def app(appname):
  #return str(ses_str)
  if appname == "usb_settings":
    ses_str['launch_current']['command'] = home_path+".keyos/open_settings.py"
    r = requests.get('http://localhost:4040/api/launch/piped/')
    if int(r.text) != 0:
        return "Oh no! Something broke!"
    else:
        return redirect('/')
  try:
    if not bool(ses_str['apps']):
      if debug:
          os.system('''DISPLAY=:0.0 notify-send "KeyOS Debugger" -t 6000 "Located {}"'''.format(app))
      ses_str['apps'] = genapps()
  except:
    ses_str['apps'] = genapps()
  cmd = '''DISPLAY=:0.0 notify-send "KeyOS Debugger" -t 6000 "An error occured: Could not locate the app {}"'''.format(appname)
  notif = True
  for app in ses_str['apps']:
    print(app)
    try:
        if appname in app['name']:
            notif = False
            if debug:
                os.system('''DISPLAY=:0.0 notify-send "KeyOS Debugger" -t 6000 "Located {}"'''.format(app))
            cmd = app['command']
            ses_str['launch_current'] = app
    except:
        print("No name?")
  if not notif:
    r = requests.get('http://localhost:4040/api/launch/piped/')
    if int(r.text) != 0:
        return "Oh no! Something broke!"
    else:
        return redirect('/')
  else:
    os.system(cmd)
    return redirect('/')

#applaunching

@home.route('/applaunching/<appname>')
def applaunching(appname):
  return render_template('page/home/applaunching.html')