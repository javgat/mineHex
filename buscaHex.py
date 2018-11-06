#-*- coding: utf-8 -*-
'''
Primera practica de Paradigmas de Programacion: Buscaminas hexagonal en terminal con modificacion.
Modificacion: Si la primera celda abierta es una mina, se intercambia por la primera celda sin mina.
Entregado el 20 de Marzo de 2018, modificacion realizada el 24 de Abril de 2018
@author: Javier Gaton Herguedas @javgato, && Juan Gaton Herguedas @juagato
'''
import random

import sys #Lo uso para escribir sin espacios en bucles

filas=("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","@","#","$","%","&")#Listas que son utiles posteriormente
columnas=("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","=","+","-",":","/")

#____________________________________________________________________________________________________________________
#    PrTab: Imprime el tablero por pantalla sin los bordes. Version muy basica                                       |
#____________________________________________________________________________________________________________________|
'''
def PrTab(Tablero):
    for i in range(len(Tablero)):
        if i%2==0:
            print " ",
        for j in range(len(Tablero[i])):
            print Tablero[i][j][0]," ",
        print ""
    return 0
'''
#____________________________________________________________________________________________________________________
#    PrTabPro: Imprime el tablero por pantalla, segun el Tab[][][1] que indica "visibilidad"                         |
#____________________________________________________________________________________________________________________|

def PrTabPro(Tablero):
    print"     ",
    for j in range(len(Tablero[0])):
        print columnas[j],
        print" ",
    print ""
    for i in range(len(Tablero)):
        if i==0:
            print "    ",
            sys.stdout.write(  u'\u250C' )
            for j in range(len(Tablero[i])-1):
                sys.stdout.write(u'\u2500' u'\u2500' u'\u2500'u'\u252C')
            sys.stdout.write( u'\u2500' u'\u2500' u'\u2500' u'\u2510')
            print ""
        print filas[i],
        if i%2==0:
            print " ",
        print u'\u2502',
        
        for j in range(len(Tablero[i])):
            if Tablero[i][j][1]==0:
                print u'\u2593',u'\u2502',
            elif Tablero[i][j][1]==1:
                if Tablero[i][j][0]==0:
                    print " ",u'\u2502',
                elif Tablero[i][j][0]<=-1:
                    print "?",u'\u2502',
                else:
                    print Tablero[i][j][0], u'\u2502',
            else:
                print"X",u'\u2502',
        print ""
        print "  ",
        if i<(len(Tablero)-1):
            if i%2==0:
                sys.stdout.write(u'\u250C')
                for j in range(len(Tablero[i])):
                    sys.stdout.write( u'\u2500' u'\u2534' u'\u2500' u'\u252C')
                sys.stdout.write( u'\u2500' u'\u2518')
            else:
                sys.stdout.write(u'\u2514')
                for j in range(len(Tablero[i])):
                    sys.stdout.write( u'\u2500' u'\u252C' u'\u2500' u'\u2534')
                sys.stdout.write( u'\u2500' u'\u2510')
        else:
            if i%2==0:
                print " ",
            sys.stdout.write(u'\u2514')
            for j in range(len(Tablero[i])-1):
                sys.stdout.write( u'\u2500' u'\u2500' u'\u2500' u'\u2534')
            sys.stdout.write( u'\u2500' u'\u2500' u'\u2500' u'\u2518')
        print ""
        
        
    return 0

#____________________________________________________________________________________________________________________
#    CreaTab: Crea una lista doble inicializada a 0                                                                  |
#____________________________________________________________________________________________________________________|

def CreaTab(nfilas, ncolumnas):
    tablero=[]
    for i in range (nfilas):
        tablero.append([])
        for j in range(ncolumnas):
            tablero[i].append([])
            tablero[i][j].append(0)#En esto irá la bomba o la cantidad de bombas que rodean
            tablero[i][j].append(0)#Oculto=0, Visionada=1, Marcada=2
    return tablero

#____________________________________________________________________________________________________________________
#    GenBomb: Genera bombas aleatoriamente, con la misma probabilidad en cada casilla                                |
#____________________________________________________________________________________________________________________|


def GenBomb(Tablero, nbomb):#Las bombas van escritas como 1, vacio como 0
    bombas=0
    while bombas<nbomb:
        ialeat=int(len(Tablero)*random.random())
        jaleat=int(len(Tablero[0])*random.random())
        if Tablero[ialeat][jaleat][0]==0:
            Tablero[ialeat][jaleat][0]="*"
            bombas+=1
    return Tablero

