import os
import psycopg2
from apps.validador_cliente import ValidadorCliente
from dotenv import load_dotenv
from flask import *
from flask_cors import CORS


def conexao():
    url = os.getenv("DATABASE_URL")
    _conexao = psycopg2.connect(url)
    return _conexao


load_dotenv()

INSERT_CLIENT = "INSERT INTO client (nome,email,idade,cpf,cep,senha) VALUES (%s,%s,%s,%s,%s,%s)"
SELECT_CLIENT = "SELECT * FROM client WHERE id = (%s)"
SELECT_ALL_CLIENT = "SELECT id,nome FROM client ORDER BY id"
app = Flask(__name__)
CORS(app)
connection = conexao()


@app.post("/api/create/acount")
def create_cliente():
    data = request.get_json()
    nome = data["nome"]
    email = data["email"]
    idade = data["idade"]
    cpf = data["cpf"]
    cep = data["cep"]
    senha = data["senha"]
    try:
        validador = ValidadorCliente(nome,email,idade,cpf,cep)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_CLIENT, (nome,email,idade,cpf,cep,senha))
        return "201"
    except Exception as e:
        print("An error occurred:", str(e))
        return str(e)


@app.route("/api/update/cliente", methods=["GET", "POST"])
def update_cliente():
    data = json.loads(request.data)
    nome = data["nome"]
    parametro = data["parametro"]
    valor_para_parametro = data["valParametro"]

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE client SET {parametro} = ({valor_para_parametro}) WHERE nome = ('{nome}')")
    return "201"


@app.get("/api/get/client")
def get_cliente():
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(SELECT_CLIENT, (id,))
                cliente = cursor.fetchall()[0]
                compilado = {"nome": cliente[1],
                             "email": cliente[2],
                             "idade": cliente[3],
                             "cpf": cliente[4],
                             "cep": cliente[6]}
                response = make_response(compilado)
                response.mimetype = "text/plain"
                print(response.mimetype)
            except Exception as e:
                return "id de cliente invalido erro = " + str(e)
    return response


@app.get("/api/get/client/list")
def get_client_list():
    dicionario = {}
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_CLIENT)
            cliente = cursor.fetchall()
            index = 0
            for c in cliente:
                dados_novos = {index: {"id": c[0], "nome": c[1]}}
                dicionario.update(dados_novos)
                index += 1
            response = make_response(dicionario)
            response.mimetype = "text/plain"
            print(response.mimetype)
    return response


@app.get("/api/plant/info")
def get_planta():
    opcao = request.args.get("option")
    opcoes = {"all": "temperature,humidity,light,ph,last_time_watered",
              "temp": "temperature",
              "humi": "humidity",
              "light": "light",
              "ph": "ph",
              "water": "last_time_watered"}
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT {opcoes.get(opcao)} FROM plant_info WHERE plant_id = {id}")
            dados = cursor.fetchall()
            if opcao == "all":
                compilado = {"temp": dados[0][0],
                             "humi": dados[0][1],
                             "light": dados[0][2],
                             "ph": dados[0][3],
                             "water": dados[0][4]}
                response_1 = make_response(compilado)
                response_1.mimetype = "text/plain"
                return response_1
            compilado = {opcao:dados[0][0]}
            response_2 = make_response(compilado)
            response_2.mimetype = "text/plain"
            return response_2
