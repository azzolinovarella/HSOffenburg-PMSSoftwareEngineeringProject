# Password Management System
Esse projeto foi desenvolvido durante o curso "Software Engineering" (Engenharia de Software) ministrado pelo Prof. Dr. Andreas Schaad da Hochschule Offenburg (Universidade de Ciências Applicadas de Offenburg), no primeiro semestre de 2020, período em que estudei na Alemanha.
<br><br>

## Considerações Iniciais
1) Esse projeto foi desenvolvido em Python utilizando a versão 3.8.3. Desta forma, recomenda-se fortemente o uso dessa versão.

2) Todas as bibliotecas externas com suas respectivas versões podem ser encontradas no arquivo "requirements.txt". Para instalá-las, insira em seu terminal:
````
pip install -r requirements.txt
````
<br>

## Explicação Geral do Projeto
Esse projeto tem como objetivo ser um gerenciador de senhas, i.e., um sistema capaz de armazenar com segurança senhas de diversas aplicações para diversos usuários, indicando a cada um se sua senha já foi vazado e, em caso positivo, quantas vezes. Além do usuário comum, nosso sitema possui um usuário administrador, capaz de executar algumas tarefas a mais que o usuário comum. <br>
Todas as ações neste sistema são feitas por meio de requests, com a passagem de dados em formato JSON. Desta forma, nosso sistema é capaz de executar as seguintes tarefas:
<br><br>

### Adicionar Usuário
Feito a partir de um <u>POST Request</u> passando um JSON contendo o <u>email do usuário</u>  ("user_email") e a <u>senha do usuário</u> ("user_password"), como exemplificado abaixo: 
````
{
    "user_email": "exemplo_de_email@gmail.com",
    "user_password": "Senha1234!"
}
````
<br>

### Editar Senha do Sistema do Usuário
Feito a partir de um <u>PUT Request</u> passando um JSON contendo o <u>email do usuário</u>  ("user_email"), a <u>senha antiga do usuário</u> ("user_password") e a <u>nova senha do usuário</u> ("user_new_password"), como exemplificado abaixo: 
````
{
    "user_email": "exemplo_de_email@gmail.com",
    "user_password": "Senha1234!",
    "user_new_password": "SenhaNova1234!"
}
````
<br>

### Adicionar Serviços a um Usuário
Feito a partir de um <u>PUT Request</u> passando um JSON contendo o <u>email do usuário</u> ("user_email"), a <u>senha do usuário</u> ("user_password"), o <u>nome da aplicação do usuário</u> ("service_name") e a <u>senha da aplicação do usuário</u> ("service_password"), como exemplificado abaixo:
````
{
    "user_email": "exemplo_de_email@gmail.com",
    "user_password": "SenhaNova1234!",
    "service_name": "Facebook",
    "service_password": "SenhaDoFacebook"
}
````
<br>

### Editar a Senha de um Serviço
Feito a partir de um <u>PUT Request</u> passando um JSON contendo o <u>email do usuário</u> ("user_email"), a <u>senha do usuário</u> ("user_password"), o <u>nome da aplicação do usuário</u> ("service_name") e a <u>nova senha da aplicação do usuário</u> ("service_new_password"), como exemplificado abaixo:
````
{
    "user_email": "exemplo_de_email@gmail.com",
    "user_password": "SenhaNova1234!",
    "service_name": "Facebook",
    "service_new_password": "NovaSenhaDoFacebook"
}
````
<br>

### Deletar um Serviço
Feito a partir de um <u>DELETE Request</u> passando um JSON contendo o <u>email do usuário</u> ("user_email"), a <u>senha do usuário</u> ("user_password") e o <u>nome da aplicação do usuário</u> ("service_name"), como exemplificado abaixo:
````
{
    "user_email": "exemplo_de_email@gmail.com",
    "user_password": "SenhaNova1234!",
    "service_name": "Facebook"
}
````
<br>

