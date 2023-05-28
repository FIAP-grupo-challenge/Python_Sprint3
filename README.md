<a name="API"></a>

<br />
<div align="center">
  <a href="#">
    <img src="images/logo.png" alt="Logo" width="auto" height="80">
  </a>
</div>

## Sobre o projeto

<div>
<p>Esta api foi escrita com o intuito de conectar diversar partes do sistema da mini estufa <br></p>
<p>Areas que api conecta: <br>
* Sensores/Arduino da estufa <br>
* Banco de dados <br>
* Site da empresa <br>
* Dashboard do cliente</p>
</div>
<div align="center">

</div>

## Instalação
1. Clonar o respositorio
    ```sh
    git clone https://github.com/FIAP-grupo-challenge/Python_GS.git
    ```
2. Instalar dependencias
    ```sh
    pip install -r requirements.txt
    ```
3. Rodar o flask (servidor de desenvolvimento)
    ```sh
    flask run --port 80 
    ```
    <div>
    <p>
    Não eh necessario que o programa seja executado na porta 80, contudo a demonstração deste <br>
    documento sera feita no servidor de desenvolvimento do flask (improprio para produção) e porta 80
    </p></div>

## Endpoints
1. Criar conta
    ```text
    /api/create/acount
    ```
   <div>
   <p>
   Uso: criar uma conta no banco de dados <br>
   <br> Exemplo: </p>
   <img src="images/exemplo1.png" alt="Logo" width="auto" height="auto"><br>
   <p>Este endpoint possui validações</p><br>
   <p>Validações:<br>
   * email :<br> <img src="images/code1.png" alt="Logo" width="auto" height="auto"><br>
   * idade :<br> <img src="images/code2.png" alt="Logo" width="auto" height="auto"><br>
   * cpf :<br> <img src="images/code3.png" alt="Logo" width="auto" height="auto"><br>
   * cep :<br> <img src="images/code4.png" alt="Logo" width="auto" height="auto"></p><br><br><br></div>

2. Mudar informações da conta
    ```text
    /api/update/cliente
    ```
   <div>
   <p>
   Uso: Modifica um elemento especifico da informação do cliente  <br>
   <br> Exemplo: </p>
   <img src="images/exemplo2.png" alt="Logo" width="auto" height="auto">
   <p>Lista de parametros editaveis:<br>
   * nome<br>
   * email<br>
   * idade<br>
   * cpf<br>
   * cep<br>
   * senha</p><br><br><br></div>
   
3. Buscar cliente por ID
    ```text
    /api/get/client?id=(id desejado)
    ```
   <div>
   <p>
   Uso: Buscar informações de um cliente que voce tem o ID <br>
   <br> Exemplo: </p>
   <img src="images/exemplo3.png" alt="Logo" width="auto" height="auto"><br>
   <p>
   Este endpoint deve receber um parametro id para que a busca possa ser feita</p><br><br><br></div>

4. Lista de clientes
    ```text
    /api/get/client/list
    ```
   <div>
   <p>
   Uso: Fornece uma lista de clientes que mostra os seus nomes e IDs <br>
   <br> Exemplo: </p>
   <img src="images/exemplo4.png" alt="Logo" width="auto" height="auto"><br><br><br></div>

5. Lista de plantas por id de cliente
    ```text
    /api/get/plant/list?id=(id desejado)
    ```
   <div>
   <p>
   Uso: Fornece uma lista de todas as plantas daquele cliente <br>
   <br> Exemplo: </p>
   <img src="images/exemplo5.png" alt="Logo" width="auto" height="auto"><p>
   Este endpoint deve receber um parametro id para que a busca possa ser feita</p><br><br><br></div>

6. Obter informações de uma planta em específico
    ```text
    /api/get/plant/info?plant_id=(id da planta desejado)&option=(opção)
    ```
   <div>
   <p>
   Uso: Fornece informações da planta <br>
   <br> Exemplo: </p>
   <img src="images/exemplo6.png" alt="Logo" width="auto" height="auto"><p>
   Este endpoint deve receber um parametro id para que a busca possa ser feita<br>
   juntamente do parametro options</p><br>
   <p>Parametro option:<br>
   * all : retorna todas as informações da planta<br>
   * temp : retorna a temperatura do ambiente da planta<br>
   * humi : retorna a humidade do ambiente da planta<br>
   * light : retorna a luminosidade do ambiente da planta<br>
   * ph : retorna o ph do solo no ambiente da planta<br>
   * water : retorna a ultima vez que a planta foi regada (timestamp)</p><br><br><br></div>

