document.addEventListener('DOMContentLoaded', function() {

    let modal_confirmacao = document.querySelector('#modal-confirmacao');
    let guardar = document.querySelector('#bt-guardar');
    let cancelar = document.querySelector('#bt-cancelar');

    // abrir o modal de confirmação ao clicar em guardar
    guardar.onclick = function () {
        modal_confirmacao.style.display = "block";
    }

    // fechar o modal ao clicar no botão cancelar
    cancelar.onclick = function () {
        modal_confirmacao.style.display = "none";
    }

    // fechar modal de confirmação ao clicar em qualquer parte fora do modal
    window.onclick = function (event) {
        if (event.target == modal_confirmacao) {
            modal_confirmacao.style.display = "none";
        }
    }
});