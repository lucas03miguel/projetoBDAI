// Lista de músicas selecionadas
let musicasSelecionadas = [];

// Função para adicionar música à lista da playlist
function adicionarMusica(ismn, titulo) {
    // Evita duplicação na lista
    if (!musicasSelecionadas.some(musica => musica.ismn === ismn)) {
        musicasSelecionadas.push({ ismn, titulo });
        console.log('Música adicionada:', titulo);
        atualizarLista();
    }
}

// Função para remover música da lista da playlist
function removerMusica(ismn) {
    musicasSelecionadas = musicasSelecionadas.filter(m => m.ismn !== ismn);
    atualizarLista();
}

// Atualizar a lista de músicas selecionadas na interface
function atualizarLista() {
    const listaDiv = document.getElementById('lista-musicas');
    listaDiv.innerHTML = '';

    musicasSelecionadas.forEach(musica => {
        const item = document.createElement('div');
        item.className = 'musica-item';
        item.innerHTML = `
            <span>${musica.titulo}</span>
            <button 
                type="button" 
                class="btn-remover" 
                onclick="removerMusica(${musica.ismn})">
                Remover
            </button>
        `;
        listaDiv.appendChild(item);
    });

    const hiddenField = document.getElementById('musicas-selecionadas');
    hiddenField.value = JSON.stringify(musicasSelecionadas.map(m => m.ismn));
}

// Função para realizar a pesquisa de músicas
function pesquisarMusicas() {
    const query = document.getElementById('pesquisa-musicas').value.toLowerCase();
    const resultadosDiv = document.getElementById('resultados-pesquisa');
    resultadosDiv.innerHTML = ''; // Limpa os resultados anteriores

    if (query) {
        fetch(`/app/pesquisar_musicas?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.musicas && data.musicas.length > 0) {
                    data.musicas.forEach(musica => {
                        const item = document.createElement('div');
                        item.className = 'musica-item';
                        item.innerHTML = `
                            <span>${musica.titulo}</span>
                            <button 
                                type="button" 
                                class="btn-adicionar" 
                                onclick="adicionarMusica(${musica.ismn}, '${musica.titulo}')">
                                +
                            </button>
                        `;
                        resultadosDiv.appendChild(item);
                    });
                } else {
                    resultadosDiv.innerHTML = '<p>Nenhuma música encontrada.</p>';
                }
            })
            .catch(error => {
                console.error('Erro ao buscar músicas:', error);
            });
    }
}

