# ==============================================================================
# 1. IMPORTAÇÕES
# ==============================================================================
import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_sql_query_chain
from dotenv import load_dotenv

# Importações para geração de relatórios
import io
import datetime
import re
from weasyprint import HTML, CSS

# ==============================================================================
# 2. FUNÇÕES AUXILIARES PARA RELATÓRIOS
# ==============================================================================

def sanitize_filename(text):
    return re.sub(r'[\\/*?:"<>|]', "", text)

def create_professional_filename(prompt):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    sanitized_prompt = sanitize_filename(prompt[:30]).replace(' ', '_')
    return f"Relatorio_{sanitized_prompt}_{timestamp}"

def convert_df_to_excel(df, prompt):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        sheet_name = 'Relatorio'
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        title_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter'})
        header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#0056B3', 'font_color': 'white', 'border': 1})
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(2, col_num, value, header_format)
        for i, col in enumerate(df.columns):
            column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, column_len)
    return output.getvalue()

def create_pdf_simple(df):
    html_string = df.to_html(index=False, justify='center', border=1)
    return HTML(string=html_string).write_pdf()

def create_pdf_corporate(df, prompt):
    generation_time = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    html_string = df.to_html(index=False, justify='center', border=1)
    html_with_style = f"""
    <html><head><meta charset="UTF-8"><style>
        @page {{ size: A4 portrait; margin: 2cm;
            @top-center {{ content: "🧠 Relatório de Análise de Dados"; font-size: 14px; font-weight: bold; font-family: sans-serif; color: #333; }}
            @bottom-right {{ content: "Página " counter(page) " de " counter(pages); font-family: sans-serif; font-size: 10px; }}
        }}
        body {{ font-family: sans-serif; font-size: 11px; }} h2 {{ text-align: center; color: #0056b3; }}
        .prompt {{ font-style: italic; text-align: center; color: #555; margin-bottom: 20px; }}
        .timestamp {{ text-align: center; font-size: 10px; color: #777; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #dddddd; text-align: left; padding: 6px; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        th {{ background-color: #0056b3; color: white; font-weight: bold;}}
    </style></head><body>
        <h2>Resultados da Consulta</h2><p class="prompt">" {prompt} "</p><p class="timestamp">Gerado em: {generation_time}</p>{html_string}
    </body></html>"""
    return HTML(string=html_with_style).write_pdf()

# ==============================================================================
# 3. CONFIGURAÇÃO DA PÁGINA E LÓGICA DE BACK-END
# ==============================================================================

st.set_page_config(page_title="ChatSQL", page_icon="🧠", layout="centered", initial_sidebar_state="collapsed")
st.title("🧠 ChatSQL")
st.write("Faça uma pergunta e a IA irá transformá-la em uma consulta SQL e trazer o resultado.")

load_dotenv()

def get_sql_from_prompt(prompt):
    try:
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST", "127.0.0.1")
        port = os.getenv("DB_PORT", "3306")
        database_name = os.getenv("DB_NAME")

        user_encoded = quote_plus(user)
        password_encoded = quote_plus(password)
        connection_string = f"mysql+pymysql://{user_encoded}:{password_encoded}@{host}:{port}/{database_name}"

        db = SQLDatabase.from_uri(connection_string)
        engine = create_engine(connection_string)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
        generate_query_chain = create_sql_query_chain(llm, db)

        consulta_sql_gerada = generate_query_chain.invoke({"question": prompt})
        sql_limpo = consulta_sql_gerada.strip().replace("```sql", "").replace("```", "").strip()

        if sql_limpo.strip().upper().startswith("SELECT"):
            with engine.connect() as connection:
                resultado = connection.execute(text(sql_limpo)).mappings().all()
            df = pd.DataFrame(resultado)
            return {"sql": sql_limpo, "df": df, "error": None}
        else:
            return {"sql": sql_limpo, "df": None, "error": "AÇÃO BLOQUEADA! Apenas consultas SELECT são permitidas."}
    except Exception as e:
        return {"sql": None, "df": None, "error": f"Ocorreu um erro: {e}"}

# ==============================================================================
# 4. INTERFACE DE CHAT DO STREAMLIT
# ==============================================================================

def display_download_section(df, user_prompt, key_suffix):
    st.write("---")
    col1, col2 = st.columns(2)
    file_name_base = create_professional_filename(user_prompt)

    with col1:
        st.download_button(
            label="**Excel (.xlsx)**",
            data=convert_df_to_excel(df, user_prompt),
            file_name=f"{file_name_base}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key=f"excel_{key_suffix}"
        )

    session_key = f"pdf_layout_{key_suffix}"
    selected_layout = st.session_state.get(session_key, "Corporativo")

    if selected_layout == "Simples":
        pdf_data = create_pdf_simple(df)
    else:
        pdf_data = create_pdf_corporate(df, user_prompt)

    with col2:
        st.download_button(
            label="**PDF (.pdf)**",
            data=pdf_data,
            file_name=f"{file_name_base}_{selected_layout.lower()}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key=f"pdf_download_{key_suffix}"
        )

    st.selectbox(
        "Escolha o layout do PDF para o próximo download:",
        ("Corporativo", "Simples"),
        key=session_key,
        help="A sua escolha aqui será usada na próxima vez que você clicar no botão 'PDF (.pdf)'."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if "prompt" in message:
            st.markdown(message["prompt"])
        if "response" in message:
            response_data = message["response"]
            if response_data["error"]:
                st.error(response_data["error"])
            else:
                st.markdown("Aqui está o que eu encontrei:")
                st.code(response_data["sql"], language='sql')
                if not response_data["df"].empty:
                    st.dataframe(response_data["df"])
                    if i > 0 and st.session_state.messages[i-1]['role'] == 'user':
                        user_prompt = st.session_state.messages[i-1]['prompt']
                        display_download_section(response_data["df"], user_prompt, key_suffix=f"history_{i}")
                else:
                    st.write("A consulta não retornou resultados.")

if prompt := st.chat_input("Qual a sua pergunta?"):
    st.session_state.messages.append({"role": "user", "prompt": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💡"):
        with st.spinner("Pensando..."):
            response = get_sql_from_prompt(prompt)
            if response["error"]:
                st.error(response["error"])
            else:
                st.markdown("Aqui está o que eu encontrei:")
                st.code(response["sql"], language='sql')
                if not response["df"].empty:
                    st.dataframe(response["df"])
                    display_download_section(response["df"], prompt, key_suffix="current")
                else:
                    st.write("A consulta não retornou resultados.")
            st.session_state.messages.append({"role": "assistant", "response": response})
