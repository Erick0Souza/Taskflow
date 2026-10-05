# TaskFlow

Sistema web para gestão de projetos e tarefas, desenvolvido com **Python** e **Django**.

O projeto foi pensado para ser simples de usar e fácil de manter: interface limpa, regras de acesso claras e fluxo de tarefas sem retornos desnecessários.

## Funcionalidades

- Cadastro e login de usuários.
- Perfis de acesso: Administrador, Gerente e Membro.
- Criação e edição de projetos.
- Inclusão e remoção de membros por projeto.
- Tarefas com responsável, prioridade e prazo.
- Busca e filtros.
- Comentários nas tarefas.
- Histórico de alterações.
- Dashboard com resumo de pendências, andamento, concluídas e atrasadas.
- Controle de permissões por projeto.
- Fluxo de status somente para frente:

```text
Pendente → Em andamento → Concluída
```

Depois de concluída, a tarefa não volta automaticamente para estados anteriores.

## Tecnologias

- Python 3.13
- Django 5.2
- Django ORM
- SQLite para desenvolvimento local
- PostgreSQL para Docker/produção
- HTML
- CSS
- JavaScript
- WhiteNoise
- Gunicorn
- Docker
- GitHub Actions

## Rodando no Windows

### Opção rápida

Execute:

```powershell
setup.bat
run.bat
```

### Manualmente

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative:

```powershell
.venv\Scripts\activate
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Copie o arquivo de ambiente:

```powershell
Copy-Item .env.example .env
```

Execute as migrations:

```powershell
python manage.py migrate
```

Crie o administrador inicial:

```powershell
python manage.py create_initial_admin
```

Inicie:

```powershell
python manage.py runserver
```

Abra:

```text
http://127.0.0.1:8000
```

## Conta inicial

Ao executar `create_initial_admin` sem variáveis extras:

```text
Usuário: admin
E-mail: admin@taskflow.local
Senha: Admin@123
```

Use apenas para ambiente local. Troque a senha em qualquer ambiente real.

## Banco PostgreSQL com Docker

Execute:

```powershell
docker compose up --build
```

Depois acesse:

```text
http://127.0.0.1:8000
```

## Testes

Execute:

```powershell
python manage.py test tests
```

Os testes cobrem cadastro, criação de projetos, controle de acesso, membros e avanço de status das tarefas.

## Estrutura

```text
accounts/       autenticação e usuários
projects/       projetos e equipes
tasks/          tarefas, comentários e histórico
dashboard/      página inicial
templates/      telas HTML
static/         CSS e JavaScript
tests/          testes automatizados
config/         configurações do Django
```

## Otimizações aplicadas

- `select_related` e `prefetch_related` nas consultas principais.
- Paginação em projetos e tarefas.
- Índices nos campos mais usados em filtros.
- Regras de negócio isoladas em services.
- Controle de permissões separado da camada de apresentação.
- PostgreSQL com `CONN_MAX_AGE`.
- Static files com WhiteNoise.
- Gunicorn com múltiplos workers.
- Containers sem dependências de desenvolvimento desnecessárias.

## GitHub

Não envie:

```text
.env
.venv/
db.sqlite3
media/
staticfiles/
```

O `.gitignore` já está preparado para isso.
