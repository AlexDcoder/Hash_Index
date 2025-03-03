import streamlit as st
import pandas as pd
from utils.utils import dividir_em_paginas, construir_indice, buscar_com_indice, table_scan, calcular_estatisticas

st.set_page_config('Project Hash', page_icon=':hash:')

st.title('_Hash Index Project_')

with st.sidebar:
    file_uploaded = st.file_uploader('Upload File', type=["txt"])

if file_uploaded is None:
    st.info('Escolha o arquivo para configurar o hash', icon='ℹ️')
    st.stop()

# Leitura do arquivo
palavras = file_uploaded.getvalue().decode("utf-8").splitlines()

with st.sidebar:
    with st.form('config_form'):
        st.markdown('**Hash Configuration**')
        page_size = st.number_input('Page Size', min_value=1)
        bucket_size = st.number_input('Bucket Size', min_value=1)
        num_buckets = st.number_input('Number of Buckets', min_value=1)
        col1, col2 = st.columns(2)
        with col1:
            value = st.text_input('Search Value', 'alan')
        submit = st.form_submit_button('Submit')

    if submit:
        paginas = dividir_em_paginas(palavras, page_size)
        indice = construir_indice(paginas, num_buckets, bucket_size)

        busca = buscar_com_indice(indice, value)
        scan = table_scan(paginas, value)
        stats = calcular_estatisticas(indice, len(palavras))

        st.subheader('Resultados')
        if busca['entry']:
            st.success(f"Chave encontrada na página {busca['entry']['pagina']}")
        else:
            st.error("Chave não encontrada")

        st.text(f"Custo de busca (com índice): {busca['custo']}")
        st.text(f"Tempo de busca (com índice): {busca['tempo']:.6f} seg")
        st.text(f"Custo do Table Scan: {scan['custo']}")
        st.text(f"Tempo do Table Scan: {scan['tempo']:.6f} seg")
        st.text(f"Taxa de colisões: {stats['taxaColisao']:.2f}%")
        st.text(f"Taxa de overflows: {stats['taxaOverflow']:.2f}%")
