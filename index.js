document.getElementById('buildIndexBtn').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    const pageSize = parseInt(document.getElementById('pageSize').value);
    if (fileInput.files.length === 0 || !pageSize) {
      alert('Selecione um arquivo e informe o tamanho da página.');
      return;
    }
  
    const file = fileInput.files[0];
    const reader = new FileReader();
  
    reader.onload = function(event) {
      // Cada linha é uma palavra
      const palavras = event.target.result.split(/\r?\n/).filter(linha => linha.trim() !== '');
      const paginas = dividirEmPaginas(palavras, pageSize);
  
      // Exemplo: calcular número de buckets (NB > NR/FR)
      // Aqui, podemos definir bucketSize (FR) e calcular um número de buckets adequado
      const bucketSize = 5; // por exemplo
      const totalEntradas = palavras.length;
      const numBuckets = Math.ceil(totalEntradas / bucketSize) + 1; // ou outra lógica
  
      window.paginas = paginas; // armazenando globalmente para acesso nas buscas
      window.indice = construirIndice(paginas, numBuckets, bucketSize);
      
      // Exiba a primeira e a última página na interface
      document.getElementById('result').innerHTML = `
        <h3>Páginas Carregadas</h3>
        <p><strong>Primeira Página (${paginas[0].numero}):</strong> ${paginas[0].registros.join(', ')}</p>
        <p><strong>Última Página (${paginas[paginas.length - 1].numero}):</strong> ${paginas[paginas.length - 1].registros.join(', ')}</p>
      `;
      
      // Calcular e exibir estatísticas iniciais
      const stats = calcularEstatisticas(window.indice, totalEntradas);
      document.getElementById('result').innerHTML += `
        <p>Taxa de Colisões: ${stats.taxaColisao.toFixed(2)}%</p>
        <p>Taxa de Overflows: ${stats.taxaOverflow.toFixed(2)}%</p>
      `;
    };
  
    reader.readAsText(file);
  });
  
  document.getElementById('searchBtn').addEventListener('click', () => {
    const chave = document.getElementById('searchKey').value;
    if (!chave || !window.indice) {
      alert('Informe uma chave e construa o índice primeiro.');
      return;
    }
    
    const resultado = buscarComIndice(window.indice, chave);
    let mensagem = '';
    if (resultado.entry) {
      mensagem += `<p>Chave "${chave}" encontrada na página ${resultado.entry.pagina}.<br>`;
    } else {
      mensagem += `<p>Chave "${chave}" não encontrada usando o índice.<br>`;
    }
    mensagem += `Custo (acessos simulados): ${resultado.custo} <br>`;
    mensagem += `Tempo: ${resultado.tempo.toFixed(2)} ms</p>`;
    
    document.getElementById('result').innerHTML += mensagem;
  });
  
  document.getElementById('tableScanBtn').addEventListener('click', () => {
    const chave = document.getElementById('searchKey').value;
    if (!chave || !window.paginas) {
      alert('Informe uma chave e construa o índice primeiro.');
      return;
    }
    
    const resultado = tableScan(window.paginas, chave);
    let mensagem = '';
    if (resultado.paginaEncontrada) {
      mensagem += `<p>Chave "${chave}" encontrada na página ${resultado.paginaEncontrada.numero} via Table Scan.<br>`;
    } else {
      mensagem += `<p>Chave "${chave}" não encontrada via Table Scan.<br>`;
    }
    mensagem += `Custo (páginas lidas): ${resultado.custo} <br>`;
    mensagem += `Tempo: ${resultado.tempo.toFixed(2)} ms</p>`;
    
    document.getElementById('result').innerHTML += mensagem;
});
  