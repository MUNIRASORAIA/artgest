document.addEventListener('DOMContentLoaded', function() {

    let modal_confirmacao = document.querySelector('#modal-confirmacao');
    let cancelar = document.querySelector('#bt-cancelar');

    // fechar o modal ao clicar no botão cancelar
    if (cancelar) {
        cancelar.onclick = function () {
            modal_confirmacao.style.display = "none";
        }
    }

    // fechar modal de confirmação ao clicar em qualquer parte fora do modal
    window.onclick = function (event) {
        if (event.target == modal_confirmacao) {
            modal_confirmacao.style.display = "none";
        }
    }
});

function eliminar_registo (url) {
    console.log('url: ' + url);
    let modal_confirmacao = document.querySelector('#modal-confirmacao');
    modal_confirmacao.style.display = "block";

    let eliminar = document.querySelector('#bt-eliminar');
    eliminar.href = url;
    console.log(eliminar);
}