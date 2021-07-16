document.addEventListener('DOMContentLoaded', function() {
    const modal_confirmacao = document.querySelector('#modal-confirmacao');
    const guardar = document.querySelector('#bt-guardar');
    const cancelar = document.querySelector('#bt-cancelar');

    // abrir o modal de confirmação ao clicar em registar
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

function mensagem_utilizador(mensagem) {
    alert(mensagem)
}

function submeter_form_principal() {
    document.querySelector('#form-principal-tpprod').submit();
}