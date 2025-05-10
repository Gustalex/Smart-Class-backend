# Smart-Class - Backend

## Descrição
Este repositório contém o backend do projeto Smart-Class, uma aplicação desenvolvida para gerenciamento de aulas e atividades educacionais.

## Pré-requisitos
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- 
## Configuração
- No microservice "auth" é exigida a configuração de variáveis de ambiente no arquivo ".env" para a criação do usuário root manager, o diretório já contem um arquivo .env.example com as seguintes informações.
  
ROOT_NAME="Nome do Usuário"
ROOT_CPF=00000000000
ROOT_EMAIL=user@email.com
ROOT_PASSWORD=user_password
ROOT_ROLE=user_role

## Instalação e Execução

1. Clone o repositório:
 ```bash
  git clone https://github.com/seu-usuario/Smart-Class-backend.git
  cd Smart-Class-backend
```
2. Primeira execução (construir as imagens Docker)
 ```bash
docker-compose up --build
```
3. Para execuções posteriores
  ```bash
docker-compose up -d
```
4. Para parar os containers
 ```bash
docker-compose down
```
Pronto! Após esses passos o serviço será executado nas portas configuradas no arquivo docker-compose.yml
