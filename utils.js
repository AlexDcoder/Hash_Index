// função que divide um array de palavras em páginas, de acordo com o tamanho definido para cada página
function dividirEmPaginas(palavras, tamanhoPagina) {
  const paginas = []; // array para armazenar as paginas resultantes
  let numeroPagina = 1;
  for (let i = 0; i < palavras.length; i += tamanhoPagina) { //pula de "tamanhoPagina" em "tamanhoPagina"
    // extrai um pedaço do array de palavras, começando em "i" até "i + tamanhoPagina"
    const registros = palavras.slice(i, i + tamanhoPagina);
    // cria uma instância de Page com o número da página atual e os registros extraídos
    paginas.push(new Page(numeroPagina, registros));
    numeroPagina++; //incrementa contador
  }
  return paginas;
}

// função que constrói o índice hash a partir das páginas criadas
function construirIndice(paginas, numBuckets, bucketSize) {
  // cria uma instância de HashIndex, passando o número de buckets e o tamanho de cada bucket
  const indice = new HashIndex(numBuckets, bucketSize);

  paginas.forEach(pagina => { // para cada página do array de páginas
    pagina.registros.forEach(chave => { // para cada chave presente na página
      // adiciona a chave e o número da página ao índice hash
      indice.adicionar(chave, pagina.numero);
    });
  });
  return indice;
}

// função que realiza a busca de uma chave usando o índice hash
function buscarComIndice(indice, chave) {
  // registra o tempo inicial
  const inicio = performance.now();
  // busca a entrada correspondente à chave no índice usando o método buscar do HashIndex
  const entry = indice.buscar(chave);
  // simula o custo da busca: 1 acesso para o bucket e 1 acesso para a página
  const custo = 2;
  // registra o tempo final
  const fim = performance.now();

  return { entry, custo, tempo: fim - inicio };
}

// função que realiza um table scan nas páginas para encontrar uma chave.
function tableScan(paginas, chave) {
  // registra o tempo inicial
  const inicio = performance.now();
  // inicializa o custo da operação (contador de páginas lidas) com 0
  let custo = 0;
  let paginaEncontrada = null;

  // percorre cada página do array de páginas
  for (let pagina of paginas) {
    custo++; // incrementa o contador para cada página lida
    if (pagina.registros.includes(chave)) {//se a chave estiver presente no registro da página
      paginaEncontrada = pagina; // armazena a página
      break;
    }
  }
  // registra o tempo final
  const fim = performance.now();

  return { paginaEncontrada, custo, tempo: fim - inicio };
}

// função que calcula estatísticas do índice
function calcularEstatisticas(indice, totalEntradas) {
  let colisoes = 0; // contador de colisões
  let overflows = 0; // contador de overflows

  indice.buckets.forEach(bucket => { //para cada bucket em indice
    if (bucket.entries.length > 1) { //se houver mais de uma entrada
      colisoes += bucket.entries.length - 1; // incrementa a qntd de colisões (número de entradas além da primeira)
    }

    if (bucket.entries.length > bucket.maxTuplas) { // se o número de entradas no bucket ultrapassar o tamanho máximo permitido (maxTuplas)
      overflows += bucket.entries.length - bucket.maxTuplas; //incrementa a qntd de overflows (número de entradas que excedem o limite)
    }
  });

  // calcula a taxa de colisões
  const taxaColisao = (colisoes / totalEntradas) * 100;

  // calcula a taxa de overflows
  const taxaOverflow = (overflows / totalEntradas) * 100;

  return { taxaColisao, taxaOverflow };
}