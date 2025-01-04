import os
import sys
import json
from flask_socketio import SocketIO
from flask import render_template
import re
import json
import ast

path = os.path.dirname(sys.argv[0])

def getjson():
    try:
        with open(f"{path}\\bot\\data\\thing.txt") as f:
            file = f.read()
            print(file)
            out = ast.literal_eval(file)
        return out
    except:
        return [{"div":"user","name":"Error","content":"there has been an error with the webgui, The feed should return soon"}]

path = os.path.dirname(sys.argv[0])

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    try:
        out = []
        history=getjson()
        for prompt in history:
            print(prompt)
            try:
                if prompt["role"] == "user":
                    name = prompt["content"].split(" says")[0]
                    content = prompt["content"].split(" says")[1]
                    out.append({"div":"user","name":name,"content":content})
                    
                elif prompt["role"] == "assistant":
                    out.append({"div":"assist","name":"AI","content":prompt["content"]})
                if len(out) > 3:
                    out = out[-3:]
            except:
                print("error")
        print(out)
        try:
            outthing = render_template('index.html', history=out)
        except:
            outthing = render_template('index.html', history=[{"div":"user","name":"Error","content":"there has been an error with the webgui, The feed should return soon"}])
           
    except: 
        outthing = render_template('index.html', history=[{"div":"user","name":"Error","content":"there has been an error with the webgui, The feed should return soon"}])
    return outthing
app.run(debug=True,port=8091)