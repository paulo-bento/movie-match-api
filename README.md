# MovieMatch API

API REST para um sistema de recomendação de filmes e séries, baseado em avaliações dos usuários. Projeto desenvolvido para a disciplina **WEB I** – Segunda Unidade.

---

## 📌 Funcionalidades

- **CRUD completo** de filmes, gêneros e avaliações
- **Autenticação JWT** (login e refresh token)
- **Soft delete** em todos os modelos
- **Filtros e busca** por título, gênero, ano, etc.
- **Paginação** nas listagens
- **Cache** em endpoints de listagem
- **Endpoint de recomendação** (`/filmes/recomendados/`)
- **Documentação interativa** com Swagger e ReDoc
- **Permissões personalizadas** (apenas dono pode editar/deletar avaliações)

---

## 🛠️ Tecnologias

- **Python 3.14**
- **Django 6.1**
- **Django REST Framework**
- **PostgreSQL**
- **JWT** (djangorestframework-simplejwt)
- **drf-spectacular** (documentação Swagger)
- **django-filter** (filtros avançados)

---

## 📦 Como rodar o projeto localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/movie-match-api.git
cd movie-match-api
```

### 2. Criar e ativar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Criar banco de dados PostgreSQL

```bash
sudo -u postgres psql -c "CREATE DATABASE movie_match;"
```

### 5. Configurar variáveis de ambiente (`.env`)

```env
DB_NAME=movie_match
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-sua-chave-aqui
```

### 6. Rodar migrações

```bash
python manage.py migrate
```

### 7. Criar superusuário

```bash
python manage.py createsuperuser
```

### 8. (Opcional) Cadastrar dados iniciais via admin

- Acesse `/admin/`
- Crie gêneros, filmes e avaliações

### 9. Rodar servidor

```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/api/v1/`

---

## 📚 Documentação da API

- **Swagger UI:** `http://127.0.0.1:8000/api/swagger/`
- **ReDoc:** `http://127.0.0.1:8000/api/redoc/`

---

## 🧪 Como testar a API com Postman

### Configuração inicial

1. Crie um **Environment** no Postman:
   - `base_url`: `http://127.0.0.1:8000`
   - `token`: (deixe vazio, será preenchido automaticamente)

2. Crie uma **Collection** chamada `MovieMatch API`.

---

### Autenticação (JWT)

**Obter token de acesso**

- **POST** `{{base_url}}/api/token/`
- Body (JSON):
```json
{
    "email": "admin@admin.com",
    "password": "admin123"
}
```

**Salvar token automaticamente** (aba "Tests"):
```javascript
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set('token', response.access);
}
```

---

### Filmes

| Ação | Método | URL | Body (exemplo) |
|------|--------|-----|----------------|
| Listar | GET | `/api/v1/filmes/` | - |
| Criar | POST | `/api/v1/filmes/` | `{"titulo":"Matrix","descricao":"...","ano_lancamento":1999,"generos":[1,2]}` |
| Buscar | GET | `/api/v1/filmes/1/` | - |
| Atualizar (PUT) | PUT | `/api/v1/filmes/1/` | todos os campos |
| Atualizar (PATCH) | PATCH | `/api/v1/filmes/1/` | `{"titulo":"Novo título"}` |
| Deletar | DELETE | `/api/v1/filmes/1/` | - |

---

### Gêneros

| Ação | Método | URL | Body (exemplo) |
|------|--------|-----|----------------|
| Listar | GET | `/api/v1/generos/` | - |
| Criar | POST | `/api/v1/generos/` | `{"nome":"Ação","descricao":"..."}` |
| Buscar | GET | `/api/v1/generos/1/` | - |
| Atualizar | PATCH | `/api/v1/generos/1/` | `{"nome":"Aventura"}` |
| Deletar | DELETE | `/api/v1/generos/1/` | - |

---

### Avaliações

| Ação | Método | URL | Body (exemplo) |
|------|--------|-----|----------------|
| Listar | GET | `/api/v1/avaliacoes/` | - |
| Criar | POST | `/api/v1/avaliacoes/` | `{"filme":1,"nota":5,"comentario":"Excelente!"}` |
| Buscar | GET | `/api/v1/avaliacoes/1/` | - |
| Atualizar | PATCH | `/api/v1/avaliacoes/1/` | `{"nota":4}` |
| Deletar | DELETE | `/api/v1/avaliacoes/1/` | - |

**🔐 Permissão:** apenas o dono da avaliação pode editar/deletar.

---

### Filtros e buscas

```http
GET /api/v1/filmes/?search=matrix
GET /api/v1/filmes/?generos=1&ano_lancamento=1999
```

---

### Endpoint de recomendados

```http
GET /api/v1/filmes/recomendados/
```

Retorna os 10 filmes com maior média de nota (que tenham pelo menos 1 avaliação).

---

## ✅ Requisitos atendidos

- [x] `.env`
- [x] `BaseModel`
- [x] Soft Delete
- [x] Versionamento da API (`/api/v1/`)
- [x] Autenticação JWT
- [x] Pelo menos 3 modelos (Filme, Gênero, Avaliação, CustomUser)
- [x] Documentação com Swagger
- [x] CRUD completo (serializer, viewset, router)
- [x] Paginação
- [x] Cache nas listagens
- [x] Search com `query_params`
- [x] Apresentação com Postman

---

## 📁 Estrutura do Projeto

```
movie-match-api/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py
│   ├── admin.py
│   ├── api/
│   │   └── v1/
│   │       ├── serializers.py
│   │       ├── viewsets.py
│   │       ├── router.py
│   │       └── permissions.py
│   └── ...
├── .env
├── manage.py
└── requirements.txt
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**João Paulo Bento**  
[GitHub](https://github.com/seu-usuario)
