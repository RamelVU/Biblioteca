function listadoLibros(){
    $.ajax({
        url: "/libro/listar_libro/",
        type: "get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#tabla_libros')){
                $('#tabla_libros').DataTable().destroy();
            }
            $('#tabla_libros tbody').html("");
            for(let i=0; i <response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['titulo'] + '</td>';
                if (response[i]["fields"]['autor_id'] == ''){
                    fila += '<td>Desconocido</td>';
                }else{
                    fila += '<td>' + response[i]["fields"]['autor_id'] + '</td>';       
                }  
                fila += '<td>' + response[i]["fields"]['fecha_publicacion'] + '</td>';
                fila += '<td><button class="btn btn-primary btn-sm tableButton" onclick="abrir_modal_edicion(\'/libro/editar_libro/'+response[i]['pk']+'/\');">Editar</button>'; 
                fila += '<button class="btn btn-danger btn-sm tableButton" onclick="abrir_modal_eliminacion(\'/libro/eliminar_libro/'+response[i]['pk']+'/\');">Eliminar</button></td>'; 
                fila += '</tr>';
                $('#tabla_libros tbody').append(fila);
            }
            $('#tabla_libros').DataTable({
                language: {
                    decimal: "",
                    emptyTable: "No hay información",
                    info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                    infoEmpty: "Mostrando 0 de 0 de 0 Entradas",
                    infoFiltered: "(Filtrado de _MAX_ total entradas)",
                    infoPostFix: "",
                    thousands: ",",
                    lengthMenu: "Mostrar _MENU_ Entradas",
                    loadingRecords: "Cargando...",
                    processing: "Procesando...",
                    search: "Buscar:",
                    zeroRecords: "Sin resultados encontrados",
                    paginate: {
                        first: "Primero",
                        last: "Ultimo",
                        next: "Siguiente",
                        previous: "Anterior",
                    },
                },
            });
        },
        error: function(error){
            console.log(error);
        }
    });
}

function registrar(){
    activarBoton();
    var data = new FormData($('#form_creacion').get(0));
	$.ajax({
		data: data,
		url: $('#form_creacion').attr('action'),
        type: $('#form_creacion').attr('method'),
        cache: false,
        contentType: false,
        processData: false,
		success: function(response){
            notificacionSuccess(response.mensaje)
			listadoLibros();
			cerrar_modal_creacion();
		},
		error: function(error){
            notificacionError(error.responseJSON.mensaje)
            mostrarErroresCreacion(error)
            activarBoton();
            
		}
	});
}

function editar(){
    activarBoton();
    var data = new FormData($('#form_edicion').get(0));
    $.ajax({
		data: data,
		url: $('#form_edicion').attr('action'),
        type: $('#form_edicion').attr('method'),
        cache: false,
        contentType: false,
        processData: false,
		success: function(response){
            notificacionSuccess(response.mensaje)
			listadoLibros();
			cerrar_modal_edicion();
		},
		error: function(error){
            notificacionError(error.responseJSON.mensaje)
            mostrarErroresEdicion(error)
            activarBoton();
            
		}
	});
}

function eliminar(pk){
    $.ajax({
        data: {
            csrfmiddlewaretoken:$("[name='csrfmiddlewaretoken']").val()
        },
		url: '/libro/eliminar_libro/' + pk + '/',
		type: 'post',
		success: function(response){
            notificacionSuccess(response.mensaje)
			listadoLibros();
			cerrar_modal_eliminacion();
		},
		error: function(error){
            notificacionError(error.responseJSON.mensaje)
            
		}
	});
}

$(document).ready(function(){
    listadoLibros();
});
