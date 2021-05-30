## IMPORTAR PAQUETES ##

from flask import Flask, render_template, abort, requests
import os, json

app= Flask (__name__)


## PROGRAMA ##

@app.route('/', methods=["GET"])
def inicio():
    return render_template("index.html")





port= os.environ["PORT"]
app.run('0.0.0.0',int(port),debug=False)
