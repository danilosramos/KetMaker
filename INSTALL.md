# Guia de Instalação e Configuração (INSTALL.md)

Este documento detalha os passos necessários para instalar e configurar o ambiente de desenvolvimento e execução do projeto **KetMaker**.

## 1. Pré-requisitos

O projeto KetMaker é desenvolvido em Python e utiliza o framework Flask para o backend.

- **Sistema Operacional:** Linux, macOS ou Windows.
- **Python:** Versão 3.x (Recomendado: Python 3.10 ou superior).
- **Gerenciador de Pacotes:** `pip` (geralmente instalado com o Python).

## 2. Instalação

### 2.1. Clonar o Repositório

```bash
git clone https://github.com/danilosramos/KetMaker.git
cd KetMaker
```

### 2.2. Configurar o Ambiente Virtual

É altamente recomendado o uso de um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
# No Linux/macOS
source venv/bin/activate
# No Windows (Command Prompt)
venv\Scripts\activate.bat
# No Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 2.3. Instalar Dependências

O projeto utiliza o Flask. As dependências serão instaladas a partir de um arquivo `requirements.txt` (a ser criado). Por enquanto, instale o Flask manualmente:

```bash
pip install Flask
```

## 3. Configuração

### 3.1. Variáveis de Ambiente

O projeto pode exigir variáveis de ambiente para configuração (ex: chaves secretas, conexão com banco de dados).

Por exemplo, para o Flask:

```bash
# No Linux/macOS
export FLASK_APP=software/backend/app.py
export FLASK_ENV=development

# No Windows (Command Prompt)
set FLASK_APP=software/backend/app.py
set FLASK_ENV=development
```

## 4. Execução

Com o ambiente virtual ativado e as variáveis de ambiente configuradas, você pode executar o servidor Flask:

```bash
flask run
```

O servidor estará acessível em `http://127.0.0.1:5000/`.

## 5. Estrutura do Código

O código-fonte principal está organizado na pasta `software`:

- `software/backend/`: Contém os arquivos Python do servidor (`app.py`, `ketmaker.py`).
- `software/frontend/`: Contém os arquivos HTML, CSS e JavaScript da interface do usuário (`index.html`).
