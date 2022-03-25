from datetime import datetime, timedelta
from math import sin,cos,pi
import sys
import os
import json
from tkinter import *

# Nao sei fazer relogio dinamico resize, porem quando muda o valor de height e width na declaracao do Canvas,
# ele se ajusta automatico, porem nao sei porque, nao aceita valores maiores que 1000 para height and width.

#  @author Gabriel Bittencourt de Souza Pinto

class Clock:
    def __init__(self,Tk):
        self.Tk = Tk
        self.delta = -3
        self.city = self.get_city_from_offset()
        self.today = datetime.now().strftime('%d/%m/%Y')
        self.clockCanvas = Canvas(Tk,bg='black',height=1000,width=1000)
        self.clockCanvas.pack()
        self.draw_everything()
        self.poll()

    # Retorna o width e height atual do Canvas
    # @return dois valores width e height
    def current_w_h(self):
        self.clockCanvas.update()
        w = self.clockCanvas.winfo_width()
        h = self.clockCanvas.winfo_height()
        return w,h

    # Retorna cidade do UTC fornecido pelo self.delta
    # @return string da cidade
    def get_city_from_offset(self):
        self.places = []
        f = open('./localtime.json', 'r')
        data = json.load(f)
        for c in data['cities']:
            self.places.append((c['city'], c['offset']))
        for i in self.places:
            if i[1] == self.delta:
                return i[0]

    ## Converte um vetor de coordenadas polares para cartesianas.
    # @param angle angulo do vetor.
    # @param radius comprimento do vetor.
    # @return um ponto 2D.
    def polar2cartesian(self,angle,radius=1):
        angle = pi/2 - angle
        return (radius*cos(angle),radius*sin(angle))

    # Desenha os ponteiros
    # @param angle angulo do vetor
    # @param len comprimento do ponteiro
    # @param wid grossura do ponteiro
    def draw_handle(self,angle,len,wid=None):
        x,y = self.polar2cartesian(angle,len)

        w,h = self.current_w_h()

        self.clockCanvas.create_line(w/2,h/2,w/2+x,h/2-y,fill='white',tag='handles',width=wid,capstyle=ROUND)


    # Desenha o oval do relogio
    # Desenha os pontinhos marcando hora e minutos
    # Desenha informacao UTC no canto inferior direito
    def draw_everything(self):
        w,h = self.current_w_h()

        self.clockCanvas.create_oval(1/100*w, 1/100*w, 99/100*h, 99/100*h, outline="white")

        segundos = 60
        horas = 12

        for i in range(horas):
            x,y = self.polar2cartesian((pi/6)*i,w/2-10)
            self.clockCanvas.create_line(w/2+0.85*x,h/2-0.85*y,w/2+x,h/2-y,fill="pink",width=3)
            tx,ty = self.polar2cartesian((pi/6)*i,w/2-110)
            if i == 0:
                i = 12
            self.clockCanvas.create_text(w/2+tx,h/2-ty,fill="pink",font="Times 30 bold",text=i)

        for i in range(segundos):
            x,y = self.polar2cartesian((pi/30)*i,w/2-10)
            self.clockCanvas.create_line(w/2+0.95*x,h/2-0.95*y,w/2+x,h/2-y,fill="pink",width=3)

        self.clockCanvas.create_text(92/100*w,88/100*h,fill="white",font="Times 30 bold",text="UTC "+str(self.delta))
        self.clockCanvas.create_text(90/100*w,92/100*h,fill="white",font="Times 30 bold",text=str(self.city))
        self.clockCanvas.create_text(90/100*w,97/100*h,fill="white",font="Times 30 bold",text=self.today)

    # Deleta ponteiros atuais
    # Pega h,m,s atual e usa na funcao para desenhar novos ponteiros
    def paint_hms(self):
        self.clockCanvas.delete('handles')


        h,m,s = datetime.timetuple(datetime.utcnow()+timedelta(hours=self.delta))[3:6]

        hUTC = h+(self.delta*-1)

        oneMin = pi/30
        fiveMin = pi/6

        hora = fiveMin*(h+m/60)
        horaUTC = fiveMin*(hUTC+m/60)
        minutos = oneMin*(m+s/60)
        segundos = oneMin*s

        w,h = self.current_w_h()

        self.draw_handle(hora,(w/4)*0.8,10)
        self.draw_handle(minutos,(w/2)*0.9,10)
        self.draw_handle(segundos,(w/2)*0.95,3.6)
        self.draw_handle(horaUTC,(w/2)*0.98,0.9)

    # Desenha os ponteiros em loop
    def poll(self):
        self.paint_hms()
        self.Tk.after(200,self.poll)


Main = Tk()
Clock(Main)
Main.mainloop()