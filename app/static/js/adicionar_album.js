// Declaração global de discografia para evitar falhas
let discografia = [];

try {
    // Pega os dados de discografia do template
    const rawDiscografia = document.getElementById("discografia-data").textContent.trim();
    if (rawDiscografia) {
        discografia = JSON.parse(rawDiscografia); // Processa se for válido
        console.log("Discografia carregada:", discografia);
    } else {
        console.log("Discografia está vazia.");
    }
} catch (error) {
    console.error("Erro ao processar discografia:", error);
}

// Gera os campos dinâmicos para músicas
function gerarCamposMusicas() {
    const numMusicas = parseInt(document.getElementById("numero-musicas").value, 10);
    const container = document.getElementById("musicas-container");
    container.innerHTML = ""; // Limpa os campos anteriores

    if (isNaN(numMusicas) || numMusicas <= 0) {
        container.innerHTML = "<p>Por favor, insira um número válido de músicas.</p>";
        return;
    }

    for (let i = 1; i <= numMusicas; i++) {
        const musicaDiv = document.createElement("div");
        musicaDiv.className = "musica";

        let options = `<option value="" disabled selected>Selecione uma música</option>`;
        discografia.forEach(musica => {
            options += `<option value="${musica.ismn}">${musica.titulo}</option>`;
        });

        musicaDiv.innerHTML = `
            <h3>Música ${i}</h3>
            <label>Escolher da Discografia:</label>
            <select class="styled-select" name="musica_discografia_${i}">
                ${options}
            </select>
            <p>Ou</p>
            <h4>Adicionar Nova Música:</h4>
            <label>Título:</label>
            <input type="text" name="titulo_${i}" placeholder="Insira o título da música">
            <label>Género:</label>
            <input type="text" name="genero_${i}" placeholder="Insira o género da música">
            <label>Duração (min:seg):</label>
            <input type="time" step="1" name="duracao_${i}">

        `;
        container.appendChild(musicaDiv);
    }
}
