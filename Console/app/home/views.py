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

import sys
sys.path.append("..")
from merrors import merrors
import conf
from flask import app




configs=conf.config()
configs.read()
name = configs.get("name")
print(name)
Merrors=merrors()
Merrors.error("Test")


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
    sql = ''' INSERT INTO posts(title,contents,imageurl)
              VALUES(?,?,?) '''
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

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """

    return render_template('page/home/index.html', title="Home Page")

@home.route('/settings')
def settings():
    """
    Render the settings template on the /settings route
    """

    return render_template('page/home/general-settings.html', title="General Settings")

# API
@home.route('/api/launch/piped/<command>')
def launch(command):
  os.system('''DISPLAY=:0.0 notify-send "KeyOS App Launcher" -t 6000 "{} might take a few seconds to start"'''.format(command))
  myip = gethostbyname(gethostname())
  cmd = str("bash switch "+str(command)).split(" ")
  #os.system("bspc desktop --focus ^9 && python3 qtlaunch.py&")
  cmd = subprocess.run(cmd, text=True)
  return str(cmd.returncode)

@home.route('/app/<appname>')
def app(appname):
  r = requests.get('http://localhost:4040/api/launch/piped/'+appname)
  if int(r.text) != 0:
    return "Oh no! Something broke!"
  else:
    return redirect('/')

#applaunching

@home.route('/applaunching/<appname>')
def applaunching(appname):
  return render_template('page/home/applaunching.html')