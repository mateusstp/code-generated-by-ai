# Django App for Project, Rules, Components, and Business Units Management

## Overview
This project is a Django-based web application designed to manage Projects, Rules, Components, and Business Units with full CRUD capabilities, including archiving and restoring records. It features a modern, responsive UI and supports bilingual documentation (English and Portuguese).

## Features
- CRUD operations for Projects, Rules, Components, and Business Units
- Archive and restore functionality for all entities
- Detail and list views with search and action buttons
- User authentication and authorization
- Responsive design using Bootstrap-like styling
- CSRF protection for secure forms

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd django_app
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
7. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage Examples
- Log in as an admin to access all CRUD and archive/restore features.
- Use the search bar in list views to filter records.
- Archived items are highlighted in red and can be restored by admin users.

## Environment Variables
- Ensure you are using a virtual environment for dependency management.

## Security
- CSRF protection is enabled for all forms.
- User authentication is required for all sensitive operations.

---

# Documentação em Português

## Visão Geral
Este projeto é uma aplicação web baseada em Django para gerenciar Projetos, Regras, Componentes e Unidades de Negócio com funcionalidades completas de CRUD, incluindo arquivamento e restauração de registros. Possui uma interface moderna e responsiva, além de documentação bilíngue (Inglês e Português).

## Funcionalidades
- Operações CRUD para Projetos, Regras, Componentes e Unidades de Negócio
- Funcionalidade de arquivar e restaurar para todas as entidades
- Visualizações de detalhe e lista com busca e botões de ação
- Autenticação e autorização de usuários
- Design responsivo com estilo semelhante ao Bootstrap
- Proteção CSRF para formulários seguros

## Instruções de Instalação

1. **Clone o repositório:**
   ```bash
   git clone <seu-repositorio-url>
   cd django_app
   ```
2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Aplique as migrações:**
   ```bash
   python manage.py migrate
   ```
5. **Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Execute o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```
7. **Acesse a aplicação:**
   Abra o navegador e acesse `http://127.0.0.1:8000/`

## Exemplos de Uso
- Faça login como administrador para acessar todos os recursos de CRUD e arquivamento/restauração.
- Use a barra de busca nas listas para filtrar registros.
- Itens arquivados são destacados em vermelho e podem ser restaurados por administradores.

## Variáveis de Ambiente
- Certifique-se de usar um ambiente virtual para o gerenciamento das dependências.

## Segurança
- A proteção CSRF está habilitada para todos os formulários.
- A autenticação de usuário é obrigatória para todas as operações sensíveis.

---

## License
MIT License

## Author
Your Name
