document.addEventListener('DOMContentLoaded', function() {
    // Produção
    let adicionar_prod = document.querySelector('#bt-adicionar-producao');
    let editar_prod = document.querySelector('#bt-editar-producao');
    let modal_prod = document.querySelector('#modal-prod');
    let custo_producao = document.querySelector('#custo-producao');
    let cancelar_prod = document.querySelector('#bt-cancelar-prod');
    let producao_conteudo = document.querySelector('#producao-conteudo');

    // abrir o modal para criar produção ao clicar em adicionar
    adicionar_prod.onclick = function () {
        modal_prod.style.display = "block";
    }

    // fechar o modal produção ao clicar no botão cancelar
    cancelar_prod.onclick = function () {
        modal_prod.style.display = "none";
    }

//    custo_producao.addEventListener('change', (event) => {
//        if (custo_producao.value == '') {
//            adicionar_prod.style.display = "block";
//            editar_prod.style.display = "none";
//        }
//        else {
//            editar_prod.style.display = "block";
//            adicionar_prod.style.display = "none";
//        }
//    });
});
