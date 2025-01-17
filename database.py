import psycopg2
from psycopg2 import sql
from contrato import Vendas
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def salvar_no_postgres(dados: Vendas):
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()

        # Query de inserção
        insert_query = sql.SQL(
            "INSERT INTO vendas (email, data, valor, quantidade, produto) VALUES (%s, %s, %s, %s, %s)"
        )
        
        # Executar a query com os valores passados
        cursor.execute(insert_query, (
            dados.email, 
            dados.data, 
            dados.valor, 
            dados.quantidade,
            dados.produto  # Removido .value, presumo que produto seja uma string
        ))
        
        # Commit para salvar as mudanças
        conn.commit()

        # Fechar o cursor e conexão
        cursor.close()
        conn.close()

        # Mensagem de sucesso
        st.success("Dados salvos com sucesso no banco de dados")

    except Exception as e:
        st.error(f"Erro ao salvar dados no banco de dados: {e}")
