function comprarEntrada(evento){
    swalAjaxInput(
        "Confirmar compra.",
        "Introduzca la cantidad de entradas a comprar.",
        "question",
        "number",
        "Cantidad",
        function(){
            console.log(evento);
            console.log($('input[placeholder="Cantidad"]').val()),
            swalExito();
        }
    )
}

function swalAjaxInput(titulo, texto, tipo, input, placeholder, ajax){
    Swal.fire({
        title: titulo,
        text: texto,
        type: tipo,
        input: input,
        inputPlaceholder: placeholder,
        inputValidator: (value) => {
            if (!value){
                return "La cantidad no puede estar vacía.";
            } else if (value<=0){
                return "Introduzca un número positivo";
            }
        },
        showConfirmButton: true,
        showCancelButton: true,
        confirmButtonColor: '#f03a47',
        cancelButtonColor: '#f2c078',
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.value){
            ajax();
        }
    });
}

function swalExito(){
    Swal.fire({
        title: "Éxito",
        text: "Transacción exitosa",
        type: "success",
        showConfirmButton: true,
        confirmButtonColor: '#f03a47',
        confirmButtonText: 'Aceptar',
    })
}

function swalError(){
    Swal.fire({
        title: "Error",
        text: "Hubo un error en tu solicitud.",
        type: "error",
        showConfirmButton: true,
        confirmButtonColor: '#f03a47',
        confirmButtonText: 'Aceptar',
    })
}