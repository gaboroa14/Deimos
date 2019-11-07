var poplogin = false;
var popsignUp = false;

function comprarEntrada(evento){
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    swalAjaxInput(
        "Confirmar compra.",
        "Introduzca la cantidad de entradas a comprar.",
        "question",
        "number",
        "Cantidad",
        function(){
            $.ajax({
                url: '/ajax/comprar_entrada/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': token,
                    'evento': evento,
                    'cantidad': $('input[placeholder="Cantidad"]').val(),
                },
                dataType: 'json',
                success: function(data) {
                    if (data.exito){
                        Swal.fire("Éxito","Entrada comprada exitosamente.","success",timer=1000);
                        setTimeout(function(){
                            window.location.replace("/entradas/" + data.id + "/");
                        }, 1000);
                    } else {
                        Swal.fire("Error", data.mensaje, "warning");
                    }
                }
            });
        }
    )
}

function eliminarEvento() {
    Swal.fire({
        title: "Eliminar Evento",
        text: "¿Seguro de eliminar el Evento?",
        type: "question",
        showConfirmButton: true,
        showCancelButton: true,
        confirmButtonColor: '#a0db81',
        cancelButtonColor: '#f03a47',
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.value){
            swalExito();
        }
    });
}

function registrarEvento() {
    $('#modal-regE').addClass('is-active');
}

function modificarEvento() {
    $('#modal-modE').addClass('is-active');
}

function mostrarLogin(){
    if (poplogin) {
        $('#poplogin').css('visibility', 'hidden');
        $('#poplogin').css('opacity', '0');
        poplogin = false;
    } else {
        $('#poplogin').css('visibility', 'visible');
        $('#poplogin').css('opacity', '1');
        poplogin = true;
    }
}

function mostrarSignUp() {
    if (popsignUp) {
        $('#popsignUp').css('visibility', 'hidden');
        $('#popsignUp').css('opacity', '0');
        popsignUp = false;
    } else {
        $('#popsignUp').css('visibility', 'visible');
        $('#popsignUp').css('opacity', '1');
        popsignUp = true;
    }
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

function aceptarModE() {
    Swal.fire({
        title: "Modificar Evento",
        text: "¿Seguro de relizar esta modificación?",
        type: "question",
        showConfirmButton: true,
        showCancelButton: true,
        confirmButtonColor: '#a0db81',
        cancelButtonColor: '#f03a47',
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.value) {
            $('#modal-modE').removeClass('is-active');
            swalExito();
        }
    });  
}

function login(){
    var username = $("#username").val()
    var password = $("#password").val()
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ajax/login/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': token,
            'username': username,
            'password': password,
        },
        dataType: 'json',
        success: function(data) {
            if (data.exito){
                Swal.fire("Bienvenido","Login exitoso. Bienvenido.","success",timer=1000);
                setTimeout(function(){
                    window.location.replace("/check/");
                }, 1000);
            } else {
                Swal.fire("Error", "Hubo un error con tus credenciales. Verifica e intenta de nuevo", "warning");
            }
        }
    });
}

function redirectSignUp() {
    var username = $("#usernameSU").val()
    var email = $("#emailSU").val()
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    if (email!='' && username!=''){
        $.ajax({
            url: '/ajax/redirectSU/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': token,
                'username': username,
                'email': email,
            },
            dataType: 'json',
            success: function (data) {
                if (data.exito) {
                    window.location.href = "/registrar/";
                } else {
                    Swal.fire("Error", data.mensaje, "warning");
                }
            }
        });
    } else {
        Swal.fire("Error","Debe llenar todos los datos","warning");
    }
}

function aceptarRegE() {
    if ($('#nombRE').val() == ''){
        Swal.fire('Error','Introduzca el nombre del evento', 'error');
        return;
    } else if ($('#fechRE').val() == ''){
        Swal.fire('Error','Introduzca la fecha del evento', 'error');
        return;
    } else if ($('#horRE').val() == ''){
        Swal.fire('Error','Introduzca la hora del evento', 'error');
        return;
    } else if ($('#lugRE').val() == ''){
        Swal.fire('Error','Introduzca el lugar del evento', 'error');
        return;
    } else if ($('#precRE').val() == ''){
        Swal.fire('Error','Introduzca el precio del evento', 'error');
        return;
    } else if ($('#afRE').val() == ''){
        Swal.fire('Error','Introduzca el aforo máximo del evento', 'error');
        return;
    } else if ($('#descRE').val() == ''){
        Swal.fire('Error','Introduzca la descripción del evento', 'error');
        return;
    } 
    Swal.fire({
        title: "Registrar Evento",
        text: "¿Seguro de relizar este registro?",
        type: "question",
        showConfirmButton: true,
        showCancelButton: true,
        confirmButtonColor: '#a0db81',
        cancelButtonColor: '#f03a47',
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.value) {
            $('#modal-regE').removeClass('is-active');
            var token = $('input[name="csrfmiddlewaretoken"]').val();
            $.ajax({
                url: '/ajax/crearevento/',
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': token,
                    'nombre':$('#nombRE').val(),
                    'fecha':$('#fechRE').val(),
                    'hora':$('#horRE').val(),
                    'lugar':$('#lugRE').val(),
                    'aforo':$('#afRE').val(),
                    'precio':$('#precRE').val(),
                    'descripcion':$('#descRE').val(),
                },
                dataType: 'json',
                success: function(data) {
                    if (data.exito == true) {
                        swalExito();                        
                    } else {
                        swalError();
                    }
                }
            });
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