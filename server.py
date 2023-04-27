import socket
from flask import request,redirect,Flask,render_template

app = Flask(__name__)

@app.route("/",methods = ["POST"])
def index_it():
    return open("login.html","rb").read()
@app.errorhandler(404)
def err(e):
    return open("login.html","rb").read()
ip_addr = socket.gethostbyname(socket.gethostname())
try:
    app.run(ip_addr,80)
except:
    app.run(ip_addr,8000)