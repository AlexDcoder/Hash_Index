import os
import streamlit as st
import pandas as pd
from utils.utils import calcular_numero_buckets,dividir_em_paginas, construir_indice, buscar_com_indice, table_scan, calcular_estatisticas
import plotly.express as px

# Configurações da página
st.set_page_config('Project Hash', page_icon=':hash:', layout='wide')

st.title('_Hash Index Project_')

# Variáveis a serem salvas durante a execução
if 'df_response' not in st.session_state:
    st.session_state.df_response = pd.DataFrame(columns=[
        'page_size', 'bucket_size', 'num_buckets', 'search_value',
        'custo_busca_com_indice', 'tempo_busca_com_indice',
        'custo_scan', 'tempo_scan', 'taxa_colisoes', 'taxa_overflows',
        'status_encontrado'
    ])

with st.sidebar:
    file_uploaded = st.file_uploader('**Upload File**', type=["txt"])

if file_uploaded is None:
    st.info('Escolha o arquivo para configurar o hash', icon='ℹ️')
    st.stop()

# Leitura do arquivo
palavras = file_uploaded.getvalue().decode("utf-8").splitlines()

with st.sidebar:
    # Formulário para configurações do Índice Hash
    with st.expander('_**Hash Configuration**_', icon='⚙️'):
        with st.form(key='config_form'):
            page_size = st.number_input('Page Size', min_value=1)
            bucket_size = st.number_input('Bucket Size', min_value=1)
            col1, col2 = st.columns(2)
            with col1:
                value = st.text_input('Search Value', 'Alan')
            submit = st.form_submit_button('Submit', use_container_width=True)
    
if submit:
    # Executando as funções após a submissão do primeiro formulário
    paginas = dividir_em_paginas(palavras, page_size)
    # Exibir a primeira e a última página carregada
    if paginas:
        st.subheader("📄 Páginas Carregadas")
        
        primeira_pagina = paginas[0]
        ultima_pagina = paginas[-1]

        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Primeira Página (Número {primeira_pagina.numero})**")
            st.text("\n".join(primeira_pagina.registros))

        with col2:
            st.markdown(f"**Última Página (Número {ultima_pagina.numero})**")
            st.text("\n".join(ultima_pagina.registros))

    num_buckets = calcular_numero_buckets(len(palavras), bucket_size)
    indice = construir_indice(paginas, num_buckets, bucket_size)

    busca = buscar_com_indice(indice, value)
    scan = table_scan(paginas, value)
    stats = calcular_estatisticas(indice, len(palavras))
    encontrado = True
    
    with st.sidebar:
        if busca['entry']:
            st.success(f"Chave encontrada na página {busca['entry']['pagina']} ✅")
        else:
            st.error("Chave não encontrada ❌")
            encontrado = False

        st.text(f"Custo de busca (com índice): {busca['custo']}")
        st.text(f"Tempo de busca (com índice): {busca['tempo']:.6f} seg")
        st.text(f"Custo do Table Scan: {scan['custo']}")
        st.text(f"Tempo do Table Scan: {scan['tempo']:.6f} seg")
        st.text(f"Taxa de colisões: {stats['taxaColisao']:.2f}%")
        st.text(f"Taxa de overflows: {stats['taxaOverflow']:.2f}%")
        
    PERFORMANCE_PATH = './report/performance.csv'

    response = {
        'page_size': [page_size],
        'bucket_size': [bucket_size],
        'num_buckets': [num_buckets],
        'search_value': [value],
        'custo_busca_com_indice': [busca['custo']],
        'tempo_busca_com_indice': [busca['tempo']],
        'custo_scan': [scan['custo']],
        'tempo_scan': [scan['tempo']],
        'taxa_colisoes': [stats['taxaColisao']],
        'taxa_overflows': [stats['taxaOverflow']],
        'status_encontrado': True if encontrado else False
    }

    novo_df = pd.DataFrame(response)
    st.session_state.df_response = pd.concat([st.session_state.df_response, novo_df], ignore_index=True)

with st.sidebar:
    with st.form(key='performance_form'):
        selected_words = st.selectbox(
            'Selelecione um elemento para pesquisar seu desempenho', 
            st.session_state.df_response['search_value'].unique())
        selected_submit = st.form_submit_button('Search', use_container_width=True)

with st.expander('Performance', icon='📊'):
    st.dataframe(st.session_state.df_response, use_container_width=True, hide_index=True)

if selected_submit:
    st.subheader(f'Selecionado: _{selected_words}_ ')
    df_selected = st.session_state.df_response.query(f'search_value == "{selected_words}"')
    df_selected_performance = pd.DataFrame(
        {
            'search_value': df_selected['search_value'].values.tolist(),
            'scan_performance': (df_selected['custo_busca_com_indice'] / df_selected['tempo_busca_com_indice']).tolist(), 
            'indice_performance': (df_selected['custo_scan'] / df_selected['tempo_scan']).tolist()
        }
    )

    col3, col4 = st.columns(2, vertical_alignment='center')
    with col3:
        st.plotly_chart(
            px.line(
                df_selected_performance,
                x= df_selected_performance.index,
                y=['scan_performance', 'indice_performance'],
                title='Comparação de Desempenho',
                log_y=True, markers=True
            )
        )
    with col4:
        with st.expander('_**Comparação de Desempenho**_', icon='💾'):
            st.dataframe(df_selected.reset_index().drop('index', axis=1)[
                ['search_value', 'page_size', 'bucket_size', 'num_buckets']],
                use_container_width=True)
        col5, col6 = st.columns(2)
        col7, col8 = st.columns(2)
        with col5:
            st.metric(
                label='Média de Colisões',
                value=f'{df_selected["taxa_colisoes"].mean():.2f}%',
                border=True,
                delta=f'{df_selected["taxa_colisoes"].std():.2f}%'\
                    if df_selected["taxa_overflows"].std() != 0 else None,
            )
        with col6:
            st.metric(
                label='Média de Overflows',
                value=f'{df_selected["taxa_overflows"].mean():.2f}%',
                border=True,
                delta=f'{df_selected["taxa_overflows"].std():.2f}%' \
                    if df_selected["taxa_overflows"].std() != 0 else None,
            )
        with col7:
            st.metric(
                label='Média de Scan',
                value=f'{df_selected_performance["scan_performance"].mean():.2f}',
                border=True,
                delta=f'{df_selected_performance["scan_performance"].std():.2f}' \
                    if df_selected_performance["scan_performance"].std() != 0 else None,
            )
        with col8:
            st.metric(
                label='Média de Busca',
                value=f'{df_selected_performance["indice_performance"].mean():.2f}',
                border=True,
                delta=f'{df_selected_performance["indice_performance"].std():.2f}' \
                    if df_selected["taxa_overflows"].std() != 0 else None,
                )