from dataclasses import dataclass, field

# Onde será armazenado as entradas do índice hash.
@dataclass
class Bucket:
    max_tuples: int # número máximo de tuplas permitidas no bucket
    entries: list[str] = field(default_factory=list) # onde vai armazenar os objetos de entrada (cada entrada é uma tupla com chave e página)
    
    # Função para adicionar as entradas ao array "entries" do bucket
    def add_entry(self, key, value):
        # Adiciona um novo objeto com propriedades 'chave' (a chave de busca) e 'pagina' (o número da página onde a tupla está armazenada)
        self.entries.append((key, value))
    
    # Verifica se o bucket excedeu o número máximo de tuplas permitido (teve overflow)
    def has_overflow(self):
        # Retorna 'True' se o número de entradas no bucket len(self.entries) for maior que 'max_tuples'
        return len(self.entries) > self.max_tuples