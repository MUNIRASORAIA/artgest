document.addEventListener("DOMContentLoaded", function(event) {

    let produtos = document.querySelector('#bt-produtos');
    let materiasprimas = document.querySelector('#bt-materiasprimas');
    let gastos = document.querySelector('#bt-gastos');
    let fornecedores = document.querySelector('#bt-fornecedores');
    let instrucoes = document.querySelector('#bt-instrucoes');
    let prodvendidos = document.querySelector('#bt-prodvendidos');

    produtos.onclick = function () {
        // closeSubMenus();
        document.querySelector('#bt-produtos-registar').style.display = "block";
        document.querySelector('#bt-produtos-listar').style.display = "block";
    }

    materiasprimas.onclick = function () {
        // closeSubMenus();
        document.querySelector('#bt-materiasprimas-registar').style.display = "block";
        document.querySelector('#bt-materiasprimas-listar').style.display = "block";
    }

    gastos.onclick = function () {
        // closeSubMenus();
        document.querySelector('#bt-gastos-registar').style.display = "block";
        document.querySelector('#bt-gastos-listar').style.display = "block";
    }

    fornecedores.onclick = function () {
        // closeSubMenus();
        document.querySelector('#bt-fornecedores-registar').style.display = "block";
        document.querySelector('#bt-fornecedores-listar').style.display = "block";
    }

    instrucoes.onclick = function () {
        // closeSubMenus();
        document.querySelector('#bt-instrucoes-registar').style.display = "block";
        document.querySelector('#bt-instrucoes-listar').style.display = "block";
    }

    prodvendidos.onclick = function () {
        // closeSubMenus();
        document.querySelector('#bt-prodvendidos-registar').style.display = "block";
        document.querySelector('#bt-prodvendidos-listar').style.display = "block";
    }
});

// function closeSubMenus () {
//     document.querySelectorAll('.side-menu-inner').forEach(function (sub_menus) {
//         sub_menus.style.display = "None";
//         console.log('ola')
//     });
// }