def ResetRodeo(Tab):
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            if Tab[i][j][0]!="*":
                Tab[i][j][0]=0
    return Tab

def CambiarMina(Tab, filamina, columnamina):
    encontrada= False
    i=0
    while i<len(Tab) and encontrada==False:
        j=0
        while j<len(Tab[i]) and encontrada==False:
            if Tab[i][j][0]!="*":
                encontrada=True
                Tab[i][j][0]="*"
                Tab[filamina][columnamina][0]=0
                Tab=ResetRodeo(Tab)
                RodeoBomb(Tab)
            j+=1
        i+=1
    return Tab

#____________________________________________________________________________________________________________________
#    RodeoBomb: Da a las casillas no bombas el valor de la cantidad de bombas que las rodean                         |
#____________________________________________________________________________________________________________________|

def RodeoBomb(Tablero):
    for i in range(len(Tablero)):
        for j in range(len(Tablero[i])):
            if Tablero[i][j][0]=="*":
                PosImp=0#PosImp valdra 1 si es fila impar. Para al comprobar compruebe correcto
                if i%2==0:
                    PosImp=1
                if j>0:
                    if Tablero[i][j - 1][0] != "*":
                        Tablero[i][j - 1][0]+=1
                if  j+1<len(Tablero[i]):
                    if Tablero[i][j + 1][0] != "*":
                        Tablero[i][j + 1][0]+=1
                if i>0:
                    if (j+PosImp)>0:
                        if Tablero[i - 1][j - 1 + PosImp][0]!="*":
                            Tablero[i - 1][j - 1 + PosImp][0]+=1
                    if (j+PosImp)<len(Tablero[i]):
                        if Tablero[i - 1][j + PosImp][0]!="*":
                            Tablero[i - 1][j + PosImp][0]+=1
                if i+1<len(Tablero):
                    if (j+PosImp)>0:
                        if Tablero[i + 1][j - 1 + PosImp][0]!="*":
                            Tablero[i + 1][j - 1 + PosImp][0]+=1
                    if (j+PosImp)<len(Tablero[i]):
                        if Tablero[i + 1][j + PosImp][0]!="*":
                            Tablero[i + 1][j + PosImp][0]+=1
    return Tablero

#____________________________________________________________________________________________________________________
#    pertenece: Comprueba que un elemento pertenezca a un conjunto [posini,posfin]                                   |
#____________________________________________________________________________________________________________________|

def pertenece(valor,conjunto,posini,posfin):
    pertenencia=False
    i=posini
    while i<=posfin and pertenencia==False:
        if valor==conjunto[i]:
            pertenencia=True
        i+=1
    return pertenencia

#____________________________________________________________________________________________________________________
#    pedirvalor: Pide valor con recursividad hasta que sea correcto                                                  |
#____________________________________________________________________________________________________________________|

def pedirvalor(Tab):
    scanner=(raw_input("Indique celda y accion (! marcar, * abrir): ")).strip()
    if len(scanner)<3:
        print "Entrada erronea, no consta de suficientes elementos." #Cambiar luego
        scanner=pedirvalor(Tab)
    if len(scanner)%3!=0:
        print "Entrada erronea, faltan o sobran elementos." #Cambiar luego
        scanner=pedirvalor(Tab)
    a=len(scanner)/3
    i=0
    nofin=True
    while i<a and nofin==True:
        p=3*i
        if len(Tab)<=26:
            if scanner[0+p] <"A" or scanner[0+p]>filas[len(Tab)-1]:
                print "Entrada erronea, primer elemento de alguna instruccion no comprendido." #Cambiar luego
                scanner=pedirvalor(Tab)
                nofin=False
        else:
            if (scanner[0+p] <"A" or scanner[0+p]>"Z") and pertenece(scanner[0+p],filas,26,len(Tab)-1)==False:
                print "Entrada erronea, primer elemento de alguna instruccion no comprendido." #Cambiar luego
                scanner=pedirvalor(Tab)
                nofin=False
        if len(Tab[0])<=26:
            if scanner[1+p] <"a" or scanner[1+p]>columnas[len(Tab[0])-1]:
                print "Entrada erronea, segundo elemento de alguna instruccion no comprendido." #Cambiar luego
                scanner=pedirvalor(Tab)
                nofin=False
        else:
            if (scanner[1+p] <"a" or scanner[1+p]>"z") and pertenece(scanner[1+p],columnas,26,len(Tab[0])-1)==False:
                print "Entrada erronea, segundo elemento de alguna instruccion no comprendido." #Cambiar luego
                scanner=pedirvalor(Tab)
                nofin=False
        if scanner[2+p] !="!" and scanner[2+p]!="*":
            print "Entrada erronea, tercer elemento de alguna instruccion no comprendido." #Cambiar luego
            scanner=pedirvalor(Tab)
            nofin=False
        i+=1
    return scanner 

