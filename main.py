#!/usr/bin/python3
#coding: utf-8
########################################################
#### ©EmmanuelBOURHIS, 2021, BTS SN IR , LCR, BREST ####
######################################################## 
from API import datas, erreur, identification
from m_auto import modeauto
from multiprocessing import Process
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
import sys
####
####INIT
app = Flask(__name__)                #CREATION DE L'OBJET APPLICATION AVEC LA LIBRAIRIE FLASK APP EST LE NOM DE L'APPLICATION
#app.secret_key = os.urandom(12)
#app.secret_key = b'CLEFDESESSION'
app.config['SECRET_KEY'] =  b'_XXXXXXXXXXXXXXXXXXXXXXX'
app.config['PERMANENT_SESSION_LIFETIME'] = 600 # la session dure x secondes( 10 mn ici)
app.config['SESSION_COOKIE_NAME'] = "SESSION_UTILISATEUR" 
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = True
#####
#####PARTIE URLs ACTIVES
@app.route('/')                      #URL PAR DEFAUT DE TTN
def index():
    if not session.get('utilisateur_ok'):
        return render_template('login.html') 
    else:
        r = datas.sqldernier()           #RECUPERATION DU DERNIER ENREGISTREMENT DE LA BDD , GRACE A MA LIBRAIRIE
        heure = datas.tempfixe()         #VARIABLE DE L'HEURE VIA MA LIBRAIRIE
        return render_template("index.html", heure = heure, humiair = r[0] , tempeair = r[1] , tempesol = r[2], humisol= r[3], sol = r[4]) #PAGE WEB AVEC DES VARIABLES POUR LES COMPTEURS

@app.route("/logout")
def logout():
    session['utilisateur_ok'] = False
    if not session.get('admin_log'):
        session['admin_log'] = False
    else:
        session['admin_log'] = False
    return redirect(url_for('index'))

@app.route('/graphiques')            #PAGE POUR L'AFFICHAGE DES GRAPHIQUES
def graphiques():
    if not session.get('utilisateur_ok'):
        return render_template('login.html') 
    else:
        r = datas.sqlgraph()             #RECUPERE LES 20 DERNIERES DONNEES DE LA BDD POUR LES GRAPHIQUES 
        return render_template('line_chart.html',humair= r[0], tempair = r[1],  tempsol= r[2], humsol = r[3], enso = r[4], labels = r[5]) #PAGE WEB AVEC LES GRAPHIQUES AVEC DES TABLEAUX DES VALEURS RECUPERES

@app.route('/commande<string:id>')            #PAGE POUR L'AFFICHAGE DES COMMANDES LEDS
def commandep(id):
    if not session.get('utilisateur_ok'):
        return render_template('login.html') 
    else:    
        id =  identification.idnombre(id) #pour envoyer dans une futur dfocntiion à l'affichage de l'historique de réglage
        vals = datas.visuvallreglage(id)
        page = "commande"+identification.idlettre(id)+".html"
        return render_template( page, vals = vals, typec = datas.sqlvisucommande , aff = datas.visuvallreglage)
        
@app.route('/pageadmin')
def admin():
    if not session.get('admin_log'):
        return render_template('loginadmin.html')
    else:
        vals = datas.bddlogin()
        return render_template('pageadmin.html',vals = vals[2])
####
####PARTIE URLs CACHEES / FONCTIONS
@app.route('/login', methods=['POST'])
def login():   #Ecrire une fonction pour vérifier la reception de la table dans ma classe
    user  = request.form['username']
    passw = request.form['password']
    ret = datas.bddlogin(user,passw)
    if ret[0] == True:
        session['utilisateur_ok'] = True
        return redirect(url_for('index'))
    else:
        #print('Mauvais mot de passe')
        if 'visits' in session:
            session['visits'] = session.get('visits') + 1 
            if (session['visits'] == 3):  
                datas.bddatt(user,passw)
                session['visits'] =   0   # ou pour supp session.pop('visits', None)
        else:
            session['visits'] = 1  # 1 car deja premier passage ici a la creation de cette session
        return redirect(url_for('index'))

@app.route('/commandes', methods = ['POST']) 
def pcommandes(): 
    r = request.form['Reglage_LED']  
    c = request.form['Chauffage']
    a = request.form['Arrosoir']
    envoi = identification.id(r,c,a)
    datas.reglage(envoi[0], envoi[1])
    return datas.entreglageval(envoi[0],envoi[1], 1)    #retour de la fonction de la lib

