Primeiro projeto fullstack realizado em Django. 


    Título Projeto: ToDo (aplicação de lista de tarefas) — Django

Descrição Aplicação simples de gerenciamento de tarefas desenvolvida com Django. 
Permite criar, listar, editar, excluir e marcar tarefas como concluídas.
Foi usada como projeto didático para demonstrar conceitos do Django (models, migrations, Class Based Views, templates, forms, csrf, etc.).

    Funcionalidades

Listar tarefas (ordenadas por data de entrega)
Cadastrar nova tarefa (título + data de entrega)
Editar tarefa
Excluir tarefa (com confirmação)
Marcar tarefa como concluída (atribui data de conclusão)
Painel administrativo do Django (admin)

    Tecnologias principais:

- Python
- Django (Class Based Views: ListView, CreateView, UpdateView, DeleteView, View)
- SQLite (db.sqlite3 — usado em desenvolvimento)
- Bootstrap 5 (front-end)
- django-crispy-forms + crispy-bootstrap5 (renderização/estilização de formulários)
- python-decouple (gerenciamento de variáveis sensíveis/ambiente)
- dj-database-url (parsing de DATABASE_URL)
- Black (formatador de código)
- VS Code (editor) + extensões para Django/templates e visualização de SQLite
- Git/Gitignore
- 
    Pré-requisitos

Python 3.8+ instalado
pip disponível
(opcional) Visual Studio Code e extensões para Django/templates e SQLite viewer
Instalação e execução (passo-a-passo)

- Obtenha o código fonte do projeto (clone o repositório ou copie os arquivos para sua máquina).

- Crie e ative um ambiente virtual

- Criar: python -m venv .venv

- Ativar no Windows (PowerShell): ..venv\Scripts\Activate (se der erro por política do PowerShell, execute: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force)

- Ativar no Windows (CMD): ..venv\Scripts\activate.bat

- Ativar em macOS / Linux: source .venv/bin/activate

- Instale dependências

- Se existir requirements.txt: pip install -r requirements.txt

- Se não tiver, instale manualmente: pip install django django-crispy-forms crispy-bootstrap5 python-decouple dj-database-url black

- Configurar variáveis de ambiente / .env

- Crie um arquivo .env na raiz do projeto (não comite esse arquivo).

- Exemplo mínimo (valores de exemplo — ajuste conforme desejado): SECRET_KEY=troque_por_uma_chave_segura DEBUG=True ALLOWED_HOSTS=127.0.0.1,localhost DATABASE_URL=sqlite:///db.sqlite3

- O projeto usa python-decouple para ler essas variáveis no settings.py; ajuste conforme sua configuração local.

- Migrations (criar esquema do banco)

- Gerar migrações (caso tenha alterado models): python manage.py makemigrations

- Aplicar migrações: python manage.py migrate

- Criar superusuário (opcional, para acessar /admin) python manage.py createsuperuser

- Executar servidor de desenvolvimento python manage.py runserver

- Acesse no navegador: http://localhost:8000 (rota raiz da aplicação)

- /update/<pk>/ → Edição de tarefa (pk = id)

- /delete/<pk>/ → Página de confirmação e exclusão

- /complete/<pk>/ → Ação para marcar tarefa como concluída (Observação: nomes exatos das rotas podem variar no projeto; use os caminhos definidos em setup/urls.py ou no arquivo de rotas da app.)

    Boas práticas / recomendações

- Mantenha SECRET_KEY e outras credenciais fora do repositório (use .env).
- Use o venv por projeto para isolar dependências.
- Utilize Black para formatação automática do código.
- Use a filosofia “fat models, thin views” (regras de negócio dentro dos models).
- Caso leve o app para produção, troque SQLite por um SGBD (Postgres/MySQL) e ajuste DATABASE_URL adequadamente.
- Exemplo de requirements.txt (sugestão) Django>=4.2 django-crispy-forms crispy-bootstrap5 python-decouple dj-database-url black

    Dicas de desenvolvimento (VS Code)

Ative formatação automática (Black) ao salvar para manter padrão de código.
Instale extensão de sintaxe de templates Django para melhor autocompletar.
Use extensão de visualização/edição de SQLite para inspecionar o db.sqlite3.
Problemas comuns e soluções rápidas

Erro 403 CSRF ao submeter formulário: verifique se o template inclui a tag csrf_token dentro do form. Em formulários POST, a tag "{% csrf_token %}" (template tag do Django) é obrigatória.
Ativação do .venv no PowerShell: ajuste a política com Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force (somente para sessão atual).
Migrações falham ao alterar tipos: em alguns casos SQLite não suporta alteração direta de coluna — pode ser necessário recriar tabela ou adaptar migração manualmente; para desenvolvimento, recriar db.sqlite3 e aplicar migrations pode ser a opção mais rápida.
O que o projeto entrega na prática

Uma aplicação CRUD completa para tarefas, com interface web básica estilizada com Bootstrap e formulários mais amigáveis via crispy-forms. Permite ver na prática: models, migrations, Class Based Views (List/Create/Update/Delete), templates com herança, gerenciamento de ambiente e variáveis sensíveis.


