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
    page=1
    parametros={"api_key":key,"language":'es-ES',"page":page}
    r=requests.get(url_base+"movie/popular",params=parametros)
    listado=[]
    if r.status_code==200:
        documento=r.json()
        for i in documento.get("results"):
            diccionario={}
            if i.get("title"):
                diccionario["nombre"]=i.get("title")
            else:
                diccionario["nombre"]=i.get("original_title")
            diccionario["id"]=i.get("id")
            listado.append(diccionario)
        page=documento.get("page")+1
        total=documento.get("total_pages")
    return render_template("pelispopulares.html",listado=listado,page=page)

@app.route('/peliculaspopulares/<int:page>', methods=["GET"])
def siguiente(page):
    page=page
    parametros={"api_key":key,"language":'es-ES',"page":page}
    r=requests.get(url_base+"movie/popular",params=parametros)
    listado=[]
    if r.status_code==200:
        documento=r.json()
        for i in documento.get("results"):
            diccionario={}
            if i.get("title"):
                diccionario["nombre"]=i.get("title")
            else:
                diccionario["nombre"]=i.get("original_title")
            diccionario["id"]=i.get("id")
            listado.append(diccionario)
        total=documento.get("total_pages")
        if page < total:
            page=page+1
    return render_template("pelispopulares.html",listado=listado,page=page)


key=os.environ["KEY"]
port= os.environ["PORT"]
app.run('0.0.0.0',int(port),debug=False)
