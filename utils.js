function dividirEmPaginas(palavras, tamanhoPagina) {
    const paginas = [];
    let numeroPagina = 1;
    for (let i = 0; i < palavras.length; i += tamanhoPagina) {
      const registros = palavras.slice(i, i + tamanhoPagina);
      paginas.push(new Page(numeroPagina, registros));
      numeroPagina++;
    }
    return paginas;
}

function construirIndice(paginas, numBuckets, bucketSize) {
const indice = new HashIndex(numBuckets, bucketSize);
paginas.forEach(pagina => {
    pagina.registros.forEach(chave => {
    indice.adicionar(chave, pagina.numero);
    });
});
return indice;
}

function buscarComIndice(indice, chave) {
    const inicio = performance.now();
    const entry = indice.buscar(chave);
    // Simula custo: 1 acesso para o bucket + 1 para a página
    const custo = 2;
    const fim = performance.now();
    return { entry, custo, tempo: fim - inicio };
}

function tableScan(paginas, chave) {
const inicio = performance.now();
let custo = 0;
let paginaEncontrada = null;

for (let pagina of paginas) {
    custo++; // contagem de acesso (leitura de página)
    if (pagina.registros.includes(chave)) {
    paginaEncontrada = pagina;
    break;
    }
}
const fim = performance.now();
return { paginaEncontrada, custo, tempo: fim - inicio };
}

function calcularEstatisticas(indice, totalEntradas) {
    let colisoes = 0;
    let overflows = 0;
    indice.buckets.forEach(bucket => {
      if (bucket.entries.length > 1) {
        colisoes += bucket.entries.length - 1;
      }
      if (bucket.entries.length > bucket.maxTuplas) {
        overflows += bucket.entries.length - bucket.maxTuplas;
      }
    });
    const taxaColisao = (colisoes / totalEntradas) * 100;
    const taxaOverflow = (overflows / totalEntradas) * 100;
    return { taxaColisao, taxaOverflow };
}


  