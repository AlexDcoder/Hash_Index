from dataclasses import dataclass, field

@dataclass
class Bucket:
    max_tuplas: int # número máximo de tuplas permitidas no bucket
    entries: list[str] = field(default_factory=list) # onde vai armazenar os objetos de entrada (cada entrada é uma tupla com chave e página)
    
    def adicionar_entrada(self, chave, pagina):
        self.entries.append({"chave": chave, "pagina": pagina})

    def has_overflow(self):
        return len(self.entries) > self.max_tuplas
