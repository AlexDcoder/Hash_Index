from src.bucket import Bucket
from dataclasses import dataclass, field

@dataclass
class HashIndex:
    num_buckets: int
    bucket_size: int
    buckets: list[Bucket] = field(init=False)
    total_colisoes: int = 0
    total_overflow: int = 0

    def __post_init__(self):
        self.buckets = [Bucket(self.bucket_size) for _ in range(self.num_buckets)]

    def funcao_hash(self, chave): 
        primo_base = 31
        primo_modulo = 1000003
        hash_value = sum(primo_base * [ord(c)**7 for c in chave]) % primo_modulo
        return hash_value % self.num_buckets

    def adicionar(self, chave, pagina):
        indice = self.funcao_hash(chave)
        bucket = self.buckets[indice]

        if len(bucket.entries) > 0:
            self.total_colisoes += 1  # Conta colisão sempre que um bucket já possui elementos

        if len(bucket.entries) < bucket.max_tuplas:
            bucket.adicionar_entrada(chave, pagina)
        else:
            bucket.adicionar_overflow(chave, pagina)
            self.total_colisoes += 1  # Conta colisões também no bucket de overflow
            self.total_overflow += 1  # Mantém a contagem de overflow

    def buscar(self, chave):
        indice = self.funcao_hash(chave)
        for entry in self.buckets[indice].entries + self.buckets[indice].overflow_entries:
            if entry["chave"] == chave:
                return entry
        return None