@app.route('/commandes<int:id>', methods = ['POST'])
def mode(id):
    return datas.changement_etat(id)

@app.route('/nombaff<int:id>/<string:nb>')
def aff(id,nb):
    return datas.changement_aff(id,nb)

@app.route('/regmode<string:id>')
def regmode(id):
    dn = datas.pageregmode()
    chaine = "regmode"+id+".html"
    return render_template(chaine, dn = dn[0], lreg = dn[1])

@app.route('/autochnt<int:id>/<string:fonc>', methods = ['POST']) 
def test(id,fonc):
    redir = "regmode"+identification.idlettre(id)
    rec = request.form.to_dict()
    if(fonc == "s"):
        datas.entreeseuils(id,rec)
        return redirect("/"+redir)
    elif(fonc == "c"):
        datas.entreeconditions(id,rec)
        return redirect("/"+redir)
     
@app.route('/endpoint', methods = ['POST'])  
def endpoint():
    dap = datas.apipoint(request.data)        #ENVOI EN 'BYTE' SI JE TTN ENVOI UNE REQUETE, FONCTION DE LIBRAIRIE TRAITEMENT ET CONVERSION EN JSON
    datas.envoisql(dap[0],dap[1],dap[2],dap[3],dap[4])      #ENVOI DES DONNNEES TRAITEES RECUES DANS MA BDD
    return index()                                     #RETOUR DE L'INDEX PAR DEFAUT

@app.route('/loginadmin', methods=['POST'])
def logina():   #Ecrire une fonction pour vérifier la reception de la table dans ma classe
    user  = request.form['username']
    passw = request.form['password']
    ret = datas.bddlogin(user,passw)
    if (ret[0] == True and ret[1] == True):
        session['admin_log'] = True
        return redirect(url_for('admin'))
    else:
        #print('Mauvais mot de passe')
        if 'visits' in session:
            session['visits'] = session.get('visits') + 1 
            if (session['visits'] == 3):  
                datas.bddatt(user,passw)
                session['visits'] =   0   # ou pour supp session.pop('visits', None)
        else:
            session['visits'] = 1  # 1 car deja premier passage ici a la creation de cette session
        return redirect(url_for('admin'))

@app.route('/pageadmin<int:fonct>', methods=['POST'])
def adminp(fonct):
    if fonct == 0:
        nvuser = request.form['adduser']
        aspass = request.form['addpass']
        priv   = request.form['priv']
        verif  = datas.bddlogin(nvuser)
        if verif[4] == False:
            if nvuser == "" or nvuser == " " or aspass == "" or aspass == " ":
                return render_template('pageadmin.html', entree = 'echar', nvuser =nvuser)
            else:
                val = datas.adduser(nvuser,aspass,priv)
                return render_template('pageadmin.html', entree = False ,nvuser =nvuser, aspass=aspass, priv = priv )
        else :
            return render_template('pageadmin.html', entree = True, nvuser =nvuser)

    elif fonct == 1:
        aff = request.form['maRecherche']
        val    = datas.bddlogin(aff)
        return render_template('pageadmin.html',ok = val[4] ,aff= aff ,loginc = val[3])   #val[3] c'est le login code, val[4] c'est la verif 

    elif fonct == 2:
        datas.suppuser(request.form['loginc'])
        return redirect(url_for('admin'))

    elif fonct == 3:
        datas.upmdp(request.form['loginc'],request.form['uppass'])
        return redirect(url_for('admin'))

@app.errorhandler(500)
def page_not_found0(e):
    return render_template('erreur.html'),500

@app.errorhandler(405)    #ERREUR 405 = ERREUR METHOD NOT ALLOWED
def page_not_found1(e):
    return redirect("/")

@app.errorhandler(404)
def page_not_found2(e):
    return render_template('erreur2.html'),404


if __name__ == "__main__":
    Process(target= modeauto).start()
    Process(target=app.run(host='0.0.0.0',debug=False)).start()
    
    # a = Process(target= modeauto)
    # a.start()
    # while True:
    #     try:
    #         Process(target=app.run(host='0.0.0.0' , debug=False)).start() #mettre false a debug quand fin dev
    #         raise KeyboardInterrupt

    #     except KeyboardInterrupt:
    #         do = input("Etes-vous sur d'arreter le serveur?(y/n)")
    #         if (do == "y" or do == "Y"):
    #             a.kill()
    #             sys.exit("ARRET")
    #         else:
    #             print(erreur.messageatt())
