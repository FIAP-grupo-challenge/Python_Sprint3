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
app = Flask(__name__)
CORS(app)
connection = conexao()

# Rota para criar conta
@app.post("/api/create/acount")
def create_cliente():
    INSERT_CLIENT = "INSERT INTO client (nome,email,idade,cpf,cep,senha) VALUES (%s,%s,%s,%s,%s,%s)"
    SELECT_CLIENT = "SELECT * FROM client WHERE email = (%s)"
    data = request.get_json()
    nome = data["nome"]
    email = data["email"]
    idade = data["idade"]
    cpf = data["cpf"]
    cep = data["cep"]
    senha = data["senha"]
    try:
        validador = ValidadorCliente(nome,email,idade,cpf,cep)
        del validador
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(INSERT_CLIENT, (nome,email,idade,cpf,cep,senha))
                cursor.execute(SELECT_CLIENT, (email,))
                cliente = cursor.fetchall()[0]
                id = {"client_id" : cliente[0]}
                response = make_response(id)
                response.mimetype = "raw/json"
        return response
    except Exception as e:
        print("An error occurred:", str(e))
        return str(e)


# rota para dar alterar informações do cliente
@app.route("/api/update/cliente", methods=["GET", "POST"])
def update_cliente():
    data = json.loads(request.data)
    nome = data["nome"]
    parametro = data["parametro"]
    valor_para_parametro = data["valParametro"]

    with connection:
        with connection.cursor() as cursor:
            if str(valor_para_parametro).isnumeric():
                cursor.execute(f"UPDATE client SET {parametro} = ({valor_para_parametro}) WHERE nome = ('{nome}')")
            else:
                cursor.execute(f"UPDATE client SET {parametro} = ('{valor_para_parametro}') WHERE nome = ('{nome}')")
    return "201"


# rota para obter informações do cliente com base no ip
@app.get("/api/get/client")
def get_cliente():
    SELECT_CLIENT = "SELECT * FROM client WHERE id = (%s)"
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(SELECT_CLIENT, (id,))
                cliente = cursor.fetchall()[0]
                cursor.execute(f"SELECT id,plant_type FROM plant WHERE client_id = {id} ORDER BY id")
                plantas = cursor.fetchall()
                lista_plantas = []
                for plant in plantas:
                    lista_plantas.append({"plant_id": plant[0], "plant_type": plant[1]})
                compilado = {"client": {
                             "nome": cliente[1],
                             "email": cliente[2],
                             "idade": cliente[3],
                             "cpf": cliente[4],
                             "cep": cliente[6]},
                             "plants": lista_plantas}
                response = make_response(compilado)
                response.mimetype = "raw/json"
                print(response.mimetype)
            except Exception as e:
                return "id de cliente invalido erro = " + str(e)
    return response


# rota para obter lista de clientes
@app.get("/api/get/client/list")
def get_client_list():
    SELECT_ALL_CLIENT = "SELECT id,nome FROM client ORDER BY id"
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
            response.mimetype = "raw/json"
    return response

# em uma situação de produção haveria muito mais segurança nesta area
# contudo por restrições de tempo neste prototipo n havera
@app.post("/api/get/client/login")
def get_client_login():
    data = request.get_json()
    email = data["email"]
    senha = data["senha"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id,senha FROM client WHERE email = '{email}'")
            dados = cursor.fetchall()
            if senha == dados[0][1]:
                response = True
            else:
                response = False
    return {"resposta": response,
            "client_id": dados[0][0]}


# rota para obter lista de plantas por id de cliente
@app.get("/api/get/plant/list")
def get_plant_list():
    dicionario = {}
    id = request.args.get("id")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM plant WHERE client_id = {id} ORDER BY id")
            cliente = cursor.fetchall()
            index = 0
            for c in cliente:
                dados_novos = {index: {"plant_id": c[0],
                                       "client_id": c[1],
                                       "plant_type": c[2],
                                       "plant_status": c[3]}}
                dicionario.update(dados_novos)
                index += 1
            response = make_response(dicionario)
            response.mimetype = "raw/json"
    return response

# rota para obter ifnromações da planta por id da planta
@app.get("/api/get/plant/info")
def get_planta():
    opcao = request.args.get("option")
    opcoes = {"all": "temperature,humidity,light,ph,last_time_watered",
              "temp": "temperature",
              "humi": "humidity",
              "light": "light",
              "ph": "ph",
              "water": "last_time_watered"}
    id = request.args.get("plant_id")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT {opcoes.get(opcao)} FROM plant_info WHERE plant_id = {id} ORDER BY created_at DESC")
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
            response_2.mimetype = "raw/json"
            return response_2

@app.post("/api/create/plant/info")
def create_plant_info():
    data = request.get_json()
    plant_id = data["plant_id"]
    temp = data["temp"]
    humi = data["humi"]
    light = data["light"]
    ph = data["ph"]
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM plant WHERE id = {plant_id}")
                cadastro_planta = cursor.fetchone()
                if cadastro_planta == None:
                    return "Esta planta não existe"
                else:
                    cursor.execute(f"INSERT INTO plant_info (plant_id,temperature,humidity,light,ph,last_time_watered) VALUES ("
                                   f"{plant_id},{temp},{humi},{light},{ph},NOW())")
        return "201"
    except Exception as e:
        print("An error occurred:", str(e))
        return str(e)

@app.post("/api/create/plant")
def create_plant():
    data = request.get_json()
    client_id = data["client_id"]
    plant_type = data["plant_type"]
    plant_list = ["peper", "zucchini", "arugula", "spinach", "bean", "pea",
                  "lentil", "carrot", "beet", "radish", "tomato", "lettuce"]
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM client WHERE id = {client_id}")
                cadastro_client = cursor.fetchone()
                if cadastro_client == None:
                    return "Este cliente não esta cadastrado"
                else:
                    if plant_type in plant_list:
                        cursor.execute(f"INSERT INTO plant (client_id,plant_type) VALUES ({client_id}, '{plant_type}')")
                    else:
                        return "Esta planta não esta no nosso sistema"
        return "201"
    except Exception as e:
        print("An error occurred:", str(e))
        return str(e)