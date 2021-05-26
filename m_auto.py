#!/usr/bin/python3
#coding: utf-8
########################################################
#### ©EmmanuelBOURHIS, 2021, BTS SN IR , LCR, BREST ####
########################################################
from API import datas, erreur
import time 
def modeauto():  #0 = mode fixe dessus et 1 = mode auto dessus 
    while(True):
        try:
            dval = datas.sqldernier()#dernieres valeurs 
            #print("FCNT")
            res = datas.sqlvisucommande()  #visu du mode auto de la reglete ou manuel
            #print(dval)
            dicpara = datas.pageregmode() #visu des paramètres de réglages du la page du mode réglages
            #print(dicpara)   #[0] pour l'ensemble [x] pour l'id en partant de 0 [x1] pour la place dans la bdd
            time.sleep(1)
            for i in res:
                LED   = int(i[0])
                CHAUF = int(i[1])
                ARR   = int(i[2])
            if(LED == 0 or CHAUF == 0 or ARR == 0 ):
                pass
            ####
            ####
            if( LED == 1 ):
                if (dval[4] >= dicpara[0][0][5]) :
                    if(dicpara[0][0][10]==str(0)):  ##### différence pour le mode prog ou pas
                        datas.reglage(dicpara[0][0][7], 1)
                        datas.entreglageval(dicpara[0][0][7], 1,0)   # (val , id, besoinretour-->0)
                    elif(dicpara[0][0][10]==str(1)):
                        fonc = 1 #supprimer une fois la fonction ecrite
                        fonc = 1                        
                        #fonc = int((float(dval[4])*(float(dicpara[0][0][8])/float(dicpara[0][0][9])*-1))+10)  #dval[4] = luminusité
                        """if(fonc >= 10 ):
                            datas.reglage(10, 1)
                            datas.entreglageval(10, 1,0)
                        elif(fonc <= 0 ):
                            datas.reglage(0, 1)
                            datas.entreglageval(0, 1,0)"""
                        print(fonc)
                else:
                    datas.reglage(dicpara[0][0][6], 1)
                    datas.entreglageval(dicpara[0][0][6], 1,0)
            ####
            ####
            if( CHAUF == 1 ):
                if (dval[0] > dicpara[0][1][3] and dval[1] > dicpara[0][1][1]) :
                    if(dicpara[0][1][10]==str(0)):  ##### différence pour le mode prog ou pas
                        datas.reglage(dicpara[0][1][7], 2)
                        datas.entreglageval(dicpara[0][1][7], 2,0)   # (val , id, besoinretour-->0)
                    elif(dicpara[0][1][10]==str(1)):
                        fonc = 1
                        print("ecrire la fonction mathematique")#Faire la moyenne des deux fonctions avec les parametre différents
                        if(fonc >= 10 ):
                            datas.reglage(10, 2)
                            datas.entreglageval(10, 2,0)
                        elif(fonc <= 0 ):
                            datas.reglage(0, 2)
                            datas.entreglageval(0, 2,0)  
                else:
                    datas.reglage(dicpara[0][1][6], 2)
                    datas.entreglageval(dicpara[0][1][6], 2,0)
            ####
            ####
            if( ARR == 1 ):
                if ( dval[2] > dicpara[0][2][2] and dval[3] > dicpara[0][2][4]) :
                    if(dicpara[0][2][10]==str(0)):  ##### différence pour le mode prog ou pas
                        datas.reglage(dicpara[0][2][7], 3)
                        datas.entreglageval(dicpara[0][2][7], 3,0)   # (val , id, besoinretour-->0)
                    elif(dicpara[0][2][10]==str(1)):
                        fonc = 1
                        print("ecrire la fonction mathematique")  #Faire la moyenne des deux fonctions avec les parametre différents
                        if(fonc >= 10 ):
                            datas.reglage(10, 3)
                            datas.entreglageval(10, 3,0)
                        elif(fonc <= 0 ):
                            datas.reglage(0,3)
                            datas.entreglageval(0, 3,0)  
                else:
                    datas.reglage(dicpara[0][2][6], 3)
                    datas.entreglageval(dicpara[0][2][6], 3,0)
            ####
            ####            
        except KeyboardInterrupt:
            print(erreur.attention())
            continue

