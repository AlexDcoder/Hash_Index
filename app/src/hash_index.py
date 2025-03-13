from src.bucket import Bucket

class HashIndex:
    num_buckets: int
    bucket_size: int
    buckets: list[Bucket]

    def __init__(self, num_buckets: int, bucket_size: int):
        self.num_buckets = num_buckets
        self.bucket_size = bucket_size
        self.buckets = [Bucket(self.bucket_size) for _ in range(self.num_buckets)]

    def funcao_hash(self, chave): 
        # matrículas 2216986 2214674 2214667 221462 2218935
        # https://www.wolframalpha.com/input?i=next+prime+after+2216986221467422146672214622218935
        hash_value = 2216986_2214674_2214667_221462_22189_63
        for idx, char in enumerate(chave):
            idx = idx + 1
            char = ord(char)
            hash_value = idx * (char * hash_value) + hash_value
        return hash_value % self.num_buckets

    def adicionar(self, chave: str, pagina: int):
        indice = self.funcao_hash(chave)
        bucket = self.buckets[indice]
        bucket.adicionar(chave, pagina)

    def buscar(self, busca) -> int | None:
        indice = self.funcao_hash(busca)
        bucket = self.buckets[indice]
        for (chave, pagina) in bucket.entries.items():
            if chave == busca:
                return pagina
        return None