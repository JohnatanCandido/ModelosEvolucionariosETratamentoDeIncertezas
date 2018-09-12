from tkinter import Tk, Canvas, ttk, Entry, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import programacao_genetica as pg
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import tkinter as tk


matplotlib.use("TkAgg")

master = Tk()
master.title('Programação Genética')
top_frame = Frame(master)
top_frame.pack(side=tk.TOP)
bottom_frame = Frame(master)
bottom_frame.pack(side=tk.BOTTOM)
right_frame = Frame(bottom_frame)
right_frame.pack(side=tk.RIGHT)
left_frame = Frame(bottom_frame)
left_frame.pack(side=tk.LEFT)
left_top_frame = Frame(left_frame)
left_top_frame.pack(side=tk.TOP)
left_bottom_frame = Frame(left_frame)
left_bottom_frame.pack(side=tk.BOTTOM)

button = ttk.Button(top_frame, text='Executar', command=lambda: executa())
button.pack(side=tk.LEFT)

f = Figure(figsize=(5, 5), dpi=100)
sp = f.add_subplot(111)

canvas = FigureCanvasTkAgg(f, right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

label_num_ger = ttk.Label(left_top_frame, text='Número de Gerações')
label_num_ger.pack(side=tk.TOP)
num_ger = ttk.Entry(left_top_frame)
num_ger.pack(side=tk.TOP)

label_tam_ger = ttk.Label(left_top_frame, text='Tamanho da Geração')
label_tam_ger.pack(side=tk.TOP)
tam_ger = ttk.Entry(left_top_frame)
tam_ger.pack(side=tk.TOP)

label_max_prof = ttk.Label(left_top_frame, text='Profundidade Máxima')
label_max_prof.pack(side=tk.TOP)
max_prof = ttk.Entry(left_top_frame)
max_prof.pack(side=tk.TOP)

label_chan_mut = ttk.Label(left_top_frame, text='Chance de mutação')
label_chan_mut.pack(side=tk.TOP)
chan_mut = ttk.Entry(left_top_frame)
chan_mut.pack(side=tk.TOP)

espacador1 = ttk.Label(left_top_frame)
espacador1.pack(side=tk.BOTTOM)


dados1 = ttk.Label(top_frame)
dados2 = ttk.Label(top_frame)
esp = ttk.Label(top_frame, text='   ')
esp.pack(side=tk.LEFT)
dados1.pack(side=tk.LEFT)
dados2.pack(side=tk.RIGHT)

espacador2 = ttk.Label(left_bottom_frame, text='    ')
espacador2.pack(side=tk.LEFT)

resultado = ttk.Treeview(left_bottom_frame, columns=('Num', 'Obtido    Esperado'))
resultado.heading('#0', text='Num', anchor=tk.CENTER)
resultado.heading('#1', text='Obtido', anchor=tk.CENTER)
resultado.heading('#2', text='Esperado', anchor=tk.CENTER)
resultado.column('#0', stretch=tk.NO, minwidth=50, width=50)
resultado.column('#1', stretch=tk.NO, minwidth=75, width=75)
resultado.column('#2', stretch=tk.NO, minwidth=75, width=75)
resultado.pack(side=tk.LEFT)

espacador3 = ttk.Label(left_bottom_frame, text='    ')
espacador3.pack(side=tk.LEFT)


def executa():
    dados1.config(text='Calculando...')
    dados2.config(text='')
    resultado.delete(*resultado.get_children())
    sp.clear()
    canvas.show()

    ng = num_ger.get() if num_ger.get() != '' else '250'
    tg = tam_ger.get() if tam_ger.get() != '' else '100'
    mpf = max_prof.get() if max_prof.get() != '' else '5'
    cm = chan_mut.get() if chan_mut.get() != '' else '0.5'
    solucao = pg.main(ng, tg, mpf, cm)

    dados1.config(text=str(solucao).split(' - ')[0])
    dados2.config(text=str(solucao).split(' - ')[1])
    print(f'\nFunção:  {solucao.funcao}')
    print(f'Profundidade: {pg.calc_prof(solucao)}')
    print(f'Fitness: {solucao.fitness}')
    print(f'Geração: {solucao.geracao}')
    printa_resultados(solucao)


def printa_resultados(ind):
    print('|-------------------------|')
    print('| Num | Obtido | Esperado |')
    print('|-------------------------|')
    num = [par[0] for par in pg.pares]
    esperado = [par[1] for par in pg.pares]
    obtidos = []
    for par in pg.pares:
        r = float(eval(ind.funcao.replace('x', str(par[0]))))
        print('| {:2d}  | {:6.2f} | {:6.2f}   |'.format(par[0], r, par[1]))
        resultado.insert('', 'end', text=str(par[0]), values=(str(r)[:5], str(par[1])))
        obtidos.append(r)
    print('|-------------------------|')

    red_patch = mp.Patch(color='red', label='Resultados Obtidos')
    blue_patch = mp.Patch(color='blue', label='Resultados Esperados')
    sp.legend(handles=[red_patch, blue_patch])
    sp.plot(num, obtidos, color='red', marker='o', markerfacecolor='red')
    sp.plot(num, esperado, color='blue', marker='o', markerfacecolor='blue')
    canvas.show()


if __name__ == '__main__':
    master.mainloop()
