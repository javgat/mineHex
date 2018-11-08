# -*- coding: utf-8 -*-
'''
Autores: Javier Gaton Herguedas y Juan Gaton Herguedas. T3, L8.
Practica II Paradigmas de Programacion: Buscaminas en interfaz grafica GTK
Codigo Principal a ejecutar
'''


import gtk
import time
import gobject
import minas    #archivo de funciones abstract
import random

NUMEXPL=4   #Numero de imagenes .gif de explosiones que hay
NUMVIC=4    #Numero de imagenes .gif de victoria que hay

class Tablero:
    def __del__(self):
        print "deleted"

    def borra_evento (self, wid, data = None):
        #print "\ndelete_event"
        if self.timer != None:
            gobject.source_remove(self.timer)
            self.timer = None
        return False
    def destruye (self, wid, data = None):
        #print "\ndestroy"
        gtk.main_quit()
        return None
    def click(self):
        self.dt = int(time.time() - self.tpo0)
        #print self.dt
        self.acttiempo()
        self.startclock()
        return None
    
    def acttiempo(self):
        dt=self.dt
        if dt==0:
            self.tiempo[0]=self.display[3][10]
            self.tiempo[1]=self.display[4][10]
            self.tiempo[2]=self.display[5][10]
        elif dt>99:
            self.tiempo[0]=self.display[3][dt/100]
            self.tiempo[1]=self.display[4][(dt%100)/10]
            self.tiempo[2]=self.display[5][(dt%100)%10]
        else:
            self.tiempo[0]=self.display[3][10]
            if dt>9:
                self.tiempo[1]=self.display[4][(dt%100)/10]
            else:
                self.tiempo[1]=self.display[4][10]
            self.tiempo[2]=self.display[5][(dt%100)%10]
        for i in range(3):
            self.tiempoev[i].remove(self.tiempoev[i].get_children()[0])
            self.tiempoev[i].add(self.tiempo[i])
        self.tiempopantalla.show_all()
        return None
    
    def activatiempo(self):
        if(self.primerajugada==True):
            self.tpo0 = time.time()
            self.primerajugada=False
            self.startclock()
        return None

    def startclock(self):
        self.timer = gobject.timeout_add(1000, self.click)
        return True

    def fin(self,Abierto):
        if self.timer != None:
            gobject.source_remove(self.timer)
            self.timer = None
        rand=int(random.random()*NUMEXPL)
        #print rand
        self.resetbtn.remove(self.resetbtn.get_child())
        self.PanelFin=gtk.Window()
        self.Barrasfin=gtk.VBox()
        self.MensajeFin=gtk.Label("Derrota")
        self.imagefin=gtk.Image()
        if Abierto==True:
            self.resetbtn.add(self.smileyimgs[2])
            self.MensajeFin=gtk.Label("Victoria")
            self.imagefin.set_from_file("victoria/vic"+str(rand)+".gif")
            self.PanelFin.set_title("Victoria")
        else:
            self.resetbtn.add(self.smileyimgs[3])
            self.PanelFin.set_title("Derrota")
            self.imagefin.set_from_file("explosion/exp"+str(rand)+".gif")
        self.resetbtn.show_all()
        self.Tab=minas.TabFinal(self.Tab,self.TabAbierta)
        self.actualizabotones()
        self.Barrasfin.pack_start(self.MensajeFin)
        self.Barrasfin.pack_start(self.imagefin)
        self.PanelFin.add(self.Barrasfin)
        self.PanelFin.show_all()
        return None

    def clickizq(self,widget,event,data=None):
        if event.button==1:
            if self.primerajugada==True:
                self.activatiempo()
                if self.Tab[data[0]][data[1]][0]=="*":
                    self.Tab=minas.CambiarMina(self.Tab,data[0],data[1])
                    self.TabAbierta=minas.OpenTab(self.Tab,self.TabAbierta)
                self.primerajugada=False
            CopTab=minas.CreaTab(len(self.Tab),len(self.Tab[0]))
            CopTab=minas.CopiaTab(self.Tab, CopTab)
            modifica=minas.abrircasilla(CopTab,data[0],data[1],1,self.derrota)
            self.Tab=minas.CopiaTab(modifica[0],self.Tab)
            if self.Tab[data[0]][data[1]][0]=="*" and self.Tab[data[0]][data[1]][1]!=2 :
                self.Tab[data[0]][data[1]][1]=-2
            self.derrota=modifica[1]
            self.actualizabotones()
            #print "Pulsado el boton"+str(data)
            if self.derrota==True:
                self.fin(False)
            elif minas.casillasabiertas(self.Tab,self.nbomb):
                self.fin(True)
        return None

    def actdisplaybombas(self):
        bombas=self.nbomb-minas.cantidadmarcas(self.Tab)
        if bombas<0:
            self.bombasquedan[0]=self.display[0][10]
            self.bombasquedan[1]=self.display[1][10]
            self.bombasquedan[2]=self.display[2][10]
        elif bombas>99:
            self.bombasquedan[0]=self.display[0][bombas/100]
            self.bombasquedan[1]=self.display[1][(bombas%100)/10]
            self.bombasquedan[2]=self.display[2][(bombas%100)%10]
        else:
            self.bombasquedan[0]=self.display[0][10]
            if bombas>9:
                self.bombasquedan[1]=self.display[1][(bombas%100)/10]
            else:
                self.bombasquedan[1]=self.display[1][10]
            self.bombasquedan[2]=self.display[2][(bombas%100)%10]
        for i in range(3):
            self.bombasquedevent[i].remove(self.bombasquedevent[i].get_children()[0])
            self.bombasquedevent[i].add(self.bombasquedan[i])
        self.celdasfaltan.show_all()
        return None
        
    def clickdch(self,widget,event,data=None):
        if event.button==3:
            self.Tab=minas.marcarcasilla(self.Tab,data[0],data[1])
            self.actdisplaybombas()
            self.actualizabotones()
        return None

    def opening(self,widget,event,data=None):
        if event.button==1 and self.Tab[data[0]][data[1]][1]!=2:
            if self.Tab[data[0]][data[1]][0]!="*" or self.primerajugada==True:
                self.imgcontrol[data[0]][data[1]]=self.imgs[data[0]][data[1]][11]
            else:
                self.imgcontrol[data[0]][data[1]]=self.imgs[data[0]][data[1]][12]
                self.derrota=True
            self.Tab[data[0]][data[1]][2].remove(self.Tab[data[0]][data[1]][2].get_children()[0])
            self.Tab[data[0]][data[1]][2].add(self.imgcontrol[data[0]][data[1]])
            self.ventana.show_all()
        return None

    def CreaTab(self):
        self.Tab=[]
        for i in range(self.nfilas):
            self.Tab.append([])
            for j in range(self.ncolumnas):
                self.Tab[i].append([])
                self.Tab[i][j].append(0)#el valor
                self.Tab[i][j].append(0)#el tipo (abierto cerrado..)
                self.Tab[i][j].append(gtk.EventBox())
                self.imgcontrol[i][j]=self.imgs[i][j][7]
                self.Tab[i][j][2].add(self.imgcontrol[i][j])
                self.Tab[i][j][2].connect("button-press-event", self.opening,(i,j))
                self.Tab[i][j][2].connect("button-release-event", self.clickizq,(i,j))
                self.Tab[i][j][2].connect("button-release-event", self.clickdch,(i,j))
        return self.Tab

    def actualizabotones(self):
        for i in range(len(self.Tab)):
            for j in range(len(self.Tab[i])):
                if self.Tab[i][j][1]==0:
                    self.imgcontrol[i][j]=self.imgs[i][j][7]
                    self.Tab[i][j][2].remove(self.Tab[i][j][2].get_children()[0])
                    self.Tab[i][j][2].add(self.imgcontrol[i][j])
                elif self.Tab[i][j][1]==1:
                    if self.Tab[i][j][0]<0:
                        self.imgcontrol[i][j]=self.imgs[i][j][8]
                        self.Tab[i][j][2].remove(self.Tab[i][j][2].get_children()[0])
                        self.Tab[i][j][2].add(self.imgcontrol[i][j])
                    elif self.Tab[i][j][0]=="*":
                        self.imgcontrol[i][j]=self.imgs[i][j][9]
                        self.Tab[i][j][2].remove(self.Tab[i][j][2].get_children()[0])
                        self.Tab[i][j][2].add(self.imgcontrol[i][j])
                    else:
                        self.imgcontrol[i][j]=self.imgs[i][j][self.Tab[i][j][0]]
                        self.Tab[i][j][2].remove(self.Tab[i][j][2].get_children()[0])
                        self.Tab[i][j][2].add(self.imgcontrol[i][j])
                elif self.Tab[i][j][1]==-1:
                    self.imgcontrol[i][j]=self.imgs[i][j][13]
                    self.Tab[i][j][2].remove(self.Tab[i][j][2].get_children()[0])
                    self.Tab[i][j][2].add(self.imgcontrol[i][j])
                elif self.Tab[i][j][1]==-2:
                    self.imgcontrol[i][j]=self.imgs[i][j][12]
                    self.Tab[i][j][2].remove(self.Tab[i][j][2].get_children()[0])
                    self.Tab[i][j][2].add(self.imgcontrol[i][j])
                else:
                    self.imgcontrol[i][j]=self.imgs[i][j][10]
                    self.Tab[i][j][2].remove(self.Tab[i][j][2].get_children()[0])
                    self.Tab[i][j][2].add(self.imgcontrol[i][j])
        self.ventana.show_all()
        return self.Tab

    def cargaimagen(self,carpeta):
        self.smileyimgs=[]
        for i in range(self.nfilas):
            self.imgs.append([])
            for j in range(self.ncolumnas):
                self.imgs[i].append([])
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][0].set_from_file(carpeta+"xcelda_0.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][1].set_from_file(carpeta+"xcelda_1.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][2].set_from_file(carpeta+"xcelda_2.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][3].set_from_file(carpeta+"xcelda_3.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][4].set_from_file(carpeta+"xcelda_4.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][5].set_from_file(carpeta+"xcelda_5.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][6].set_from_file(carpeta+"xcelda_6.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][7].set_from_file(carpeta+"xcelda_cerrada.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][8].set_from_file(carpeta+"xcelda_question.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][9].set_from_file(carpeta+"xcelda_mina.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][10].set_from_file(carpeta+"xcelda_marcada.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][11].set_from_file(carpeta+"xcelda_open.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][12].set_from_file(carpeta+"xcelda_boom.png")
                self.imgs[i][j].append(gtk.Image())
                self.imgs[i][j][13].set_from_file(carpeta+"xcelda_marcada_error.png")
        self.smileyimgs.append(gtk.Image())
        self.smileyimgs[0].set_from_file(carpeta+"smiley.png")
        self.smileyimgs.append(gtk.Image())
        self.smileyimgs[1].set_from_file(carpeta+"smiley_press.png")
        self.smileyimgs.append(gtk.Image())
        self.smileyimgs[2].set_from_file(carpeta+"smiley_win.png")
        self.smileyimgs.append(gtk.Image())
        self.smileyimgs[3].set_from_file(carpeta+"smiley_dead.png")
        self.display=[]
        for i in range (6):
            self.display.append([])
            for j in range (10):
                self.display[i].append(gtk.Image())
                self.display[i][j].set_from_file(carpeta+"display_"+str(j)+".png")            
            self.display[i].append(gtk.Image())
            self.display[i][10].set_from_file(carpeta+"display_empty.png")
        return None
    
    def resettiempo(self):
        for i in range(3):
            self.tiempo[i]=self.display[i+3][10]
            self.tiempoev[i].remove(self.tiempoev[i].get_children()[0])
            self.tiempoev[i].add(self.tiempo[i])
        self.tiempopantalla.show_all()
        return None
    
    def pressreset(self,widget,event,data=None):
        if event.button==1:
            self.resetbtn.remove(self.resetbtn.get_child())
            self.resetbtn.add(self.smileyimgs[1])
            self.resetbtn.show_all()
        return None

    def reset(self,widget,event,data=None):
        if event.button==1:
            self.resetbtn.remove(self.resetbtn.get_child())
            self.resetbtn.add(self.smileyimgs[0])
            #print "reset"
            if self.timer != None:
                gobject.source_remove(self.timer)
                self.timer = None
            self.derrota=False
            self.dt=0
            self.resettiempo()
            self.GenTab()
            self.actdisplaybombas()
            self.primerajugada=True
            self.actualizabotones()
        return None

    def GenTab(self):
        self.Tab=minas.ReiniciaTab(self.Tab)
        if self.lectura==False:
            self.Tab=minas.GenBomb(self.Tab,self.nbomb)
        else:
            result=minas.CopiaFich(self.Tab,self.nombrefich)
            self.Tab=result[0]
            self.nbomb=result[1]
        self.Tab=minas.RodeoBomb(self.Tab)
        self.TabAbierta=minas.CreaTab(self.nfilas,self.ncolumnas)
        self.TabAbierta=minas.OpenTab(self.Tab,self.TabAbierta)
        return None

    def cambiotema(self,widget,event, data=None):
        if event.button==1:
            self.carpeta=data
            self.cargaimagen(self.carpeta)
            self.actualizabotones()
            self.ventanatemas.hide_all()
            self.resetbtn.remove(self.resetbtn.get_child())
            if self.derrota==True:
                self.resetbtn.add(self.smileyimgs[3])
            else:
                self.resetbtn.add(self.smileyimgs[0])
            self.actdisplaybombas()
            self.resetbtn.show_all()
            self.acttiempo()
        return None
        
    def cambiartema(self,widget,event,data=None):
        if event.button==1:
            self.ventanatemas=gtk.Window()
            self.ventanatemas.set_border_width (20)
            self.ventanatemas.set_title("Temas")
            self.lineasdifs=gtk.VBox(homogeneous=True)
            self.temalab1=gtk.Label()
            self.temalab2=gtk.Label()
            self.titulotemas=gtk.Label("Escoja un Tema: ")
            self.cabeceratemas=gtk.HBox(homogeneous=True)
            self.cabeceratemas.pack_start(self.temalab1)
            self.cabeceratemas.pack_start(self.titulotemas)
            self.cabeceratemas.pack_start(self.temalab2)
            self.tablatemas=gtk.HBox(homogeneous=True)
            self.temaclasico=gtk.Button("Clasico")
            self.temaclasico.connect("button-press-event",self.cambiotema,"celdaimg/")
            self.temablue=gtk.Button("Blue")
            self.temablue.connect("button-press-event",self.cambiotema,"blue/")
            self.temaflash=gtk.Button("Flash")
            self.temaflash.connect("button-press-event",self.cambiotema,"flash/")
            self.tablatemas.pack_start(self.temaclasico)
            self.tablatemas.pack_start(self.temablue)
            self.tablatemas.pack_start(self.temaflash)
            self.lineasdifs.pack_start(self.cabeceratemas)
            self.lineasdifs.pack_start(self.tablatemas)
            self.ventanatemas.add(self.lineasdifs)
            
            self.ventanatemas.show_all()
        return None

    def __init__(self,nfilas,ncolumnas,nbomb,lectura):
        self.timer=None
        self.dt=0
        self.nbomb=0
        self.nombrefich=""
        self.lectura=lectura
        #nbomb puede ser bomba o numero de fichero
        if self.lectura:
            self.nombrefich=nbomb
        else:
            self.nbomb=nbomb
        self.nfilas=nfilas
        self.ncolumnas=ncolumnas
        self.derrota=False
        self.primerajugada=True
        self.imgs=[]
        self.imgcontrol=[]
        self.smiley=gtk.Image()
        for i in range(nfilas):
            self.imgcontrol.append([])
            for j in range(ncolumnas):
                self.imgcontrol[i].append(gtk.Image())
        self.carpeta="celdaimg/"
        self.cargaimagen(self.carpeta)
        self.ventana = gtk.Window (gtk.WINDOW_TOPLEVEL)
        self.ventana.set_resizable(False)
        self.ventana.set_title("Buscaminas")
        self.ventana.connect ("delete_event", self.borra_evento)
        self.ventana.connect ("destroy", self.destruye)
        self.ventana.set_border_width (15) #el padding
        #self.grid es la tabla que separa cabecera de juego
        self.grid=gtk.VBox(spacing=2)
        #self.cabecera centro es la cabecera
        self.cabeceracentro=gtk.HBox(homogeneous=False,spacing=2)
        #self.cabecera es la caja donde esta la cabecera
        self.cabecera=gtk.HBox(homogeneous=False)
        #celdas faltan es la caja donde estan las imagenes de celdas (izd)
        self.celdasfaltan=gtk.HBox()
        self.bombasquedan=[]
        self.bombasquedevent=[]
        for i in range(3):
            self.bombasquedan.append(gtk.Image())
            self.bombasquedevent.append(gtk.EventBox())
            self.bombasquedan[i]=self.display[i][10]
            self.bombasquedevent[i].add(self.bombasquedan[i])            
            self.celdasfaltan.pack_start(self.bombasquedevent[i])
        #resetbtn es el boton de la carita
        self.resetbtn=gtk.EventBox()
        self.resetbtn.connect("button-press-event",self.pressreset)
        self.resetbtn.connect("button-release-event",self.reset)
        self.resetbtn.add(self.smileyimgs[0])
        #tiempo
        self.tiempopantalla=gtk.HBox()
        self.tiempo=[]
        self.tiempoev=[]
        for i in range(3):
            self.tiempo.append(gtk.Image())
            self.tiempoev.append(gtk.EventBox())
            self.tiempo[i]=self.display[i+3][10]
            self.tiempoev[i].add(self.tiempo[i])            
            self.tiempopantalla.pack_start(self.tiempoev[i])
        self.cabeceracentro.pack_start(self.celdasfaltan)
        self.cabeceracentro.pack_start(self.resetbtn,False,False)
        self.cabeceracentro.pack_start(self.tiempopantalla)
        self.Labelrelleno1=gtk.Label(None)
        self.Labelrelleno2=gtk.Label(None)
        self.cabecera.pack_start(self.Labelrelleno1)
        self.cabecera.pack_start(self.cabeceracentro,False,False)
        self.cabecera.pack_start(self.Labelrelleno2)
        self.tabla = gtk.Table(rows=self.nfilas*2, columns=(self.ncolumnas*2)+1, homogeneous=False)
        self.supercab=gtk.HBox(homogeneous=True)
        self.temaselect=gtk.Button("Cambiar Tema")
        self.temaselect.connect("button-press-event",self.cambiartema)
        self.supercab.pack_start(self.temaselect)
        self.grid.pack_start(self.supercab)
        self.grid.pack_start(self.cabecera,False,False)
        self.tablarod=gtk.HBox()
        self.label3=gtk.Label(None)
        self.label4=gtk.Label(None)
        self.tablarod.pack_start(self.label3)
        self.tablarod.pack_start(self.tabla)
        self.tablarod.pack_start(self.label4)
        self.grid.pack_start(self.tablarod)
        self.ventana.add(self.grid)
        
        

        self.Tab=self.CreaTab()
        self.GenTab()
        self.actdisplaybombas()
        for i in range(self.nfilas):
            for j in range(self.ncolumnas):
                self.tabla.attach(self.Tab[i][j][2],(j*2)+((i+1)%2),((j+1)*2)+((i+1)%2),i*2,(i+1)*2,True,False)
        self.ventana.show_all()
        return None

    def main(self):
        gtk.main()
        return None


