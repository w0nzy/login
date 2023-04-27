import os
import json
from flask import Flask, render_template, redirect, url_for, request

class IO:
    def __init__(self,file = None):
        self.file = file
    def read(self):
        return open(self.file,"r").read()
    def write(self,data):
        mode = "w"
        if isinstance(data,bytes):
            mode = "wb"
        fd = open(self.file,mode)
        fd.write(data)
        fd.close()
    def append(self,data: str or bytes):
        mode = "a+"
        if isinstance(data,bytes):
            mode = "ab+"
        fd = open(self.file,mode)
        fd.write(data)
        fd.close()
    def erase(self):
        s = open(self.file,"w")
        s.close()
class Database:
    def __init__(self):
        self.fd = IO("database.json")
    def add(self,key=None,value = None) -> bool:
        try:
            s = json.loads(self.fd.read())
            s["usernames"][key]=value
            out = json.dumps(s,indent=8)
            self.fd.write(out)
        except Exception as e:
            return False
        return True
    def get(self,key):
        ret = json.loads(self.fd.read())
        if isinstance(ret,dict):
            if not ret.get("usernames") is None:
                return ret["usernames"].get(key)
        return None
    def close(self):
        self.fd.close()
    def read(self):
        return self.fd.read()
app = Flask(__name__)
db = Database()
@app.errorhandler(404)
def handle_404_page(fault):
    return redirect("/login")
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        peer_usrname = request.form["username"]
        if not db.get(peer_usrname) is None:
            peer_pwd = request.form["pwd"]
            local_pwd = db.get(peer_usrname)
            if local_pwd != peer_pwd:
                error = "Yanlış Şifre tekrar deneyin"
            else:
                return redirect("/")
        else:
            error = "Böyle bir kullanıcı yok"
    return render_template('login.html', error=error)
@app.route("/register",methods = ["GET","POST"])
def register():
    err = "Zaten Kayıtlısınız !!"
    if request.method == "POST":
        peer_usrname = request.form["username"]
        peer_pwd = request.form["pwd"]
        if db.get(peer_usrname) is None:
            if peer_usrname == "" or peer_usrname is None:
                err = "Kullanıcı adı boş bırakılamaz"
            elif peer_usrname == "" or peer_usrname is None:
                err = "Şifre boş bırakılamaz"
            else:
                if db.add(peer_usrname,peer_pwd):
                    err = "Kayıt Başarılı"
                else:
                    err = "Kayıt yapılamadı Yetkili birimlere bildirildi"
    return render_template("register.html",error=err)
if __name__ == "__main__":
    app.run("192.168.1.124",80)