#____________________________________________________________________________________________________________________
#    marcarcasilla: Marca la celda si es que se puede, o la desmarca si ya lo esta                                   |
#____________________________________________________________________________________________________________________|

def marcarcasilla(Tablero,i,j):
    if Tablero[i][j][1]==0:
        Tablero[i][j][1]=2
        PosImp=0
        if i%2==0:
            PosImp=1
        if j>0:
            if Tablero[i][j - 1][0] != "*":
                Tablero[i][j - 1][0]-=1
        if  j+1<len(Tablero[i]):
            if Tablero[i][j + 1][0] != "*":
                Tablero[i][j + 1][0]-=1
        if i>0:
            if (j+PosImp)>0:
                if Tablero[i - 1][j - 1 + PosImp][0]!="*":
                    Tablero[i - 1][j - 1 + PosImp][0]-=1
            if (j+PosImp)<len(Tablero[i]):
                if Tablero[i - 1][j + PosImp][0]!="*":
                    Tablero[i - 1][j + PosImp][0]-=1
        if i+1<len(Tablero):
            if (j+PosImp)>0:
                if Tablero[i + 1][j - 1 + PosImp][0]!="*":
                    Tablero[i + 1][j - 1 + PosImp][0]-=1
            if (j+PosImp)<len(Tablero[i]):
                if Tablero[i + 1][j + PosImp][0]!="*":
                    Tablero[i + 1][j + PosImp][0]-=1
    elif Tablero[i][j][1]==2:
        Tablero [i][j][1]=0
        PosImp=0
        if i%2==0:
            PosImp=1
        if j>0:
            if Tablero[i][j - 1][0] != "*":
                Tablero[i][j - 1][0]+=1
        if  j+1<len(Tablero[i]):
            if Tablero[i][j + 1][0] != "*":
                Tablero[i][j + 1][0]+=1
        if i>0:
            if (j+PosImp)>0:
                if Tablero[i - 1][j - 1 + PosImp][0]!="*":
                    Tablero[i - 1][j - 1 + PosImp][0]+=1
            if (j+PosImp)<len(Tablero[i]):
                if Tablero[i - 1][j + PosImp][0]!="*":
                    Tablero[i - 1][j + PosImp][0]+=1
        if i+1<len(Tablero):
            if (j+PosImp)>0:
                if Tablero[i + 1][j - 1 + PosImp][0]!="*":
                    Tablero[i + 1][j - 1 + PosImp][0]+=1
            if (j+PosImp)<len(Tablero[i]):
                if Tablero[i + 1][j + PosImp][0]!="*":
                    Tablero[i + 1][j + PosImp][0]+=1              
    else:
        print "No se puede marcar una casilla abierta"
        
    return Tab

#____________________________________________________________________________________________________________________
#    abrircasilla: Abre la casilla si es que se puede, y abre con recursividad si es un 0                            |
#_______________________________________________________...*.._____________________________________________________________|

