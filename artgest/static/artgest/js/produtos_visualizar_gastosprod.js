document.addEventListener('DOMContentLoaded', function() {
    // Gasto Producao
    const adicionar_gasto_prod = document.querySelector('#bt-adicionar-gasto-prod');
    const modal_gasto_prod = document.querySelector('#modal-gasto');
    const inserir_gasto_prod = document.querySelector('#bt-inserir-gasto-prod');
    const form_gasto_prod = document.querySelector('#form-gasto-prod');
    const cancelar_gasto_prod = document.querySelector('#bt-cancelar-gasto-prod');
    const eliminar_gasto = document.querySelector('#bt-eliminar-gasto-prod');

    // abrir o modal para criar gasto ao clicar em adicionar
    adicionar_gasto_prod.onclick = function () {
        modal_gasto_prod.style.display = "block";
    }

    // fechar o modal gasto ao clicar no botão cancelar
    cancelar_gasto_prod.onclick = function () {
        modal_gasto_prod.style.display = "none";
    }

});
