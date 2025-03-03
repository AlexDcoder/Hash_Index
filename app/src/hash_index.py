from src.bucket import Bucket
from dataclasses import dataclass, field

@dataclass
class HashIndex:
    num_buckets: int
    bucket_size: int
    buckets: list[Bucket]= field(init=False)
    total_colisoes: int = 0
    total_overflow: int = 0
    
    def __post_init__(self):
        self.buckets = [Bucket(self.bucket_size) for _ in range(self.num_buckets)]

    def funcao_hash(self, chave):
        return sum(ord(c) for c in chave) % self.num_buckets

    def adicionar(self, chave, pagina):
        indice = self.funcao_hash(chave)
        bucket = self.buckets[indice]

        if len(bucket.entries) > 0:
            self.total_colisoes += 1
        
        bucket.adicionar_entrada(chave, pagina)

        if bucket.has_overflow():
            self.total_overflow += 1

    def buscar(self, chave):
        indice = self.funcao_hash(chave)
        for entry in self.buckets[indice].entries:
            if entry["chave"] == chave:
                return entry
        return None
