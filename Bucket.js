class Bucket {
    constructor(maxTuplas) {
      this.entries = [];
      this.maxTuplas = maxTuplas; // FR: número máximo de tuplas permitidas no bucket
    }
  
    adicionarEntrada(chave, pagina) {
      this.entries.push({ chave, pagina });
    }
  
    // Verifica se há overflow no bucket
    haOverflow() {
      return this.entries.length > this.maxTuplas;
    }
  }
  