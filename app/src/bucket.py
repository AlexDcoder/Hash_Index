from typing import Any  # Importa 'Any' do módulo 'typing' para permitir valores de qualquer tipo no dicionário de entradas.

class Bucket:  
    max_tuplas: int  
    entries: dict[str, Any]  
    next_bucket: "Bucket | None"

    def __init__(self, max_tuplas):
        self.max_tuplas = max_tuplas
        self.entries = {}
        self.next_bucket = None

    @property
    def overflow(self):  # Propriedade que calcula a quantidade de baldes extras devido a overflow.
        
        n_overflow = 0
        current = self
        
        while True:
            
            if current.next_bucket != None:  # Se houver um próximo balde (overflow),
                
                current = current.next_bucket  # Avança para o próximo balde.
                n_overflow += 1  # Incrementa o contador de overflows.
        
            else:
            
                return n_overflow  # Retorna o número total de baldes extras.

    @property
    def collisions(self):  # Propriedade que calcula o número total de colisões.
        
        n_collisions = 0
        current = self
        
        while True:
            
            if current.next_bucket != None:  # Se houver um próximo balde (indicando overflow),
                
                current = current.next_bucket  # Avança para o próximo balde.
                n_collisions += len(current.entries)  # Soma o número de entradas no balde de overflow.
        
            else:
            
                return n_collisions  # Retorna o total de colisões registradas.

    def adicionar(self, chave, pagina):  # Método para adicionar uma entrada no balde.
        
        current = self
        
        while True:
            
            if len(current.entries) <= current.max_tuplas:  # Se ainda houver espaço no balde atual, interrompe o loop.
                break
            
            if current.next_bucket == None:  # Se não houver um próximo balde (overflow), cria um novo balde.
                current.next_bucket = Bucket(current.max_tuplas)  # Cria um novo balde de overflow.

            if current.next_bucket != None:  # Se houver um próximo balde, avança para ele.
                current = current.next_bucket
            
        current.entries[chave] = pagina  # Insere a chave e o valor no balde apropriado.
