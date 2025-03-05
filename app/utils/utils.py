from src.page import Page
from src.hash_index import HashIndex
from time import perf_counter
from streamlit.runtime.uploaded_file_manager import UploadedFile

def dividir_em_paginas(palavras: UploadedFile, tamanho_pagina: int) -> list[Page]:
    '''
        Usar informações do arquivo e criar uma lista de páginas com um tamanho específico
    '''
    paginas = []
    numero_pagina = 1
    for i in range(0, len(palavras), tamanho_pagina):
        registros = palavras[i:i + tamanho_pagina]
        paginas.append(Page(numero_pagina, registros))
        numero_pagina += 1
    return paginas

def construir_indice(
    paginas: UploadedFile, num_buckets: int, 
    bucket_size: int) -> HashIndex:
    '''
        Criar a estrutura do índice Hash com base nas informações do arquivo e
        do formulário.
    '''
    indice = HashIndex(num_buckets, bucket_size)
    for pagina in paginas:
        for chave in pagina.registros:
            indice.adicionar(chave, pagina.numero)
    return indice

def buscar_com_indice(indice: HashIndex, chave: str) -> dict[str, any]:
    '''
        Buscar a chave na estrutura do índice Hash, retornando qual a entrada,
        sendo ela a palavra e a página dessa palavra, o cutos e o tempo de 
        busca
    '''
    inicio = perf_counter()
    entry = indice.buscar(chave)
    custo = 2
    fim = perf_counter()
    return {"entry": entry, "custo": custo, "tempo": fim - inicio}

def table_scan(paginas: UploadedFile, chave: str) -> dict[str, any]:
    '''
        Realizar um table scan na lista de páginas, percorrendo cada página
        e verificando se a chave está presente na página. Retorna qual a página
        a chave foi encontrada, o custo e o tempo de busca.
    '''
    inicio = perf_counter()
    custo = 0
    pagina_encontrada = None
    for pagina in paginas:
        custo += 1
        if chave in pagina.registros:
            pagina_encontrada = pagina
            break
    fim = perf_counter()
    return {"pagina_encontrada": pagina_encontrada, "custo": custo, "tempo": fim - inicio}

def calcular_estatisticas(indice: HashIndex, total_entradas: int) -> dict[str, any]:
    '''
        Calcular as estatísticas do índice Hash, incluindo a taxa de colisões e a
        taxa de overflows.
    '''
    colisoes = sum(len(bucket.entries) - 1 for bucket in indice.buckets if len(bucket.entries) > 1)
    overflows = sum(len(bucket.entries) - bucket.max_tuplas for bucket in indice.buckets if len(bucket.entries) > bucket.max_tuplas)
    taxa_colisao = (colisoes / total_entradas) * 100 if total_entradas else 0
    taxa_overflow = (overflows / total_entradas) * 100 if total_entradas else 0
    return {"taxaColisao": taxa_colisao, "taxaOverflow": taxa_overflow}
