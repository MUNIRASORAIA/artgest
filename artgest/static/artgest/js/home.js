document.addEventListener('DOMContentLoaded', function() {

    // Registar Utilizador
    let registar = document.querySelector('#bt-registar');
    let modal_registar = document.querySelector('#modal-registar');
    let cancelar_registar = document.querySelector('#bt-cancelar-registar');


    // abrir o modal para registar utilizador ao clicar em registar
    registar.onclick = function () {
        modal_registar.style.display = "block";
    }

    // fechar o modal registar ao clicar no botão cancelar
    cancelar_registar.onclick = function () {
        modal_registar.style.display = "none";
    }



    // fechar modal de confirmação ao clicar em qualquer parte fora do modal
    window.onclick = function (event) {
        if (event.target == modal_registar) {
            modal_registar.style.display = "none";
        }
    }
});
