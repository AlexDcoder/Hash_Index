//Onde será armazenado as entradas do índice hash.
class Bucket {
  constructor(maxTuplas) {
    this.entries = []; //onde vai armazenar os objetos de entrada (cada entrada é uma tupla com chave e página)
    this.maxTuplas = maxTuplas; // número máximo de tuplas permitidas no bucket
  }

  // função para adicionar as entradas ao array "entries" do bucket
  adicionarEntrada(chave, pagina) { 
    //adiciona um novo objeto com propriedades 'chave' (a chave de busca) e 'pagina' (o número da página onde a tupla está armazenada)
    this.entries.push({ chave, pagina }); 
  }

  // verifica se o bucket excedeu o número máximo de tuplas permitido (teve overflow)
  haOverflow() {
    // retorna 'true' se o número de entradas no bucket (this.entries.length) for maior que 'maxTuplas'
    return this.entries.length > this.maxTuplas; 
  }
}
  