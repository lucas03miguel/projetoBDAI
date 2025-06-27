document.addEventListener('DOMContentLoaded', function () {
    const resultadosPesquisa = document.getElementById('resultados-pesquisa');
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const query = urlParams.get('q');

    if (resultadosPesquisa && query) {
        resultadosPesquisa.style.display = 'block';
    }
});

