from flask import Flask, g, render_template, flash, request, redirect
import sqlite3

DATABASE = "blog.bd"
SECRET_KEY = "pudim"

app = Flask(__name__)
app.config.from_object(__name__)

# funcao para conectar no banco
def conectar_bd():
    return sqlite3.connect(DATABASE)

#conecta no banco sempre que chagar uma requisicao
@app.before_request
def antes_requisicao():
    g.bd = conectar_bd()

#desconectar depois que terminar de usar o banco
@app.teardown_request
def fim_requisicao(exc):
    g.bd.close()

@app.route('/')
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    for titulo, texto in cur.fetchall():
        entradas.append({
            "titulo": titulo,
            "texto": texto
            })

    #return str(entradas)
    return render_template("exibir_entradas.html", posts=entradas)

@app.route('/inserir', methods=['POST'])
def inserir_entrada():
    sql = "INSERT INTO entradas(titulo, texto) VALUES (?, ?);"
    titulo = request.form['titulo']
    texto = request.form['texto']
    g.bd.execute(sql, [titulo, texto])
    g.bd.commit()
    return redirect('/')