def abrircasilla(Tab,i,j,v,derrota):#v==1 es primera vez v==0 otra vez mayor
    if Tab[i][j][1]==2: 
        if v ==1:
            print "No se puede abrir una casilla marcada"
            
    elif Tab[i][j][1]==1:
        if v==1:
            if Tab[i][j][0]<=0:
                PosImp=0
                if i%2==0:
                    PosImp=1
                if j>0:
                    devolucion=abrircasilla(Tab,i,j - 1,0,derrota)
                    Tab=devolucion[0]
                    derrota=devolucion[1]
                if  j+1<len(Tab[i]):
                    devolucion=abrircasilla(Tab,i,j + 1,0,derrota)
                    Tab=devolucion[0]
                    derrota=devolucion[1]
                if i>0:
                    if (j+PosImp)>0:
                        devolucion=abrircasilla(Tab,i - 1,j - 1 + PosImp,0,derrota)
                        Tab=devolucion[0]
                        derrota=devolucion[1]
                    if (j+PosImp)<len(Tab[i]):
                        devolucion=abrircasilla(Tab,i - 1,j + PosImp,0,derrota)
                        Tab=devolucion[0]
                        derrota=devolucion[1]
                if i+1<len(Tab):
                    if (j+PosImp)>0:
                        devolucion=abrircasilla(Tab,i + 1,j - 1 + PosImp,0,derrota)
                        Tab=devolucion[0]
                        derrota=devolucion[1]
                    if (j+PosImp)<len(Tab[i]):
                        devolucion=abrircasilla(Tab,i + 1,j + PosImp,0,derrota)
                        Tab=devolucion[0]
                        derrota=devolucion[1]
            else:
                print "No se puede abrir una casilla cuyo numero estimado de minas que la rodean sea mayor que 0"
    else:
        Tab[i][j][1]=1
        if Tab[i][j][0]=="*":
            derrota=True
        elif Tab[i][j][0]<=0:
            PosImp=0
            if i%2==0:
                PosImp=1
            if j>0:
                devolucion=abrircasilla(Tab,i,j - 1,0,derrota)
                Tab=devolucion[0]
                derrota=devolucion[1]
            if  j+1<len(Tab[i]):
                devolucion=abrircasilla(Tab,i,j + 1,0,derrota)
                Tab=devolucion[0]
                derrota=devolucion[1]
            if i>0:
                if (j+PosImp)>0:
                    devolucion=abrircasilla(Tab,i - 1,j - 1 + PosImp,0,derrota)
                    Tab=devolucion[0]
                    derrota=devolucion[1]
                if (j+PosImp)<len(Tab[i]):
                    devolucion=abrircasilla(Tab,i - 1,j + PosImp,0,derrota)
                    Tab=devolucion[0]
                    derrota=devolucion[1]
            if i+1<len(Tab):
                if (j+PosImp)>0:
                    devolucion=abrircasilla(Tab,i + 1,j - 1 + PosImp,0,derrota)
                    Tab=devolucion[0]
                    derrota=devolucion[1]
                if (j+PosImp)<len(Tab[i]):
                    devolucion=abrircasilla(Tab,i + 1,j + PosImp,0,derrota)
                    Tab=devolucion[0]
                    derrota=devolucion[1]
            
    return (Tab, derrota)

#____________________________________________________________________________________________________________________
#    casillasabiertas: Comprueba si todas las casillas estan abiertas                                                |
#____________________________________________________________________________________________________________________|

def casillasabiertas(Tab,nbomb):
    num=0 # numero de casilles abiertes actualmente
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            if Tab[i][j][1]==1:
                num+=1
    fin=False
    if len(Tab)*len(Tab[0])-nbomb==num:
        fin=True
    return fin

#____________________________________________________________________________________________________________________
#    OpenTab: Copia Tab[][][0] en TabAbierta[][][0] y TabAbierta[][][1] lo inicializa a 1                            |
#____________________________________________________________________________________________________________________|

def OpenTab(Tab,TabAbierta):
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            TabAbierta[i][j][0]=Tab[i][j][0]
            TabAbierta[i][j][1]=1
    return TabAbierta


#____________________________________________________________________________________________________________________
#    juego: Llama a pedirvalor, y luego a marcarcasilla o abrircasilla                                               |
#____________________________________________________________________________________________________________________|

