class HashIndex {
  constructor(numBuckets, bucketSize) {
    // número total de buckets que serão criados
    this.numBuckets = numBuckets; 
    // tamanho máximo de cada bucket (a quantidade de tuplas permitidas em cada bucket)
    this.bucketSize = bucketSize; 
    // cria um array com a quantidade de elementos definido em "numBucket" 
    // para cada posição desse array é instanciado um novo objeto Bucket com o tamanho máximo definido (bucketSize)
    this.buckets = Array.from({ length: numBuckets }, () => new Bucket(bucketSize));
  }

  // define o método funcaoHash que recebe uma chave e retorna um índice correspondente ao bucket onde a chave deve ser armazenada
  funcaoHash(chave) {
    let soma = 0;
    for (let i = 0; i < chave.length; i++) {
      soma += chave.charCodeAt(i);
    }
    return soma % this.numBuckets;
  }

  // associa a chave à página
  adicionar(chave, pagina) {
    // calcula o índice do bucket correspondente à chave
    const indice = this.funcaoHash(chave);
    // acessa o bucket na posição calculada e insere a nova entrada 
    this.buckets[indice].adicionarEntrada(chave, pagina);
  }

  // procura uma entrada específica no índice com base na chave
  buscar(chave) {
    // calcula o índice do bucket correspondente à chave
    const indice = this.funcaoHash(chave);
    // dentro do bucket, procura a entrada cujo atributo "chave" seja igual à chave procurada
    return this.buckets[indice].entries.find(entry => entry.chave === chave);
  }
}
  