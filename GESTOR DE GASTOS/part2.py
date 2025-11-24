import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import json
import os

from GESTORDEGASTOS import (
    carregar_dados,
    salvar_dados,
    adicionar,
    remover,
    listar_cat,
    listar_periodo,
    saldo_periodo
)

USERS_FILE = "users.json"


def carregar_usuarios():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}

    with open(USERS_FILE, "r") as f:
        return json.load(f)


def salvar_usuarios(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


def cadastrar_usuario(username, senha):
    users = carregar_usuarios()

    if username in users:
        return False

    users[username] = senha
    salvar_usuarios(users)
    return True


def validar_login(username, senha):
    users = carregar_usuarios()
    return username in users and users[username] == senha




def janela_login():
    login = tk.Tk()
    login.title("Login - Sistema Financeiro")

    tk.Label(login, text="Usuário").grid(row=0, column=0)
    e_usuario = tk.Entry(login)
    e_usuario.grid(row=0, column=1)

    tk.Label(login, text="Senha").grid(row=1, column=0)
    e_senha = tk.Entry(login, show="*")
    e_senha.grid(row=1, column=1)

    def fazer_login():
        user = e_usuario.get().strip()
        senha = e_senha.get().strip()

        if validar_login(user, senha):
            messagebox.showinfo("OK", "Login realizado com sucesso!")
            login.destroy()
            janela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    def fazer_cadastro():
        user = e_usuario.get().strip()
        senha = e_senha.get().strip()

        if cadastrar_usuario(user, senha):
            messagebox.showinfo("OK", "Usuário cadastrado!")
        else:
            messagebox.showerror("Erro", "Usuário já existe!")

    tk.Button(login, text="Login", command=fazer_login).grid(row=3, column=0)
    tk.Button(login, text="Cadastrar", command=fazer_cadastro).grid(row=3, column=1)

    login.mainloop()


def janela_principal():
    df = carregar_dados()

    root = tk.Tk()
    root.title("Controle Financeiro - Sistema Completo")


    def func_adicionar():
        nonlocal df
        data = e_data.get()
        tipo = e_tipo.get()
        cat = e_cat.get()
        desc = e_desc.get()
        valor = float(e_valor.get())

        nova = {
            "Data": data,
            "Tipo": tipo,
            "Categoria": cat,
            "Descricao": desc,
            "Valor": valor
        }

        df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
        salvar_dados(df)
        messagebox.showinfo("OK", "Transação adicionada!")

    def func_remover():
        nonlocal df
        idx = int(e_id_remover.get())
        df = df.drop(index=idx).reset_index(drop=True)
        salvar_dados(df)
        messagebox.showinfo("OK", "Transação removida!")

    def func_exportar():
        caminho = filedialog.asksaveasfilename(defaultextension=".csv")
        if caminho:
            df.to_csv(caminho, index=False)
            messagebox.showinfo("OK", "Exportado com sucesso!")



    tk.Label(root, text="Data (dd/mm/aaaa)").grid(row=0, column=0)
    e_data = tk.Entry(root); e_data.grid(row=0, column=1)

    tk.Label(root, text="Tipo (entrada/saida)").grid(row=1, column=0)
    e_tipo = tk.Entry(root); e_tipo.grid(row=1, column=1)

    tk.Label(root, text="Categoria").grid(row=2, column=0)
    e_cat = tk.Entry(root); e_cat.grid(row=2, column=1)

    tk.Label(root, text="Descrição").grid(row=3, column=0)
    e_desc = tk.Entry(root); e_desc.grid(row=3, column=1)

    tk.Label(root, text="Valor").grid(row=4, column=0)
    e_valor = tk.Entry(root); e_valor.grid(row=4, column=1)

    tk.Button(root, text="Adicionar Transação", command=func_adicionar).grid(row=5, column=0, columnspan=2)


    tk.Label(root, text="ID para remover:").grid(row=6, column=0)
    e_id_remover = tk.Entry(root); e_id_remover.grid(row=6, column=1)
    tk.Button(root, text="Remover", command=func_remover).grid(row=7, column=0, columnspan=2)


    tk.Button(root, text="Exportar CSV", command=func_exportar).grid(row=8, column=0, columnspan=2)

    root.mainloop()


janela_login()
