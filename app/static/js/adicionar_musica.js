function toggleArtistasConvidados() {
    const featSelect = document.getElementById('feat-select');
    const convidadosDiv = document.getElementById('artistas-convidados-div');

    if (featSelect.value === 'sim') {
        convidadosDiv.style.display = 'block';
    } else {
        convidadosDiv.style.display = 'none';
    }
}
