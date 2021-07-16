document.addEventListener('DOMContentLoaded', function() {
    // Materia-prima producao
    const adicionar_mprod = document.querySelector('#bt-adicionar-mprod');
    const modal_mprod = document.querySelector('#modal-mprod');
    const inserir_mprod = document.querySelector('#bt-inserir-mprod');
    const form_mprod = document.querySelector('#form-mprod');
    const cancelar_mprod = document.querySelector('#bt-cancelar-mprod');
    const eliminar_mprod = document.querySelector('#bt-eliminar-mprod');
    // abrir o modal para criar gasto ao clicar em adicionar
    adicionar_mprod.onclick = function () {
        modal_mprod.style.display = "block";
    }

    // fechar o modal gasto ao clicar no botão cancelar
    cancelar_mprod.onclick = function () {
        modal_mprod.style.display = "none";
    }
});
