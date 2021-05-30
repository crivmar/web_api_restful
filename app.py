## IMPORTAR PAQUETES ##

from flask import Flask, render_template, abort, request
import os, json, requests

app= Flask (__name__)
url_base="https://api.themoviedb.org/3/"


## PROGRAMA ##

@app.route('/', methods=["GET"])
def inicio():
    return render_template("index.html")

@app.route('/peliculaspopulares', methods=["GET"])
def populares():
    parametros={"api_key":key,"language":'es-ES',"page":1}
    r=requests.get(url_base+"movie/popular",params=parametros)
    if r.status_code==200:
        documento=r.json()
        for i in documento.get("results"):
            if i.get("title"):
                nombre=i.get("title")
            else
                nombre=i.get("original_title")
            resumen=i.get("overview")
        total=documento.get("total_pages")
    return render_template("pelispopulares.html", nombre=nombe,resumen=resumen,total=total)

key=os.environ["KEY"]
port= os.environ["PORT"]
app.run('0.0.0.0',int(port),debug=False)
