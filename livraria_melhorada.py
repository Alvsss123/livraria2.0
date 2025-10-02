
import tkinter as tk
from tkinter import ttk
import datetime
import random

# --- ESTRUTURA DE DADOS ---
catalogo = []
generos_validos = ["Ficcao","Romance", "Fantasia", "Terror", "Biografia", "Historia", "Comedia"]

# --- FUNÇÕES ---
def adicionar_livro():
    titulo = entry_titulo.get().strip()
    autor = entry_autor.get().strip()
    ano = entry_ano.get().strip()
    genero = entry_genero.get().strip()

    erros = []

    if not titulo:
        erros.append("O título não pode estar vazio.")
    if not autor:
        erros.append("O autor não pode estar vazio.")
    if not ano:
        erros.append("O ano não pode estar vazio.")
    else:
        try:
            ano_int = int(ano)
            ano_atual = datetime.datetime.now().year
            if ano_int < 1000 or ano_int > ano_atual:
                erros.append(f"O ano deve estar entre 1000 e {ano_atual}.")
        except ValueError:
            erros.append("O ano deve ser um número inteiro.")
    if not genero:
        erros.append("O gênero não pode estar vazio.")
    elif genero not in generos_validos:
        erros.append(f"Gênero inválido. Escolha entre: {', '.join(generos_validos)}")

    if erros:
        mostrar_feedback("\n".join(erros), tipo="erro")
        return

    novo_livro = {"titulo": titulo, "autor": autor, "ano": ano, "genero": genero}
    catalogo.append(novo_livro)
    atualizar_treeview(catalogo)
    atualizar_contador()
    mostrar_feedback("Livro adicionado com sucesso!", tipo="sucesso")

    entry_titulo.delete(0, tk.END)
    entry_autor.delete(0, tk.END)
    entry_ano.delete(0, tk.END)
    entry_genero.delete(0, tk.END)

def atualizar_treeview(lista_livros):
    for item in treeview.get_children():
        treeview.delete(item)
    for livro in lista_livros:
        treeview.insert("", "end", values=(livro["titulo"], livro["autor"], livro["ano"], livro["genero"]))

def buscar_livro():
    termo_busca = entry_busca.get().lower()
    resultados = []

    for item in treeview.get_children():
        treeview.delete(item)

    for livro in catalogo:
        if (termo_busca in livro["titulo"].lower() or
            termo_busca in livro["autor"].lower() or
            termo_busca in livro["ano"].lower()):
            resultados.append(livro)
            treeview.insert("", "end", values=(livro["titulo"], livro["autor"], livro["ano"], livro["genero"]), tags=("destaque",))

    contador_label.config(text=f"Resultados encontrados: {len(resultados)}")
    mostrar_feedback(f"{len(resultados)} resultado(s) encontrado(s).", tipo="info")
    treeview.tag_configure("destaque", background="lightyellow")

def ordenar_livros():
    catalogo.sort(key=lambda livro: livro["autor"])
    atualizar_treeview(catalogo)
    atualizar_contador()
    mostrar_feedback("Livros ordenados por autor.", tipo="info")

def remover_livro():
    item_selecionado = treeview.selection()
    if item_selecionado:
        livro_valores = treeview.item(item_selecionado, "values")
        for livro in catalogo:
            if (livro["titulo"], livro["autor"], livro["ano"], livro["genero"]) == livro_valores:
                catalogo.remove(livro)
                mostrar_feedback("Livro removido com sucesso!", tipo="sucesso")
                break
        atualizar_treeview(catalogo)
        atualizar_contador()
    else:
        mostrar_feedback("Nenhum livro selecionado para remoção.", tipo="erro")

def atualizar_contador():
    contador_label.config(text=f"Total de livros: {len(catalogo)}")

def mostrar_todos():
    atualizar_treeview(catalogo)
    atualizar_contador()
    mostrar_feedback("Exibindo todos os livros.", tipo="info")

def mostrar_feedback(mensagem, tipo="info"):
    cores = {
        "sucesso": "green",
        "erro": "red",
        "info": "blue"
    }
    feedback_label.config(text=mensagem, fg=cores.get(tipo, "black"))


