from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import date
import json

app = Flask(__name__)
db = mysql.connector.connect(
    host="jobs.visie.com.br",
    user="luizesquivel",
    password="bHVpemVzcXVp",
    database="luizesquivel"
)
cursor = db.cursor(dictionary=True)
class Pessoa:
    def __init__(self, id_pessoa, nome, rg, cpf, data_nascimento, data_admissao, funcao):
        self.id_pessoa = id_pessoa
        self.nome = nome
        self.rg = rg
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.data_admissao = data_admissao
        self.funcao = funcao
@app.route("/pessoas", methods=["POST"])
def criar_pessoa():
    data = json.loads(request.data)
    nome = data["nome"]
    rg = data["rg"]
    cpf = data["cpf"]
    data_nascimento = data["data_nascimento"]
    data_admissao = data["data_admissao"]
    funcao = data.get("funcao", None)

    insert_query = "INSERT INTO pessoas (nome, rg, cpf, data_nascimento, data_admissao, funcao) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (nome, rg, cpf, data_nascimento, data_admissao, funcao)
    cursor.execute(insert_query, values)
    db.commit()
    pessoa_id = cursor.lastrowid
    return jsonify({"id_pessoa": pessoa_id}), 201
@app.route("/pessoas", methods=["GET"])
def listar_pessoas():
    query = "SELECT * FROM pessoas"
    cursor.execute(query)
    registros = cursor.fetchall()
    pessoas = []
    for registro in registros:
        pessoa = Pessoa(**registro)
        pessoas.append(pessoa.__dict__)
    return jsonify(pessoas)
@app.route("/pessoas/<int:id_pessoa>", methods=["GET"])
def obter_pessoa(id_pessoa):
    query = "SELECT * FROM pessoas WHERE id_pessoa = %s"
    cursor.execute(query, (id_pessoa,))
    pessoa = cursor.fetchone()
    if not pessoa:
        return "Pessoa não encontrada", 404

    return jsonify({
        "id_pessoa": pessoa["id_pessoa"],
        "nome": pessoa["nome"],
        "rg": pessoa["rg"],
        "cpf": pessoa["cpf"],
        "data_nascimento": pessoa["data_nascimento"].strftime("%d/%m/%Y"),
        "data_admissao": pessoa["data_admissao"].strftime("%d/%m/%Y"),
        "funcao": pessoa["funcao"]
    })
@app.route("/pessoas/<int:id_pessoa>", methods=["PUT"])
def atualizar_pessoa(id_pessoa):
    data = json.loads(request.data)
    nome = data["nome"]
    rg = data["rg"]
    cpf = data["cpf"]
    data_nascimento = data["data_nascimento"]
    data_admissao = data["data_admissao"]
    funcao = data.get("funcao", None)
    update_query = (
        "UPDATE pessoas SET nome = %s, rg = %s, cpf = %s, data_nascimento = %s, data_admissao = %s, funcao = %s "
        "WHERE id_pessoa = %s"
    )
    values = (nome, rg, cpf, data_nascimento, data_admissao, funcao, id_pessoa)
    cursor.execute(update_query, values)
    db.commit()
    if cursor.rowcount == 0:
        return "Registro não encontrado", 404
    query = "SELECT * FROM pessoas WHERE id_pessoa = %s"
    cursor.execute(query, (id_pessoa,))
    pessoa = cursor.fetchone()
    return jsonify(pessoa)
@app.route("/pessoas/<int:id_pessoa>", methods=["DELETE"])
def deletar_pessoa(id_pessoa):
    select_query = "SELECT * FROM pessoas WHERE id_pessoa = %s"
    cursor.execute(select_query, (id_pessoa,))
    pessoa = cursor.fetchone()
    delete_query = "DELETE FROM pessoas WHERE id_pessoa = %s"
    cursor.execute(delete_query, (id_pessoa,))
    db.commit()
    if cursor.rowcount == 0:
        return "Pessoa não encontrada", 404
    return jsonify(pessoa)
@app.route('/', methods=['GET'])
def index():
    query = "SELECT * FROM pessoas"
    cursor.execute(query)
    registros = cursor.fetchall()
    pessoas = []
    for registro in registros:
        pessoa = {
            "name": registro["nome"].split(' ')[0],
            "admissionDate": registro["data_admissao"].strftime('%d/%m/%Y'),
            "id": registro["id_pessoa"]
        }
        pessoas.append(pessoa)    
    return render_template('index.html', people=pessoas)
if __name__ == '__main__':
    app.run(debug=True)