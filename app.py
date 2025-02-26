import streamlit as st
import pandas as pd

st.set_page_config('Project Hash', page_icon=':hash:')

st.title('_Hash Index Project_')

with st.sidebar:
    file_uploaded = st.file_uploader('Upload File')

if file_uploaded is None:
    st.info('Escolha o arquivo para configurar o hash')
    st.stop()
    
with st.sidebar:
    with st.form('config_form'):
        st.markdown('**Hash Configuration**')
        page_size = st.number_input('Page Size', min_value=1)
        bucket_size = st.number_input('Bucket Size', min_value=1)
        col1, col2 = st.columns(2)
        with col1:
            index = st.number_input('Index', min_value=0)
        with col2:
            value = st.text_input('Value', 'alan')
        submit = st.form_submit_button('Submit')
    if submit:
        print(page_size, bucket_size, index, value)

