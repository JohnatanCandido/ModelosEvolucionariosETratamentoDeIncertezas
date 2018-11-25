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
labels = {}
sub_plots = {}
canvases = {}


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


def adiciona_frame(nome_elemento=None):
    if nome_elemento is None:
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

        labels[nome_elemento] = label_nome_elemento
        valores[nome_elemento] = valor_elemento
        sub_plots[nome_elemento] = sp
        canvases[nome_elemento] = canvas


def remove_frame(nome_elemento, frame):
    controller.remove_elemento(nome_elemento)
    labels[nome_elemento].destroy()
    valores[nome_elemento].destroy()
    frame.destroy()


def add_variavel(elemento, nome, suporte, nucleo, sp, canvas, auto=False):
    if auto:
        controller.add_variavel(elemento, nome, suporte, nucleo)
    else:
        controller.add_variavel(elemento, nome.get(), suporte.get(), nucleo.get())

    patches = []
    i = 0
    for nome_var in controller.elementos[elemento].variaveis:
        variavel = controller.elementos[elemento].variaveis[nome_var]
        patches.append(mp.Patch(color=cores[i], label=variavel.nome))
        x = [variavel.suporte[0], variavel.nucleo[0], variavel.nucleo[1], variavel.suporte[1]]
        sp.plot(x, [0, 1, 1, 0], color=cores[i])
        i += 1
    sp.legend(handles=patches)
    canvas.show()

    if not auto:
        nome.delete(0, 'end')
        suporte.delete(0, 'end')
        nucleo.delete(0, 'end')


def add_regra(regra=None, res=None):
    if regra is None:
        regra = valor_regra.get()
    if ' e ' in regra and ' ou ' in regra:
        return
    if res is None:
        res = valor_entao.get()

    controller.regras.append([regra, res])
    tabela_regras.insert('', 'end', text=len(controller.regras), values=['Se ' + regra + ' então ' + res])
    valor_regra.delete(0, 'end')
    valor_entao.delete(0, 'end')


def inserir_valores_exercicio():
    adiciona_frame('potencia')
    add_variavel('potencia', 'pouco potente', '0,120', '0,100', sub_plots['potencia'], canvases['potencia'], True)
    add_variavel('potencia', 'medio', '100,180', '120,160', sub_plots['potencia'], canvases['potencia'], True)
    add_variavel('potencia', 'potente', '160,220', '180,220', sub_plots['potencia'], canvases['potencia'], True)

    adiciona_frame('peso')
    add_variavel('peso', 'leve', '0,3000', '0,2500', sub_plots['peso'], canvases['peso'], True)
    add_variavel('peso', 'medio', '2500,4000', '3000,3600', sub_plots['peso'], canvases['peso'], True)
    add_variavel('peso', 'pesado', '3600,5000', '4000,5000', sub_plots['peso'], canvases['peso'], True)

    adiciona_frame('aceleração')
    add_variavel('aceleração', 'lento', '0,15', '0,12', sub_plots['aceleração'], canvases['aceleração'], True)
    add_variavel('aceleração', 'medio', '12,21', '15,18', sub_plots['aceleração'], canvases['aceleração'], True)
    add_variavel('aceleração', 'rapido', '19,24', '21,24', sub_plots['aceleração'], canvases['aceleração'], True)

    adiciona_frame('consumo')
    add_variavel('consumo', 'economico', '10,25', '10,20', sub_plots['consumo'], canvases['consumo'], True)
    add_variavel('consumo', 'medio', '20,35', '25,30', sub_plots['consumo'], canvases['consumo'], True)
    add_variavel('consumo', 'não economico', '30,45', '35,45', sub_plots['consumo'], canvases['consumo'], True)

    add_regra('potencia é potente e peso é pesado e aceleração é lento', 'consumo é não economico')
    add_regra('potencia é pouco potente e peso é leve e aceleração é rapido', 'consumo é economico')
    add_regra('potencia é pouco potente e peso é pesado e aceleração é medio', 'consumo é medio')
    add_regra('potencia é potente e peso é medio e aceleração é lento', 'consumo é medio')
    add_regra('potencia é potente e peso é medio e aceleração é medio', 'consumo é medio')


def inserir_valores_exemplo():
    adiciona_frame('QI')
    add_variavel('QI', 'Baixo', '0,90', '0,49', sub_plots['QI'], canvases['QI'], True)
    add_variavel('QI', 'Medio', '49,150', '90, 109', sub_plots['QI'], canvases['QI'], True)
    add_variavel('QI', 'Alto', '109, 200', '150,200', sub_plots['QI'], canvases['QI'], True)

    adiciona_frame('Idade')
    add_variavel('Idade', 'Jovem', '0,25', '0,18', sub_plots['Idade'], canvases['Idade'], True)
    add_variavel('Idade', 'Adulto', '18,70', '25, 50', sub_plots['Idade'], canvases['Idade'], True)
    add_variavel('Idade', 'Idoso', '50,100', '70,100', sub_plots['Idade'], canvases['Idade'], True)

    adiciona_frame('Contratar')
    add_variavel('Contratar', 'Não', '0,40', '0,15', sub_plots['Contratar'], canvases['Contratar'], True)
    add_variavel('Contratar', 'Talvez', '15,90', '40, 60', sub_plots['Contratar'], canvases['Contratar'], True)
    add_variavel('Contratar', 'Sim', '60, 100', '90,100', sub_plots['Contratar'], canvases['Contratar'], True)

    add_regra('QI é Baixo e Idade é Jovem', 'Contratar é Não')
    add_regra('QI é Medio e Idade é Jovem', 'Contratar é Não')
    add_regra('QI é Alto e Idade é Jovem', 'Contratar é Talvez')

    add_regra('QI é Baixo e Idade é Adulto', 'Contratar é Não')
    add_regra('QI é Medio e Idade é Adulto', 'Contratar é Talvez')
    add_regra('QI é Alto e Idade é Adulto', 'Contratar é Sim')

    add_regra('QI é Baixo e Idade é Idoso', 'Contratar é Não')
    add_regra('QI é Medio e Idade é Idoso', 'Contratar é Talvez')
    add_regra('QI é Alto e Idade é Idoso', 'Contratar é Talvez')


# inserir_valores_exercicio()
inserir_valores_exemplo()
main.mainloop()
