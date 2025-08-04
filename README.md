# ChatSQL 🧠

Uma aplicação web inteligente construída com Streamlit e Google Gemini que permite aos usuários fazer perguntas em linguagem natural (Português) e receber respostas diretamente de um banco de dados MySQL. A aplicação traduz a pergunta para uma consulta SQL, executa-a e exibe os resultados, oferecendo também a opção de exportar os dados para relatórios profissionais em Excel e PDF com múltiplos layouts.

## Demonstração

<img width="831" height="835" alt="image" src="https://github.com/user-attachments/assets/533fe7c0-9dce-486a-b05b-f0be0c46db0f" />

## Funcionalidades Principais

- **Interface de Chat Intuitiva:** Converse com seu banco dedados como se estivesse falando com um assistente.
- **Tradução de Linguagem Natural para SQL:** Utiliza o poder do Google Gemini para converter perguntas como "quais os 5 produtos mais caros?" na consulta SQL correspondente.
- **Visualização de Dados:** Exibe os resultados das consultas em tabelas claras e legíveis.
- **Geração de Relatórios Profissionais:**
    - **Excel:** Exporta dados para arquivos `.xlsx` com cabeçalhos formatados e largura de coluna autoajustada.
    - **PDF:** Oferece múltiplos layouts para download, incluindo:
        - **Simples:** Apenas os dados brutos.
        - **Corporativo:** Com cabeçalho, rodapé, logo e formatação profissional.
        - **Executivo:** Inclui um resumo visual com um gráfico gerado a partir dos dados.

## Pilha Tecnológica

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Inteligência Artificial (LLM):** [Google Gemini](https://ai.google.dev/)
- **Orquestração da IA:** [LangChain](https://www.langchain.com/)
- **Banco de Dados:** [MySQL](https://www.mysql.com/)
- **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
- **Geração de Relatórios:**
    - **Excel:** [XlsxWriter](https://xlsxwriter.readthedocs.io/)
    - **PDF:** [WeasyPrint](https://weasyprint.org/)
    - **Gráficos:** [Matplotlib](https://matplotlib.org/)

---

## Guia de Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

Antes de começar, garanta que você tenha os seguintes softwares instalados:

1.  **Python 3.9+**: [Link para download](https://www.python.org/downloads/)
2.  **Git**: [Link para download](https://git-scm.com/downloads)
3.  **Um servidor MySQL**: Um banco de dados MySQL precisa estar ativo e acessível (ex: instalado localmente ou em um container Docker).

### Passo a Passo

**1. Clonar o Repositório**

Abra seu terminal e clone este repositório para sua máquina.
```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```
*(Substitua `seu-usuario/seu-repositorio` pelo caminho real do seu projeto no GitHub.)*

**2. Criar um Ambiente Virtual**

É uma boa prática isolar as dependências do projeto.
```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

**3. Instalar Dependências**

Instale todas as bibliotecas Python necessárias com um único comando.
```bash
pip install -r requirements.txt
```
*(Se você ainda não tem um arquivo `requirements.txt`, veja as instruções na próxima seção para criá-lo.)*

**4. Instalar Dependências de Sistema (Para PDFs no Windows)**

O `WeasyPrint` requer a instalação do GTK+ no Windows. Se você estiver usando Windows, siga este passo crucial:

- Baixe e instale o GTK+ a partir [deste link](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).
- Adicione o diretório de instalação do GTK+ (ex: `C:\Program Files\GTK3-Runtime\bin`) à variável de ambiente `PATH` do seu sistema.
- **Reinicie o terminal** após a instalação e a configuração do PATH.

**5. Configurar o Banco de Dados**

- Acesse seu servidor MySQL e crie um banco de dados. O nome padrão no código é `testemaxima`.
  ```sql
  CREATE DATABASE testemaxima;
  ```
- Para ter dados para testar, execute o script SQL abaixo dentro do seu novo banco de dados.
<details>
  <summary>Clique para ver o Script SQL de Exemplo</summary>
  
  ```sql
  USE testemaxima;

  CREATE TABLE produtos (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nome_produto VARCHAR(255) NOT NULL,
      categoria VARCHAR(100),
      preco DECIMAL(10, 2),
      estoque INT
  );

  CREATE TABLE vendas (
      id_venda INT AUTO_INCREMENT PRIMARY KEY,
      id_produto INT,
      quantidade INT,
      valor_total DECIMAL(10, 2),
      data_venda DATE,
      FOREIGN KEY (id_produto) REFERENCES produtos(id)
  );

  INSERT INTO produtos (nome_produto, categoria, preco, estoque) VALUES
  ('Laptop Gamer Pro', 'Eletrônicos', 7500.00, 15),
  ('Smartphone X1', 'Eletrônicos', 3200.50, 40),
  ('Cadeira de Escritório Ergonômica', 'Móveis', 899.90, 25),
  ('Monitor Ultrawide 34"', 'Eletrônicos', 2800.00, 20),
  ('Teclado Mecânico RGB', 'Acessórios', 450.00, 60);

  INSERT INTO vendas (id_produto, quantidade, valor_total, data_venda) VALUES
  (1, 1, 7500.00, '2025-07-15'),
  (2, 2, 6401.00, '2025-07-20'),
  (3, 5, 4499.50, '2025-07-22'),
  (5, 10, 4500.00, '2025-08-01');
  ```
</details>

**6. Configurar Credenciais no Código**

Abra o arquivo `app.py` em um editor de texto ou IDE e localize a função `get_sql_from_prompt`. Atualize as seguintes informações:

```python
# Dentro da função get_sql_from_prompt
try:
    # --- PREENCHA SUAS CREDENCIAIS AQUI ---
    # ATENÇÃO: Use st.secrets ou variáveis de ambiente para proteger suas credenciais em produção!
    os.environ["GOOGLE_API_KEY"] = "SUA_CHAVE_API_DO_GOOGLE_AQUI"
    user = 'seu_usuario_mysql'
    password = 'sua_senha_mysql'
    host = '127.0.0.1' # ou o IP do seu servidor de banco de dados
    port = '3306'
    database_name = 'testemaxima'
    # ----------------------------------------
```

**7. Executar a Aplicação**

Com tudo configurado, execute o comando abaixo no seu terminal (com o ambiente virtual ativado):

```bash
streamlit run app.py
```

Seu navegador abrirá automaticamente com a aplicação em funcionamento.

## Como Usar

1.  Digite uma pergunta no campo de chat na parte inferior da tela.
2.  Pressione Enter.
3.  Aguarde a IA processar, gerar a consulta SQL e buscar os resultados.
4.  Visualize a tabela com os dados retornados.
5.  Abaixo dos resultados, utilize os botões de download para exportar o relatório em Excel ou PDF no layout de sua preferência.


## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
