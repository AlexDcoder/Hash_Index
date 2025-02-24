class HashIndex {
    constructor(numBuckets, bucketSize) {
      this.numBuckets = numBuckets;
      this.bucketSize = bucketSize; // FR
      this.buckets = Array.from({ length: numBuckets }, () => new Bucket(bucketSize));
    }
  
    // Função hash simples: soma dos códigos dos caracteres modulo o número de buckets
    funcaoHash(chave) {
      let soma = 0;
      for (let i = 0; i < chave.length; i++) {
        soma += chave.charCodeAt(i);
      }
      return soma % this.numBuckets;
    }
  
    // Adiciona uma entrada ao índice
    adicionar(chave, pagina) {
      const indice = this.funcaoHash(chave);
      this.buckets[indice].adicionarEntrada(chave, pagina);
    }
  
    // Busca a entrada de uma chave
    buscar(chave) {
      const indice = this.funcaoHash(chave);
      return this.buckets[indice].entries.find(entry => entry.chave === chave);
    }
  }
  