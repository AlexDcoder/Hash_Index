from dataclasses import dataclass, field
from typing import Any

@dataclass
class Bucket:
    max_tuplas: int  # Número máximo de tuplas permitidas no bucket
    entries: list[dict[str, Any]] = field(default_factory=list)  # Entradas principais
    overflow_entries: list[dict[str, Any]] = field(default_factory=list)  # Lista de overflow

    def adicionar_entrada(self, chave, pagina):
        self.entries.append({"chave": chave, "pagina": pagina})

    def adicionar_overflow(self, chave, pagina):
        self.overflow_entries.append({"chave": chave, "pagina": pagina})  # Encadeamento separado

    def has_overflow(self):
        return len(self.entries) > self.max_tuplas or len(self.overflow_entries) > 0