def juego(Tab, nbomb, TabAbierta):
    primeravez=True
    derrota = False
    todasabiertas= False
    while derrota==False and todasabiertas==False:
        scanner=pedirvalor(Tab)  
        a=len(scanner)/3
        for b in range(0,a):
            p=3*b
            i=0
            j=0
            if scanner[0+p]>="A" and scanner[0+p]<="Z":
                i = ord(scanner[0+p])-ord("A")
            elif scanner[0+p]=="@":
                i=26
            elif scanner[0+p]=="#":
                i=27
            elif scanner[0+p]=="$":
                i=28
            elif scanner[0+p]=="%":
                i=29
            elif scanner[0+p]=="&":
                i=30
            if scanner[1+p]>="a" and scanner[1+p]<="z":
                j = ord(scanner[1+p])-ord("a")
            elif scanner[1+p]=="=":
                j=26
            elif scanner[1+p]=="+":
                j=27
            elif scanner[1+p]=="-":
                j=28
            elif scanner[1+p]==":":
                j=29
            elif scanner[1+p]=="/":
                j=30
            if scanner[2+p] == "*":
                devolucion= abrircasilla(Tab,i,j,1,derrota)
                Tab=devolucion[0]
                derrota=devolucion[1]
                if primeravez==True:
                    if derrota==True:
                        Tab=CambiarMina(Tab,i,j)
                        derrota=False
                        TabAbierta=OpenTab(Tab,TabAbierta)
                primeravez=False
            else:
                Tab = marcarcasilla(Tab,i,j)
            PrTabPro(Tab)
        todasabiertas=casillasabiertas(Tab, nbomb)
    return derrota

#____________________________________________________________________________________________________________________
#    MAIN: El Menu, pide opcion en try para evitar errores. Luego inicia y llama a juego.                            |
#____________________________________________________________________________________________________________________|

from time import time
selector=0
while selector!=5:
    print ("BUSCAMINAS\n----------\n1. Principiante (9x9, 10 minas)\n2. Intermedio (16x16, 40 minas)\n3. Experto (16x30, 99 minas)\n4. Leer de fichero\n5. Salir")
    repetir=True
    while repetir==True:
        try:
            selector=int(raw_input("Escoja opcion: "))
        except:
            ValueError
            print("Perdona, no te he entendido")
        else:
            repetir=False
    while selector<1 or selector>5:
        try:
            selector=int(raw_input("Escoja una opcion existente (1 a 5): "))
        except:
            ValueError
            print("Perdona, no te he entendido")
    nbomb=0
    if selector!=5 and selector!=4:
        if selector==1:
            nbomb=10
            Tab=CreaTab(9,9)
            TabAbierta=CreaTab(9,9)
            
        elif selector==2:
            nbomb=40
            Tab=CreaTab(16,16)
            TabAbierta=CreaTab(16,16)
        elif selector==3:
            nbomb=99
            Tab=CreaTab(16,30)
            TabAbierta=CreaTab(16,30)
        Tab=GenBomb(Tab,nbomb)
        Tab = RodeoBomb(Tab)
        TabAbierta=OpenTab(Tab,TabAbierta)
        PrTabPro(Tab)
        tiempoinicio=time()
        derrota=juego(Tab,nbomb,TabAbierta)
        tiempofin=time()
        tiempototal= tiempofin-tiempoinicio
        if derrota== True:
            PrTabPro(TabAbierta)
            print ("!Has perdido!")
        else:
            PrTabPro(TabAbierta)
            print("!Has ganado!")
        print "Has tardado: %.2f segundos" %tiempototal
    elif selector==4:
        nombrefich=raw_input("Introduzca el nombre del fichero que desea abrir:")
        try:
            Fichero=open(nombrefich)
            tamano= Fichero.readline()
            dimension=tamano.split(" ")
            Tab=CreaTab(int(dimension[0]),int(dimension[1]))
            TabAbierta=CreaTab(int(dimension[0]),int(dimension[1]))
            if(int(dimension[0])<31 and int(dimension[1])<31):
                nbomb=0
                for i in range (len(Tab)):
                    linea=Fichero.readline()    
                    for j in range (len(Tab[i])):
                        if linea[j]=="*":
                            Tab[i][j][0]="*"
                            nbomb+=1
                Fichero.close()
                Tab = RodeoBomb(Tab)
                TabAbierta=OpenTab(Tab,TabAbierta)
                PrTabPro(Tab)
                tiempoinicio=time()
                derrota=juego(Tab,nbomb,TabAbierta)
                tiempofin=time()
                tiempototal= tiempofin-tiempoinicio
                if derrota== True:
                    PrTabPro(TabAbierta)
                    print ("!Has perdido!")
                else:
                    PrTabPro(TabAbierta)
                    print("!Has ganado!")
                print "Has tardado: %.2f segundos" %tiempototal
            else:
                print "Tamaño de alguna dimension de la tabla del fichero superior al maximo (30). No puedo ejecutarlo."
        except IOError:
            print ("No se pudo abrir el fichero seleccionado")
        
        
print("!Adios! :D")
