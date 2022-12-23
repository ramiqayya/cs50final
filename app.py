import os
from flask import Flask, redirect,render_template,url_for,request,session
from flask_session import Session
from cs50 import Session

app=Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"]=True

