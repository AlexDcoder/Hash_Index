from src.page import Page
from src.hash_index import HashIndex
from time import perf_counter
from streamlit.runtime.uploaded_file_manager import UploadedFile
import math

def calcular_numero_buckets(num_tuplas: int, num_tuplas_bucket: int) -> int:
    '''
        Calcular o número de buckets necessários para a criação do índice hash.
    '''
    if num_tuplas == 0:
        return 1  # Pelo menos um bucket deve existir

    return math.ceil(num_tuplas / num_tuplas_bucket)

def dividir_em_paginas(palavras: UploadedFile, tamanho_pagina: int) -> list[Page]:
    '''
        Criar uma lista de páginas a partir do arquivo carregado.
    '''
    paginas = []
    numero_pagina = 1
    for i in range(0, len(palavras), tamanho_pagina):
        registros = palavras[i:i + tamanho_pagina]
        paginas.append(Page(numero_pagina, registros))
        numero_pagina += 1
    return paginas

def construir_indice(paginas: UploadedFile, num_buckets: int, bucket_size: int) -> HashIndex:
    '''
        Criar a estrutura do índice Hash com base nas informações do arquivo.
    '''
    indice = HashIndex(num_buckets, bucket_size)
    for pagina in paginas:
        for chave in pagina.registros:
            indice.adicionar(chave, pagina.numero)
    return indice

def buscar_com_indice(indice: HashIndex, chave: str) -> dict[str, any]:
    '''
        Buscar a chave na estrutura do índice Hash e retornar o custo e o tempo de busca.
    '''
    inicio = perf_counter()
    entry = indice.buscar(chave)
    custo = 1 if entry is not None else 0
    fim = perf_counter()
    return {"entry": entry, "custo": custo, "tempo": fim - inicio}

def table_scan(paginas: UploadedFile, chave: str) -> dict[str, any]:
    '''
        Realizar um table scan na lista de páginas e retornar estatísticas da busca.
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
        Calcular as estatísticas do índice Hash, incluindo taxa de colisões e taxa de overflows.
    '''
    colisoes = sum(
        len(bucket.entries) - 1 + len(bucket.overflow_entries)
        for bucket in indice.buckets if len(bucket.entries) > 1 or len(bucket.overflow_entries) > 0
    )

    overflows = sum(len(bucket.overflow_entries) for bucket in indice.buckets)

    taxa_colisao = (colisoes / total_entradas) * 100 if total_entradas else 0
    taxa_overflow = (overflows / total_entradas) * 100 if total_entradas else 0

    return {"taxaColisao": taxa_colisao, "taxaOverflow": taxa_overflow}
