from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar():
    return sqlite3.connect("database.db")

def criar_banco():
    conn=conectar()
    c=conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT,telefone TEXT,endereco TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS produtos(id INTEGER PRIMARY KEY AUTOINCREMENT,nome TEXT,preco REAL,tipo TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS pedidos(id INTEGER PRIMARY KEY AUTOINCREMENT,produto TEXT,quantidade INTEGER,status TEXT)")
    conn.commit(); conn.close()

def inserir_produtos_iniciais():
    conn=conectar(); c=conn.cursor()
    c.execute("SELECT COUNT(*) FROM produtos")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO produtos(nome,preco,tipo) VALUES (?,?,?)",[('Calabresa',45.9,'Pizza'),('Frango com Catupiry',49.9,'Pizza'),('Bacon',52.9,'Pizza')])
    conn.commit(); conn.close()

criar_banco()
inserir_produtos_iniciais()

@app.route('/')
def home():
    return redirect('/cardapio')

@app.route('/cardapio')
def cardapio():
    conn=conectar(); c=conn.cursor(); c.execute('SELECT * FROM produtos'); produtos=c.fetchall(); conn.close()
    return render_template('cardapio.html', produtos=produtos)

@app.route('/carrinho/<int:id>')
def carrinho(id):
    conn=conectar(); c=conn.cursor(); c.execute('SELECT * FROM produtos WHERE id=?',(id,)); produto=c.fetchone(); conn.close()
    return render_template('carrinho.html', produto=produto)

@app.route('/finalizar', methods=['POST'])
def finalizar():
    conn=conectar(); c=conn.cursor()
    c.execute('INSERT INTO pedidos(produto,quantidade,status) VALUES (?,?,?)',(request.form['produto'],request.form['quantidade'],'Recebido'))
    conn.commit(); conn.close()
    return redirect('/pedidos')

@app.route('/cliente')
def cliente():
    return render_template('cadastro_cliente.html')

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    conn=conectar(); c=conn.cursor()
    c.execute('INSERT INTO clientes(nome,telefone,endereco) VALUES (?,?,?)',(request.form['nome'],request.form['telefone'],request.form['endereco']))
    conn.commit(); conn.close()
    return redirect('/cardapio')

@app.route('/pedidos')
def pedidos():
    conn=conectar(); c=conn.cursor(); c.execute('SELECT * FROM pedidos'); pedidos=c.fetchall(); conn.close()
    return render_template('pedidos.html', pedidos=pedidos)

@app.route('/produtos')
def produtos():
    conn=conectar(); c=conn.cursor(); c.execute('SELECT * FROM produtos'); produtos=c.fetchall(); conn.close()
    return render_template('cadastro_produtos.html', produtos=produtos)

@app.route('/salvar_produto', methods=['POST'])
def salvar_produto():
    conn=conectar(); c=conn.cursor()
    c.execute('INSERT INTO produtos(nome,preco,tipo) VALUES (?,?,?)',(request.form['nome'],request.form['preco'],request.form['tipo']))
    conn.commit(); conn.close()
    return redirect('/produtos')

if __name__ == '__main__':
    app.run(debug=True)