### Verificar os Dados um Usuário
Feito a partir de um <u>GET Request</u> passando um JSON contendo o <u>email do usuário</u> ("user_email") e a <u>senha do usuário</u> ("user_password"), como exemplificado abaixo:
````
{
    "user_email": "exemplo_de_email@gmail.com",
    "user_password": "SenhaNova1234!"
}
````
Nos retornando: 
````
{
    "Process": "Valid",
    "Process_Message": {
        "_active": true,
        "_creationdate": "2021-05-06 03:03:53.617954",
        "_email": "exemplo_de_email@gmail.com",
        "_hibp": [
            false,
            "Pwned 0 time(s)"
        ],
        "_hspassword": "$2b$12$uwyqtYyhFqCe7Vnad40Kz.0G4mMFHe1FfzHrCK3EyRpwUqUBxUB92",
        "_lastmodified": null,
        "_service_list": [],
        "_warning": [
            false,
            "Never",
            0
        ]
    }
}
````
<br>

### Deletar um Usuário
Feito a partir de um <u>DELETE Request</u> passando um JSON contendo o <u>email do usuário</u> ("user_email") e a <u>senha do usuário</u> ("user_password"), como exemplificado abaixo:
````
{
    "user_email": "exemplo_de_email@gmail.com",
    "user_password": "SenhaNova1234!"
}
````
<br>

### Modificar Dados de um Usuário (por meio do Administrador)
Feito a partir de um <u>PUT Request</u> passando um JSON contendo o <u>login do administrador</u> ("admin_login"), a <u>primeira senha de administrador</u> ("admin_pw1"), a <u>segunda senha de administrador</u> ("admin_pw2"), a <u>opção de administrador</u> ("admin_opt") e o <u>email do usuário</u> ("user_email"), como exemplificado abaixo: 
````
{
    "admin_login": "admin@admin",
    "admin_pw1": "PrimeiraSenhaDeAdm",
    "admin_pw2": "SegundaSenhaDeAdm",
    "admin_opt": OPCAO_DO_ADM,
    "user_email": "exemplo_de_email@gmail.com"
}
````
Onde OPCAO_DO_ADM pode assumir:
* "ACT": Ativa um usuário. 
* "DEACT": Desativa um usuário.
* "DEL": Deleta um usuário.
* "RANPAS": Gera uma senha aleatória para um usuário. 
<br><br>

### Editar as Informações de Administrador
Feito a partir de um <u>PUT Request</u> passando um JSON contendo o <u>login do administrador</u> ("admin_login"), a <u>primeira senha de administrador</u> ("admin_pw1"), a <u>segunda senha de administrador</u> ("admin_pw2"), o <u>novo login do administrador</u> ("admin_new_login"), a <u>nova primeira senha de administrador</u> ("admin_new_pw1") e a <u>nova segunda senha de administrador</u> ("admin_new_pw2"), como exemplificado abaixo:
````
{
    "admin_login": "admin@admin",
    "admin_pw1": "PrimeiraSenhaDeAdm",
    "admin_pw2": "SegundaSenhaDeAdm",
    "admin_new_login": "new_admin@admin",
    "admin_new_pw1": "NovaPrimeiraSenhaDeAdm",
    "admin_new_pw2": "NovaSegundaSenhaDeAdm"
}
````
<br>

## Instruções de Execução
1) Para iniciarmos nossa aplicação, basta inserirmos em nosso terminal:
````
python -m pms.app
````
2) Com nossa aplicação já inicializada, podemos executar as ações como descrito acima. Note que, isso pode ser feito, por exemplo, por meio de Softwares externos como o [Postman](https://www.postman.com/).
<br><br>

## Informações extras 
Para mais informações, abaixo encontra-se o relatório escrito por mim a respeito deste projeto.
<br><br>
<a href="docs/documents/SoftwareEngineeringAssessment.pdf"><center>Clique aqui para acessar o relatório</center></a>
