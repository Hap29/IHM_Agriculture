#!/usr/bin/python3
#coding: utf-8
########################################################
#### ©EmmanuelBOURHIS, 2021, BTS SN IR , LCR, BREST ####
########################################################
####
import requests as req
import json 
import datetime 
import mysql.connector
import base64
####
####  URL DOWNLINK DU TTN
url_ttn = 'mettresonurlttn downlink'
####
####CONNEXION A LA BDD AVEC MYSQL CONNECTOR
def conndb():
	return mysql.connector.connect(host="@ipbdd",user="admin",password="mot_de_passe", database="r2energie")
####
#### CONFIGURATION DE LA RECUPERATION ENDPOINT
def apipoint(rd) :
	Json = json.loads(rd.decode("utf_8"))                                      					#DECODAGE POUR CREER UN DICTIONNAIRE PYTHON
	payload_humair  = Json["payload_fields"]["humiditeair"]                    					#RECUPERATION DES DIFFERENTES DONNEES RECUES 
	payload_tempair = Json["payload_fields"]["temperatureair"] 
	payload_humsol  = Json["payload_fields"]["humiditesol"]  
	payload_tempsol = Json["payload_fields"]["temperaturesol"] 
	payload_soleil  = Json["payload_fields"]["ensoleillement"]
	return payload_humair, payload_tempair, payload_tempsol, payload_humsol, payload_soleil
####
####ECRITURE DANS LA BDD
def envoisql(humair,tempair,tempsol,humsol,soleil):
	db = conndb()                 		 #CONNEXION A LA BDD GRACE A LA FONCTION conndb()
	cur = db.cursor()			 		 #CREATION D'UN CURSEUR DANS LA BDD (sert a effectuer les actions sql)
	sql = "INSERT INTO DATAS_DEVICE (HUMIDITEAIR, TEMPERATUREAIR,TEMPERATURESOL,HUMIDITESOL, ENSOLEILLEMENT,DATE,HEURE) VALUES (%s, %s,%s, %s,%s,%s,%s)"  #REQUETE SQL
	date = str(datetime.date.today())   						   #RECUPERATION DE LA DATE DU JOUR
	heure = str(datetime.datetime.now().strftime("%H:%M:%S"))      #RECUPERATION DE L'HEURE ACTUELLE
	value = (humair, tempair,tempsol,humsol, soleil, date, heure ) #ENTREE DES VALEURS DANS L'ORDRE DE CORRESPONDANCE SQL 
	cur.execute(sql,value) 										   #EXECUTION DE LA REQUETE SQL AVEC LE CURSEUR
	db.commit()													   #VALIDATION DE LA TRANSACTION
	db.close()													   #FERMETURE DE LA CONNEXION A LA BASE
	return "Envoi ok"											   #RETOUR OK (pour debug seulement)
####
####ENVOI DE LA DONNEE DE REGLAGE
def reglage(ent) :     											   #arrivee 'ent' type str/chaine de characteres
    ent = float(ent)   											   #CONVERSION DE LA CHAINE DE CHARACTERES EN NOMBRE REEL
    ent = int((ent * 255) / 10)									   #CONVERSION EN INTEGER DU NOMBRE APPROCHEE POUR UN OCTECT A PARTIR DE 10 VALEURS
    convb = bytes([ent])										   #RETOURNE UN OBJECT D'OCTECTS
    convb64 = base64.b64encode(convb)							   #ENCODE EN BASE 64 LA VALEUR RECUPEREE ET CONVERTIE CI-DESSUS
    payload = convb64.decode('utf-8')							   #DECODAGE DE LA CONVERSION EN UTF-8 POUR L'ENVOI D'UNE CHAINE DE CHARACTERES
    post = {"dev_id": "controleur1-serre", "port": 1,"payload_raw": payload }    #DONNEES POUR LE TTN SOUS FORME REQUISE POUR TTN
    req.post( url_ttn , json = post) 					           #ENVOI DE LA TRAME						
####
####RECUPERATION DES 20 DERNIERE DONNEE DE LA BASE POUR LE GRAPHIQUE
def sqlgraph():
	db = conndb()   											#CONNEXION A LA BDD GRACE A LA FONCTION conndb()
	cur = db.cursor()											#CREATION D'UN CURSEUR DANS LA BDD (rappel : sert a effectuer les actions sql)
	cur.execute("SELECT HUMIDITEAIR, TEMPERATUREAIR,TEMPERATURESOL,HUMIDITESOL, ENSOLEILLEMENT,DATE,HEURE FROM DATAS_DEVICE ORDER BY idDATAS_DEVICE DESC LIMIT 20") #REQUETE SQL
	res = cur.fetchall()										#RECUPERATION DES DONNEES
	db.close()													#FERMETURE DE LA CONNEXION A LA BDD
	tempair = []												#TABLEAU DE VARIABLES DU GRAPHIQUE
	tempsol = []
	humair  = []
	humsol  = []
	enso    = []
	date    = []
	time    = []
	for i in res :											   #CORRESPONDANCE DES VALEURS RECUES AVEC LE SQL DANS LES TABLEAUX RESPECTIFS
		humair.append(i[0])
		tempair.append(i[1])
		tempsol.append(i[2])
		humsol.append(i[3])
		enso.append(i[4])
		date.append(i[5])
		time.append(i[6])
	return humair,tempair,tempsol,humsol,enso,time            #RETOUR DES TABLEAUX DE VALEURS POUR LES POINTS DES GRAPHIQUES
####
####RECUPERATION DE L'HEURE A UN MOMENT T
def tempfixe():
	date = datetime.datetime.now()						      #RECUPERATION DE LA DATE ET L'HEURE
	h = str(date.hour)										  #RECUPERATION DE L'HEURE ET CONVERTION EN CHAINE DE CHARACTERE
	m = str(date.minute)									  #RECUPERATION DES MINUTES ET CONVERTION EN CHAINE DE CHARACTERE
	s = str(date.second)									  #RECUPERATION DES SECONDES ET CONVERTION EN CHAINE DE CHARACTERE
	heure =  h +":"+m+":"+s 								  #ASSEMBLAGE DE LA CHAINE DE CHARACTERE
	return heure											  #RETOUR DE L'HEURE (moment ou la fonction a ete appelle)
####	
####RECUPERATION DE LA DERNIERE VALEUR ENREGISTREE
def sqldernier() : 
	db = conndb()										      #CONNEXION A LA BDD GRACE A LA FONCTION conndb()
	cur = db.cursor()										  #CREATION D'UN CURSEUR DANS LA BDD (rappel : sert a effectuer les actions sql)
	cur.execute("SELECT HUMIDITEAIR, TEMPERATUREAIR,TEMPERATURESOL,HUMIDITESOL, ENSOLEILLEMENT FROM DATAS_DEVICE ORDER BY idDATAS_DEVICE DESC LIMIT 1") #REQUETE SQL
	res = cur.fetchall()									  #RECUPERATION DES DONNEES DE LA DERNIERE COMMANDE
	db.close()												  #FERMETURE DE LA CONNEXION A LA BASE
	for i in res:											  #CORRESPONDANCE DES VALEURS DE LA BDD AUX VARIABLES A RENVOYER 
		humiair = i[0]
		tempair = i[1]
		tempsol = i[2]
		humisol = i[3]
		soleil  = i[4]
	return humiair,tempair,tempsol,humisol,soleil			  #DERNIERES VALEURS A AFFICHER DANS LA PAGE PRINCIPALE 
####
####

