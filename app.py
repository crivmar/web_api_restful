## IMPORTAR PAQUETES ##

from flask import Flask, render_template, abort, request
import os, json, requests


app= Flask (__name__)
url_base="https://api.themoviedb.org/3/"


## PROGRAMA ##

## INDEX ##

@app.route('/', methods=["GET"])
def inicio():
    return render_template("index.html")

## CINE POPULAR ##

@app.route('/peliculaspopulares', methods=["GET"])
@app.route('/peliculaspopulares/<int:page>', methods=["GET"])
def populares(page=1):
  
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
        page=documento.get("page")
        total=documento.get("total_pages")
        anterior=0
        if page>1:
           anterior=page-1
        if page < total:
            page=page+1
        return render_template("pelispopulares.html",listado=listado,page=page,anterior=anterior,total=total)
    else:
        abort(404)

## SERIES POPULARES ##

@app.route('/seriespopulares', methods=["GET"])
@app.route('/seriespopulares/<int:page>', methods=["GET"])
def popular(page=1):

    parametros={"api_key":key,"language":'es-ES',"page":page}
    r=requests.get(url_base+"tv/popular",params=parametros)
    listado=[]
    if r.status_code==200:
        documento=r.json()
        for i in documento.get("results"):
            diccionario={}
            if i.get("name"):
                diccionario["nombre"]=i.get("name")
            else:
                diccionario["nombre"]=i.get("original_name")
            diccionario["id"]=i.get("id")
            listado.append(diccionario)
        page=documento.get("page")
        total=documento.get("total_pages")
        anterior=0
        if page>1:
           anterior=page-1
        if page < total:
            page=page+1
        return render_template("seriespopulares.html",listado=listado,page=page,anterior=anterior,total=total)
    else:
        abort(404)

## DETALLES ##

@app.route('/peliculas/<id>', methods=["GET"])
def detalle(id):
    parametros={"api_key":key,"language":'es-ES', "id":id}
    r=requests.get(url_base+"movie/%s"%id,params=parametros)
    if r.status_code==200:
        documento=r.json()
        titulo=documento.get("title")
        imagen=documento.get("poster_path")
        resumen=documento.get("overview")
        popularidad=documento.get("popularity")
        fecha=documento.get("release_date")
        f=fecha[8:10]+"-"+fecha[5:7]+"-"+fecha[0:4]
        return render_template("detallep.html",titulo=titulo,imagen=imagen,resumen=resumen,popularidad=popularidad,f=f)
    else:
        abort(404)

@app.route('/series/<id>', methods=["GET"])
def detallese(id):
    parametros={"api_key":key,"language":'es-ES', "id":id}
    r=requests.get(url_base+"tv/%s"%id,params=parametros)
    if r.status_code==200:
        documento=r.json()
        pro=False
        titulo=documento.get('name')
        imagen=documento.get("poster_path")
        resumen=documento.get("overview")
        popularidad=documento.get("popularity")
        fecha=documento.get('first_air_date')
        f=fecha[8:10]+"-"+fecha[5:7]+"-"+fecha[0:4]
        temporadas=documento.get('number_of_seasons')
        episodios=documento.get('number_of_episodes')
        compse=1
        if documento.get('in_production')== True:
            pro=True
        return render_template("detallep.html",titulo=titulo,imagen=imagen,resumen=resumen,popularidad=popularidad,f=f,temporadas=temporadas,episodios=episodios,compse=compse,pro=pro)
    else:
        abort(404)

## BUSCADOR ##

@app.route('/lista', methods=["POST"])
@app.route('/lista/<tipo>/<int:page>', methods=["GET"])
def lista(page=1):
    
    cadena= request.form.get("cadena")
    tipo=request.form.get("tipo")
    listado=[]
    if tipo=="Películas":
        parametros={"api_key":key,"language":'es-ES',"query":cadena,"page":page}
        r=requests.get(url_base+"search/movie",params=parametros)
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
                page=documento.get("page")
                total=documento.get("total_pages")
            anterior=0
            if page>1:
                anterior=page-1
            if page < total:
                page=page+1
            tipo="Películas"
            return render_template("lista.html", listado=listado,page=page,anterior=anterior,total=total,tipo=tipo, cadena=cadena)
        else:
            abort(404)
    else:
        parametros={"api_key":key,"language":'es-ES',"query":cadena,"page":page}
        r=requests.get(url_base+"search/tv",params=parametros)
        if r.status_code==200:
            documento=r.json()
            for i in documento.get("results"):
                diccionario={}
                if i.get("name"):
                    diccionario["nombre"]=i.get("name")
                else:
                    diccionario["nombre"]=i.get("original_name")
                diccionario["id"]=i.get("id")
                listado.append(diccionario)
                page=documento.get("page")
                total=documento.get("total_pages")
            anterior=0
            s= True
            if page>1:
                anterior=page-1
            if page < total:
                page=page+1
            tipo="Películas"
            return render_template("lista.html", listado=listado,page=page,anterior=anterior,total=total,tipo=tipo,s=s,cadena=cadena)
        else:
            abort(404)

key=os.environ["KEY"]
port= os.environ["PORT"]
app.run('0.0.0.0',int(port),debug=False)
