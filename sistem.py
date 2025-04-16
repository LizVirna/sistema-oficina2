import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk


# Conexão com banco de dados
conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT,
        telefone TEXT,
        endereco TEXT,
        modelo_carro TEXT,
        placa TEXT,
        observacoes TEXT
    )
''')
conn.commit()

# Funções
def cadastrar_cliente():
    dados = (
        entry_nome.get(),
        entry_cpf.get(),
        entry_telefone.get(),
        entry_endereco.get(),
        entry_modelo.get(),
        entry_placa.get(),
        entry_obs.get("1.0", 'end').strip()
    )
    if dados[0] == "" or dados[5] == "":
        messagebox.showwarning("Atenção", "Preencha pelo menos o nome e a placa.")
        return
    cursor.execute('''
        INSERT INTO clientes (nome, cpf, telefone, endereco, modelo_carro, placa, observacoes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    limpar_campos()
    listar_clientes()
    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

def listar_clientes():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute('SELECT * FROM clientes')
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def buscar_clientes():
    termo = entry_busca.get()
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT * FROM clientes WHERE nome LIKE ? OR placa LIKE ?", (f'%{termo}%', f'%{termo}%'))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

def excluir_cliente():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
        return
    cliente_id = tree.item(item[0])['values'][0]
    cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    listar_clientes()
    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

def preencher_campos(event):
    item = tree.selection()
    if item:
        valores = tree.item(item[0])['values']
        entry_nome.delete(0, 'end')
        entry_cpf.delete(0, 'end')
        entry_telefone.delete(0, 'end')
        entry_endereco.delete(0, 'end')
        entry_modelo.delete(0, 'end')
        entry_placa.delete(0, 'end')
        entry_obs.delete("1.0", 'end')

        entry_nome.insert(0, valores[1])
        entry_cpf.insert(0, valores[2])
        entry_telefone.insert(0, valores[3])
        entry_endereco.insert(0, valores[4])
        entry_modelo.insert(0, valores[5])
        entry_placa.insert(0, valores[6])
        entry_obs.insert('end', valores[7])

def atualizar_cliente():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um cliente para atualizar.")
        return
    cliente_id = tree.item(item[0])['values'][0]
    dados = (
        entry_nome.get(),
        entry_cpf.get(),
        entry_telefone.get(),
        entry_endereco.get(),
        entry_modelo.get(),
        entry_placa.get(),
        entry_obs.get("1.0", 'end').strip(),
        cliente_id
    )
    cursor.execute('''
        UPDATE clientes
        SET nome = ?, cpf = ?, telefone = ?, endereco = ?, modelo_carro = ?, placa = ?, observacoes = ?
        WHERE id = ?
    ''', dados)
    conn.commit()
    listar_clientes()
    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")

def limpar_campos():
    entry_nome.delete(0, 'end')
    entry_cpf.delete(0, 'end')
    entry_telefone.delete(0, 'end')
    entry_endereco.delete(0, 'end')
    entry_modelo.delete(0, 'end')
    entry_placa.delete(0, 'end')
    entry_obs.delete("1.0", 'end')

# Interface com ttkbootstrap
root = ttk.Window(title="Cadastro de Clientes - Oficina", themename="flatly", size=(1000, 700))

# Campo de busca
ttk.Label(root, text="Buscar (Nome ou Placa):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_busca = ttk.Entry(root)
entry_busca.grid(row=0, column=1, padx=5, pady=5, sticky="ew", columnspan=2)
ttk.Button(root, text="Buscar", command=buscar_clientes, bootstyle="info").grid(row=0, column=3, padx=5)
ttk.Button(root, text="Mostrar Todos", command=listar_clientes, bootstyle="secondary").grid(row=0, column=4, padx=5)

# Campos de entrada
labels = ["Nome", "CPF", "Telefone", "Endereço", "Modelo do Carro", "Placa", "Observações"]
widgets = []

entry_nome = ttk.Entry(root)
entry_cpf = ttk.Entry(root)
entry_telefone = ttk.Entry(root)
entry_endereco = ttk.Entry(root)
entry_modelo = ttk.Entry(root)
entry_placa = ttk.Entry(root)
entry_obs = tk.Text(root, height=4)

campos = [
    ("Nome", entry_nome),
    ("CPF", entry_cpf),
    ("Telefone", entry_telefone),
    ("Endereço", entry_endereco),
    ("Modelo do Carro", entry_modelo),
    ("Placa", entry_placa),
    ("Observações", entry_obs),
]

for i, (label, widget) in enumerate(campos):
    ttk.Label(root, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky='e')
    if isinstance(widget, tk.Text):
        widget.grid(row=i+1, column=1, columnspan=4, sticky="ew", padx=5)
    else:
        widget.grid(row=i+1, column=1, columnspan=4, sticky="ew", padx=5)

# Botões principais
frame_botoes = ttk.Frame(root)
frame_botoes.grid(row=8, column=0, columnspan=5, pady=10)
ttk.Button(frame_botoes, text="Cadastrar", command=cadastrar_cliente, bootstyle="success").grid(row=0, column=0, padx=5)
ttk.Button(frame_botoes, text="Atualizar", command=atualizar_cliente, bootstyle="warning").grid(row=0, column=1, padx=5)
ttk.Button(frame_botoes, text="Excluir", command=excluir_cliente, bootstyle="danger").grid(row=0, column=2, padx=5)
ttk.Button(frame_botoes, text="Limpar", command=limpar_campos, bootstyle="secondary").grid(row=0, column=3, padx=5)

# Tabela
tree = ttk.Treeview(root, columns=('ID', 'Nome', 'CPF', 'Telefone', 'Endereço', 'Modelo', 'Placa', 'Obs'), show='headings', height=10, bootstyle="primary")
for col in tree['columns']:
    tree.heading(col, text=col)
tree.grid(row=9, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")
tree.bind('<<TreeviewSelect>>', preencher_campos)

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=9, column=5, sticky='ns')

# Layout responsivo
for i in range(5):
    root.columnconfigure(i, weight=1)
root.rowconfigure(9, weight=1)

listar_clientes()
root.mainloop()
