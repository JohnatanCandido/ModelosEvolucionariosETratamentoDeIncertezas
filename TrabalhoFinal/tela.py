from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TrabalhoFinal import controller
from matplotlib.figure import Figure
from tkinter import Tk, ttk, Frame
import matplotlib.patches as mp
import tkinter as tk

cores = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']

main = Tk()
main.title('Modelos Difusos')
main.geometry('510x600')

nb = ttk.Notebook(main)


nb.grid(row=0, column=0, rowspan=49, sticky='NSEW')

main_page = ttk.Frame(nb)
nb.add(main_page, text='Principal')

top_frame = Frame(main_page)
top_frame.pack(side=tk.TOP)

bottom_frame = Frame(main_page)
bottom_frame.pack(side=tk.TOP)

top_left_frame = Frame(top_frame)
top_left_frame.pack(side=tk.LEFT)

label_elemento = ttk.Label(top_left_frame, text='Elemento')
label_elemento.pack(side=tk.TOP)
valor_nome_elemento = ttk.Entry(top_left_frame)
valor_nome_elemento.pack(side=tk.TOP)

top_right_frame = Frame(top_frame)
top_right_frame.pack(side=tk.RIGHT)

botao_adicionar_elemento = ttk.Button(top_right_frame, text='Adicionar', command=lambda: adiciona_frame())
botao_adicionar_elemento.pack(side=tk.TOP)

label_resultado = ttk.Label(bottom_frame, text='-')
botao_calc = ttk.Button(bottom_frame, text='Calcular', command=lambda: controller.calcular(valores, label_resultado))
botao_calc.pack(side=tk.TOP)
label_resultado.pack(side=tk.TOP)
spacer = ttk.Label(bottom_frame)
spacer.pack(side=tk.TOP)

valores = {}


# =====================================================================================================================

page_regras = ttk.Frame(nb)
regra_top_frame = Frame(page_regras)
regra_top_frame.pack(side=tk.TOP)
nb.add(page_regras, text='Regras')
label_regra = ttk.Label(regra_top_frame, text='Se ')
label_regra.pack(side=tk.LEFT)
valor_regra = ttk.Entry(regra_top_frame)
valor_regra.pack(side=tk.LEFT)

label_entao = ttk.Label(regra_top_frame, text=' então ')
label_entao.pack(side=tk.LEFT)
valor_entao = ttk.Entry(regra_top_frame)
valor_entao.pack(side=tk.LEFT)

botao_add_regra = ttk.Button(regra_top_frame, text='Adicionar', command=lambda: add_regra())
botao_add_regra.pack(side=tk.LEFT)

regra_bottom_frame = Frame(page_regras)
regra_bottom_frame.pack(side=tk.TOP)

tabela_regras = ttk.Treeview(regra_bottom_frame, columns=2)
tabela_regras.heading('#0', text='#', anchor=tk.CENTER)
tabela_regras.heading('#1', text='Regras', anchor=tk.CENTER)
tabela_regras.column('#0', stretch=tk.NO, minwidth=50, width=50)
tabela_regras.column('#1', stretch=tk.NO, minwidth=450, width=450)
tabela_regras.pack(side=tk.TOP)


def adiciona_frame():
    nome_elemento = valor_nome_elemento.get()
    if nome_elemento != '':
        controller.add_elemento(nome_elemento)

        valor_nome_elemento.delete(0, 'end')

        nova_aba = ttk.Frame(nb)
        nb.add(nova_aba, text=nome_elemento)

        top_frame_aba = Frame(nova_aba)
        top_frame_aba.pack(side=tk.TOP)

        botao_remover = ttk.Button(top_frame_aba, text='Remover', command=lambda: remove_frame(nome_elemento, nova_aba))
        botao_remover.pack(side=tk.LEFT)

        middle_frame_aba = Frame(nova_aba)
        middle_frame_aba.pack(side=tk.TOP)

        middle_left_frame_aba = Frame(middle_frame_aba)
        middle_left_frame_aba.pack(side=tk.LEFT)

        label_variavel = ttk.Label(middle_left_frame_aba, text='Variavel')
        label_variavel.pack(side=tk.TOP)
        valor_variavel = ttk.Entry(middle_left_frame_aba)
        valor_variavel.pack(side=tk.TOP)

        middle_middle_frame_aba = Frame(middle_frame_aba)
        middle_middle_frame_aba.pack(side=tk.LEFT)

        label_suporte = ttk.Label(middle_middle_frame_aba, text='Suporte')
        label_suporte.pack(side=tk.TOP)
        valor_suporte = ttk.Entry(middle_middle_frame_aba)
        valor_suporte.pack(side=tk.TOP)

        middle_right_frame_aba = Frame(middle_frame_aba)
        middle_right_frame_aba.pack(side=tk.LEFT)

        label_nucleo = ttk.Label(middle_right_frame_aba, text='Nucleo')
        label_nucleo.pack(side=tk.TOP)
        valor_nucleo = ttk.Entry(middle_right_frame_aba)
        valor_nucleo.pack(side=tk.TOP)

        botton_frame_aba = Frame(nova_aba)
        botton_frame_aba.pack(side=tk.TOP)

        f = Figure(figsize=(5, 5), dpi=100)
        sp = f.add_subplot(111)

        canvas = FigureCanvasTkAgg(f, botton_frame_aba)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        botao_adicionar = ttk.Button(middle_frame_aba, text='Adicionar', command=lambda: add_variavel(nome_elemento,
                                                                                                      valor_variavel,
                                                                                                      valor_suporte,
                                                                                                      valor_nucleo,
                                                                                                      sp, canvas))

        canvas.show()
        botao_adicionar.pack(side=tk.BOTTOM)

        label_nome_elemento = ttk.Label(bottom_frame, text=nome_elemento)
        label_nome_elemento.pack(side=tk.TOP)
        valor_elemento = ttk.Entry(bottom_frame)
        valor_elemento.pack(side=tk.TOP)

        valores[nome_elemento] = valor_elemento


def remove_frame(nome_elemento, frame):
    controller.remove_elemento(nome_elemento)
    frame.destroy()


def add_variavel(elemento, nome, suporte, nucleo, sp, canvas):
    controller.add_variavel(elemento, nome.get(), suporte.get(), nucleo.get())

    patches = []
    i = 0
    for nome_var in controller.elementos[elemento].variaveis:
        variavel = controller.elementos[elemento].variaveis[nome_var]
        patches.append(mp.Patch(color=cores[i], label=variavel.nome))
        x = [variavel.suporte[0], variavel.nucleo[0], variavel.nucleo[1], variavel.suporte[1]]
        sp.plot(x, [0, 1, 1, 0], color=cores[i], marker='o', markerfacecolor=cores[i])
        i += 1
    sp.legend(handles=patches)
    canvas.show()

    nome.delete(0, 'end')
    suporte.delete(0, 'end')
    nucleo.delete(0, 'end')


def add_regra():
    regra = valor_regra.get()
    res = valor_entao.get()

    controller.regras.append([regra, res])
    tabela_regras.insert('', 'end', text=len(controller.regras), values=['Se ' + regra + ' então ' + res])
    valor_regra.delete(0, 'end')
    valor_entao.delete(0, 'end')


main.mainloop()