class   buscaminas():
    def borra_evento (self, wid, data = None):
        #print "\ndelete_event"
        return False
    def destruye (self, wid, data = None):
        #print "\ndestroy"
        self.select=2
        gtk.main_quit()
        return None

    def partida(self, wid, data = None):
        self.select=data[0]
        self.nfila=data[1]
        self.ncolumn=data[2]
        self.nbomb=data[3]
        gtk.main_quit()
        return None

    def leerarchivo(self,data=None):
        try:
            Fichero=open(self.nombrefich.get_text())
            tamano= Fichero.readline()
            dimension=tamano.split(" ")
            self.nfila=int(dimension[0])
            self.ncolumn=int(dimension[1])
            self.select=1
            gtk.main_quit()
            Fichero.close()
        except:
            print ("No se pudo abrir el fichero seleccionado")
        return None

    def leer(self,wid, data=None):
        self.elige=gtk.FileChooserDialog("Elige un archivo",None, gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response=self.elige.run() #if cancelar response =-6, if abrir response = -5
        auxiliar=self.elige.get_filename()
        if auxiliar!=None:
            self.nombrefich.set_text(auxiliar)
        else:
            self.nombrefich.set_text("Nada seleccionado")
        if response==-5:
            self.leerarchivo()
        #print self.nombrefich.get_text()
        self.elige.destroy()
        return None

    def __init__(self):
        self.select=0
        self.nfila=0
        self.ncolumn=0
        self.nbomb=0
        self.ventana = gtk.Window (gtk.WINDOW_TOPLEVEL)
        self.ventana.set_title("Buscaminas HEX")
        self.ventana.set_resizable(False)
        #self.ventana.modify_bg(gtk.STATE_NORMAL,gtk.gdk.Color_parse(red=60000, blue=60000, green=65535))
        self.ventana.connect ("delete_event", self.borra_evento)
        self.ventana.connect ("destroy", self.destruye)
        self.ventana.set_border_width (50) #el padding
        self.tabla = gtk.VBox (homogeneous=True,spacing=2)
        self.titulo= gtk.Image()
        self.titulo.set_from_file("titulo.png")
        self.label = gtk.Label("Segunda práctica de Paradigmas de Programacion\nAutores: Javier Gaton Herguedas y Juan Gatón Herguedas\n")
        self.botonfacil = gtk.Button("Principiante. 9x9 9 minas")
        self.botonfacil.connect("clicked", self.partida,(0,9,9,9))
        self.botonmedio = gtk.Button("Intermedio. 16x16 40 minas")
        self.botonmedio.connect("clicked", self.partida,(0,16,16,40))
        self.botondif = gtk.Button("Experto. 16x30 99 minas")
        self.botondif.connect("clicked", self.partida,(0,16,30,99))
        self.botonleer = gtk.Button("Leer tablero")
        self.botonleer.connect("clicked", self.leer)
        self.nombrefich=gtk.Label("Ningun archivo seleccionado")

        self.botonsalir = gtk.Button("SALIR")
        self.botonsalir.connect("clicked", self.destruye)
        
        
        self.tabla.pack_start(self.label)
        self.tabla.pack_start(self.botonfacil)
        self.tabla.pack_start(self.botonmedio)
        self.tabla.pack_start(self.botondif)
        self.tabla.pack_start(self.botonleer)
        self.tabla.pack_start(self.botonsalir)

        self.tablarod=gtk.HBox()
        self.labelaux1=gtk.Label()
        self.labelaux2=gtk.Label()
        self.tablarod.pack_start(self.labelaux1)
        self.tablarod.pack_start(self.tabla)
        self.tablarod.pack_start(self.labelaux2)
        
        self.tablasup=gtk.VBox()
        self.tablasup.pack_start(self.titulo)
        self.tablasup.pack_start(self.tablarod)
        self.ventana.add(self.tablasup)
        self.ventana.show_all()
        return None

    def main(self):
        gtk.main()
        return (self.select,self.nfila,self.ncolumn,self.nbomb,self.nombrefich.get_text())
#MAIN


if __name__ == "__main__" :
    nfilas=30
    ncolumnas=9
    nbomb=15
    select=0
    busca = buscaminas()
    while select!=2:
        busca.ventana.show_all()
        result=busca.main()
        busca.ventana.hide_all()
        select=result[0]
        nfila=result[1]
        ncolumn=result[2]
        nbomb=result[3]
        if select==0:
            Tab=Tablero(nfila,ncolumn,nbomb,False)
            Tab.main()
            del Tab
        elif select==1:
            Tab=Tablero(nfila,ncolumn,result[4],True)
            Tab.main()
            del Tab
        