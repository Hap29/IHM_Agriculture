#!/usr/bin/python3
#coding: utf-8
########################################################
#### ©EmmanuelBOURHIS, 2021, BTS SN IR , LCR, BREST ####
########################################################
import API as datas
from flask import Flask , render_template, request
app = Flask(__name__)                #CREATION DE L'OBJET APPLICATION AVEC LA LIBRAIRIE FLASK APP EST LE NOM DE L'APPLICATION

@app.route('/')                      #URL PAR DEFAUT DE TTN
def index(): 
    r = datas.sqldernier()           #RECUPERATION DU DERNIER ENREGISTREMENT DE LA BDD , GRACE A MA LIBRAIRIE
    heure = datas.tempfixe()         #VARIABLE DE L'HEURE VIA MA LIBRAIRIE
    return render_template("index.html", heure = heure, humiair = r[0] , tempeair = r[1] , tempesol = r[2], humisol= r[3], sol = r[4]) #PAGE WEB AVEC DES VARIABLES POUR LES COMPTEURS


@app.route('/', methods = ['POST'])  #URL PAR DEFAUT, PRET SI REQUETE POST
def resultat(): 
    r = request.form['Reglage_LED']  #JE RECUPERE DE MA PAGE INDEX LA VALEUR DU SLIDER [Reglage_LED]
    datas.reglage(r)                 #JE TRAIRE ET J'ENVOI A L'AIDE DE LA LIBRAIRIE LA DONNEE DE REGLAGE
    return index()                   #JE RETURN SUR LA FONCTION DE LA PAGE PAR DEFAUT


@app.route('/graphiques')            #PAGE POUR L'AFFICHAGE DES GRAPHIQUES
def graphiques():
    r = datas.sqlgraph()             #RECUPERE LES 20 DERNIERES DONNEES DE LA BDD POUR LES GRAPHIQUES 
    return render_template('line_chart.html',humair= r[0], tempair = r[1],  tempsol= r[2], humsol = r[3], enso = r[4], labels = r[5]) #PAGE WEB AVEC LES GRAPHIQUES AVEC DES TABLEAUX DES VALEURS RECUPERES


@app.route('/endpoint', methods = ['POST'])   #URL DE L'ENDPOINT
def endpoint():
    dap = datas.apipoint(request.data)        #ENVOI EN 'BYTE' SI JE TTN ENVOI UNE REQUETE, FONCTION DE LIBRAIRIE TRAITEMENT ET CONVERSION EN JSON
    datas.envoisql(dap[0],dap[1],dap[2],dap[3],dap[4])      #ENVOI DES DONNNEES TRAITEES RECUES DANS MA BDD
    return index()                                          #RETOUR DE L'INDEX PAR DEFAUT


if __name__ == "__main__":

    app.run(host='0.0.0.0' , debug=True)  #mettre ne false cette fonction une fois en ligne, app run = lancement du serveur