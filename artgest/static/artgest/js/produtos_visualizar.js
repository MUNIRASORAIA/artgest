document.addEventListener('DOMContentLoaded', function() {
    const modal_confirmacao = document.querySelector('#modal-confirmacao');
    const cancelar = document.querySelector('#bt-cancelar');

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

function muda_url (url) {
    const preco_valor = document.querySelector('#preco-valor');
    url = url.replace(-9999, preco_valor.value)
    const modal_confirmacao = document.querySelector('#modal-confirmacao');
    modal_confirmacao.style.display = "block";
    let guardar_confirmacao = document.querySelector('#bt-guardar-confirmacao');
    guardar_confirmacao.href = url;
}