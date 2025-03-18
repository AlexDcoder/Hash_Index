from src.bucket import Bucket  # Importa a classe 'Bucket' do módulo 'src.bucket'.

class HashIndex:
    num_buckets: int
    bucket_size: int
    buckets: list[Bucket]

    def __init__(self, num_buckets: int, bucket_size: int):  # Construtor da classe, recebe a quantidade de baldes e o tamanho máximo de cada balde.
        self.num_buckets = num_buckets  # Inicializa o número de baldes.
        self.bucket_size = bucket_size  # Inicializa o tamanho máximo de cada balde.
        self.buckets = [Bucket(self.bucket_size) for _ in range(self.num_buckets)]  # Cria a lista de baldes, inicializando cada um com o tamanho especificado.

    def funcao_hash(self, chave):
        # matrículas 2216986 2214674 2214667 221462 2218935
        # https://www.wolframalpha.com/input?i=next+prime+after+2216986221467422146672214622218935
        hash_value = 2216986_2214674_2214667_221462_22189_63
        for idx, char in enumerate(chave):  # Percorre cada caractere da chave.
            idx = idx + 1  # O índice começa de 1 para evitar multiplicação por zero.
            char = ord(char)  # Obtém o valor numérico do caractere na tabela ASCII.
            hash_value = idx * (char * hash_value) + hash_value  # Aplica a fórmula de dispersão para gerar o valor hash.
        return hash_value % self.num_buckets  # Retorna o índice do bucket usando módulo com o número de baldes.

    def adicionar(self, chave: str, pagina: int):  # Método para adicionar um elemento ao índice hash.
        indice = self.funcao_hash(chave)  # Calcula o índice do balde onde a chave será armazenada.
        bucket = self.buckets[indice]  # Obtém o balde correspondente ao índice calculado.
        bucket.adicionar(chave, pagina)  # Insere a chave e a página dentro do balde.

    def buscar(self, busca) -> int | None:  # Método para buscar um valor associado a uma chave no índice hash.
        indice = self.funcao_hash(busca)  # Calcula o índice do balde onde a chave pode estar armazenada.
        bucket = self.buckets[indice]  # Obtém o balde correspondente ao índice calculado.
        for (chave, pagina) in bucket.entries.items():  # Percorre todas as entradas do balde.
            if chave == busca:  # Se a chave buscada for encontrada,
                return pagina  # Retorna o valor associado à chave.
        return None  # Se a chave não for encontrada, retorna None.