def mostrar_livro_aleatorio():
    if not catalogo:
        mostrar_feedback("O catálogo está vazio.", tipo="erro")
        return
    livro = random.choice(catalogo)
    for item in treeview.get_children():
        treeview.delete(item)
    treeview.insert("", "end", values=(livro["titulo"], livro["autor"], livro["ano"], livro["genero"]), tags=("aleatorio",))
    treeview.tag_configure("aleatorio", background="lightblue")
    contador_label.config(text="Livro aleatório exibido.")
    mostrar_feedback("Livro aleatório exibido com sucesso!", tipo="info")

# --- INTERFACE GRÁFICA ---
janela = tk.Tk()
janela.title("Sistema de Livraria")
janela.geometry("850x600")

# Campos de entrada
label_titulo = tk.Label(janela, text="Título:")
label_titulo.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_titulo = tk.Entry(janela, width=30)
entry_titulo.grid(row=0, column=1, padx=5, pady=5)

label_autor = tk.Label(janela, text="Autor:")
label_autor.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_autor = tk.Entry(janela, width=30)
entry_autor.grid(row=1, column=1, padx=5, pady=5)

label_ano = tk.Label(janela, text="Ano:")
label_ano.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_ano = tk.Entry(janela, width=30)
entry_ano.grid(row=2, column=1, padx=5, pady=5)

label_genero = tk.Label(janela, text="Gênero:")
label_genero.grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_genero = tk.Entry(janela, width=30)
entry_genero.grid(row=3, column=1, padx=5, pady=5)

botao_adicionar = tk.Button(janela, text="Adicionar Livro", command=adicionar_livro, bg="green", fg="white")
botao_adicionar.grid(row=4, column=1, padx=5, pady=10)

# Widgets de busca e ações
label_busca = tk.Label(janela, text="Buscar:")
label_busca.grid(row=0, column=2, padx=10, pady=5, sticky="e")
entry_busca = tk.Entry(janela, width=30)
entry_busca.grid(row=0, column=3, padx=5, pady=5)

botao_buscar = tk.Button(janela, text="Buscar Livro", command=buscar_livro, bg="green", fg="white")
botao_buscar.grid(row=1, column=3, padx=5, pady=5)

botao_ordenar = tk.Button(janela, text="Ordenar por Autor", command=ordenar_livros, bg="green", fg="white")
botao_ordenar.grid(row=2, column=3, padx=5, pady=5)

botao_mostrar_todos = tk.Button(janela, text="Mostrar Todos", command=mostrar_todos, bg="green", fg="white")
botao_mostrar_todos.grid(row=3, column=2, padx=5, pady=5)

botao_remover = tk.Button(janela, text="Remover Livro", command=remover_livro, bg="green", fg="white")
botao_remover.grid(row=3, column=3, padx=5, pady=5)

botao_aleatorio = tk.Button(janela, text="Livro Aleatório", command=mostrar_livro_aleatorio, bg="green", fg="white")
botao_aleatorio.grid(row=4, column=3, padx=5, pady=10)

# Tabela (Treeview)
colunas = ("titulo", "autor", "ano", "genero")
treeview = ttk.Treeview(janela, columns=colunas, show="headings")
treeview.heading("titulo", text="Título")
treeview.heading("autor", text="Autor")
treeview.heading("ano", text="Ano")
treeview.heading("genero", text="Gênero")
treeview.column("titulo", width=250)
treeview.column("autor", width=150)
treeview.column("ano", width=80)
treeview.column("genero", width=120)
treeview.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Contador de livros
contador_label = tk.Label(janela, text="Total de livros: 0", font=("Arial", 12), fg="green")
contador_label.grid(row=6, column=0, columnspan=4, pady=10)

# Marcador de feedback
feedback_label = tk.Label(janela, text="", font=("Arial", 12))
feedback_label.grid(row=7, column=0, columnspan=4, pady=5)

# Redimensionamento
janela.grid_rowconfigure(5, weight=1)
janela.grid_columnconfigure(1, weight=1)
janela.grid_columnconfigure(3, weight=1)

janela.mainloop()

