from src.page import Page
from src.hash_index import HashIndex
from time import perf_counter

def dividir_em_paginas(palavras, tamanho_pagina):
    paginas = []
    numero_pagina = 1
    for i in range(0, len(palavras), tamanho_pagina):
        registros = palavras[i:i + tamanho_pagina]
        paginas.append(Page(numero_pagina, registros))
        numero_pagina += 1
    return paginas

def construir_indice(paginas, num_buckets, bucket_size):
    indice = HashIndex(num_buckets, bucket_size)
    for pagina in paginas:
        for chave in pagina.registros:
            indice.adicionar(chave, pagina.numero)
    return indice

def buscar_com_indice(indice, chave):
    inicio = perf_counter()
    entry = indice.buscar(chave)
    custo = 2
    fim = perf_counter()
    return {"entry": entry, "custo": custo, "tempo": fim - inicio}

def table_scan(paginas, chave):
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

def calcular_estatisticas(indice, total_entradas):
    colisoes = sum(len(bucket.entries) - 1 for bucket in indice.buckets if len(bucket.entries) > 1)
    overflows = sum(len(bucket.entries) - bucket.max_tuplas for bucket in indice.buckets if len(bucket.entries) > bucket.max_tuplas)
    taxa_colisao = (colisoes / total_entradas) * 100 if total_entradas else 0
    taxa_overflow = (overflows / total_entradas) * 100 if total_entradas else 0
    return {"taxaColisao": taxa_colisao, "taxaOverflow": taxa_overflow}
