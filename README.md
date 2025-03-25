# 🔐 Flask Auth API

Uma API simples de autenticação e controle de usuários utilizando **Flask**, com conexão ao **MySQL** via Docker e segurança de senhas com `bcrypt`.

## 🚀 Funcionalidades

- Cadastro de usuários com hash de senha (`bcrypt`)
- Login com verificação de senha segura
- Logout
- Leitura, edição e exclusão de usuários
- Controle de permissões por `role` (admin ou user)
- Proteção de rotas com `Flask-Login`

---

## ⚙️ Tecnologias

- Python 3.10+
- Flask
- Flask-Login
- Flask-SQLAlchemy
- MySQL (via Docker)
- bcrypt (para senhas seguras)
- PyMySQL

---

## ⚙️ Requisitos

- Python instalado (recomendado: 3.10 ou superior)
- Docker e Docker Compose instalados

---

## 📦 Instalação e execução

### 1. Clone o projeto

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

### 2. Suba o banco de dados com Docker

```bash
docker-compose up -d
```

> Isso vai criar um container MySQL acessível na porta `3306`.

### 3. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Inicie o banco de dados (crie as tabelas)

No terminal, entre no shell Flask:

```bash
flask shell
```

E execute:

```python
from database import db
db.create_all()
exit()
```

### 6. Rode o app

```bash
flask run
```

---

## 🧪 Testando a API

Você pode usar o **Postman** ou **Insomnia** para testar as rotas:

### 🔐 Login
`POST /login`

```json
{
  "username": "admin",
  "password": "senha123"
}
```

### 👤 Criar usuário
`POST /user`

```json
{
  "username": "lucas",
  "password": "senha123"
}
```

### ↺ Atualizar senha
`PUT /user/1`

```json
{
  "password": "nova_senha"
}
```

### ❌ Deletar usuário
`DELETE /user/2`

> Somente usuários com `role: admin` podem excluir outros usuários.

---

## 📁 Estrutura de Pastas

```
.
├── app.py
├── models/
│   └── user.py
├── database.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔒 Controle de Acesso

- `role: user`: pode alterar apenas sua própria senha
- `role: admin`: pode excluir qualquer usuário (menos a si mesmo)

---

## 💬 Contribuições

Sinta-se à vontade para abrir issues ou PRs!


