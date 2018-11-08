# -*- coding: utf-8 -*-

'''
Autores: Javier Gaton Herguedas y Juan Gaton Herguedas. T3, L8.
Practica II Paradigmas de Programacion: Buscaminas en interfaz grafica GTK
Archivo fuente de funciones abstract
'''

from random import random

MAXDIM=36

def GenBomb(Tab, nbomb):#Las bombas van escritas como 1, vacio como 0
    bombas=0
    while bombas<nbomb:
        ialeat=int(len(Tab)*random())
        jaleat=int(len(Tab[0])*random())
        if Tab[ialeat][jaleat][0]==0:
            Tab[ialeat][jaleat][0]="*"
            bombas+=1
    return Tab

def OpenTab(Tab,TabAbierta):
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            TabAbierta[i][j][0]=Tab[i][j][0]
            TabAbierta[i][j][1]=1
    return TabAbierta

def CopiaFich(Tab,nombrefich):
    try:
        Fichero=open(nombrefich)
        Fichero.readline()
        if(len(Tab)<MAXDIM and len(Tab[0])<MAXDIM):
            nbomb=0
            for i in range (len(Tab)):
                linea=Fichero.readline()    
                for j in range (len(Tab[i])):
                    if linea[j]=="*":
                        Tab[i][j][0]="*"
                        nbomb+=1
            Fichero.close()
        else:
            print "Tamano de alguna dimension de la tabla del fichero superior al maximo (50). No puedo ejecutarlo."
    except IOError:
        print ("No se pudo abrir el fichero seleccionado")
    return (Tab,nbomb)

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

def casillasabiertas(Tab,nbomb):
    num=0 # numero de casilles abiertes actualmente
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            if Tab[i][j][1]==1:
                num+=1
    fin=False
    if len(Tab)*len(Tab[0])-nbomb<=num:
        fin=True
    return fin

def cantidadmarcas(Tab):
    cont=0
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            if Tab[i][j][1]==2:
                cont=cont+1
    return cont

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

def CreaTab(nfilas, ncolumnas):
    tablero=[]
    for i in range (nfilas):
        tablero.append([])
        for j in range(ncolumnas):
            tablero[i].append([])
            tablero[i][j].append(0)
            tablero[i][j].append(0)
    return tablero
def CopiaTab(Tab,TabCopia):
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            TabCopia[i][j][0]=Tab[i][j][0]
            TabCopia[i][j][1]=Tab[i][j][1]
    return TabCopia

def ReiniciaTab(Tab):
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            Tab[i][j][0]=0
            Tab[i][j][1]=0
    return Tab

def TabFinal(Tab,TabAbierta):
    for i in range(len(Tab)):
        for j in range(len(Tab[i])):
            if Tab[i][j][0]=="*":
                if Tab[i][j][1]==0:
                    Tab[i][j][1]=1
            else:
                if Tab[i][j][1]==2:
                    Tab[i][j][1]=-1
                else:
                    Tab[i][j][0]=TabAbierta[i][j][0]
                    if Tab[i][j][1]==0:
                        Tab[i][j][1]=1
    return Tab

def abrircasilla(Tab,i,j,v,derrota):#v==1 es primera vez v==0 otra vez mayor
    #if Tab[i][j][1]==2:
        #if v ==1:
        #    print "No se puede abrir una casilla marcada"
            
    if Tab[i][j][1]==1:
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
            #else:
                #print "No se puede abrir una casilla cuyo numero estimado de minas que la rodean sea mayor que 0"
    elif Tab[i][j][1]==0:
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
    #else:
    #    print "No se puede marcar una casilla abierta"
        
    return Tablero