from typing import Any

class Bucket:
    max_tuplas: int
    entries: dict[str, Any]
    next_bucket: "Bucket | None"

    def __init__(self, max_tuplas):
        self.max_tuplas = max_tuplas
        self.entries = {}
        self.next_bucket = None

    @property
    def overflow(self):
        
        n_overflow = 0
        current = self
        
        while True:
            
            if current.next_bucket != None:
                
                current = current.next_bucket
                n_overflow += 1
        
            else:
            
                return n_overflow

    @property
    def collisions(self):
        
        n_collisions = 0
        current = self
        
        while True:
            
            if current.next_bucket != None:
                
                current = current.next_bucket
                n_collisions += len(current.entries)
        
            else:
            
                return n_collisions
            
    def adicionar(self, chave, pagina):
        
        current = self
        
        while True:
            
            if len(current.entries) <= current.max_tuplas:
                break
            
            if current.next_bucket == None:
                current.next_bucket = Bucket(current.max_tuplas)

            if current.next_bucket != None:
                current = current.next_bucket
            
        current.entries[chave] = pagina
