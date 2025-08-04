# ChatSQL - IA para Consultas SQL

Este projeto é um assistente em Streamlit que transforma perguntas em linguagem natural em consultas SQL, utilizando um modelo de linguagem da Google (Gemini) e executando as queries no seu banco de dados MySQL. Além disso, os resultados podem ser exportados em formatos Excel e PDF com layouts profissionais ou personalizados de acordo com o usuário.



<img width="972" height="907" alt="image" src="https://github.com/user-attachments/assets/c25ecd49-6bdc-42ad-8a06-52f00e0531bb" />




## 📌 Funcionalidades

- Interface de chat com IA para gerar consultas SQL a partir de perguntas.
- Execução segura apenas de comandos `SELECT`.
- Conexão com banco de dados MySQL.
- Exportação dos resultados para **Excel (.xlsx)** e **PDF (.pdf)** com layouts corporativo e simples.

## ⚙️ Requisitos

Antes de iniciar, é necessário ter instalado:

- Python 3.8 ou superior
- MySQL Server (com banco `seu banco`)
- Streamlit
- Node.js (caso queira usar recursos mais avançados com frontend)
- Pacotes Python listados no `requirements.txt`

## 🔧 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/chat-sql.git
cd chat-sql
```

2. Crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o acesso ao banco de dados MySQL:

No arquivo `app.py`, altere a linha com as variáveis de conexão para refletir suas credenciais:

```python
user, password, host, port, database_name = 'root', 'SUA_SENHA', '127.0.0.1', '3306', 'database_name'
```

⚠️ Por segurança, recomenda-se usar variáveis de ambiente ou arquivos `.env` em produção.

5. Instale o driver do MySQL para Python:

```bash
pip install pymysql
```

6. Instale os pacotes necessários para geração de PDF:

```bash
sudo apt install libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info  # (Linux)
pip install weasyprint
```

No Windows:

```bash
pip install weasyprint
```

e siga as instruções do site oficial:  
https://weasyprint.readthedocs.io/en/latest/install.html#windows

## ▶ Como Rodar

Execute o app com o Streamlit:

```bash
streamlit run app.py
```

A aplicação será aberta no navegador (http://localhost:8501).

## 🧠 Modelo de IA

O projeto usa o modelo `gemini-1.5-flash-latest` via `langchain_google_genai`. Configure a variável `GOOGLE_API_KEY` com sua chave da API do Google:

```bash
export GOOGLE_API_KEY="sua-chave-aqui"  # Linux/Mac
set GOOGLE_API_KEY=sua-chave-aqui       # Windows (cmd)
$env:GOOGLE_API_KEY="sua-chave-aqui"    # Windows (PowerShell)
```

## 📄 Licença

Este projeto é de uso livre para fins educacionais. Sinta-se à vontade para modificar, distribuir e aprimorar.

## 💬 Contato

**Lucas Sousa**  
[LinkedIn](https://www.linkedin.com/in/lucasmoreirasousa/)
