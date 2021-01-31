function listadoLibrosReservados(){
    $.ajax({
        url: "/libro/reservas-vencidas/",
        type: "get",
        dataType: "json",
        success: function(response){
            if($.fn.DataTable.isDataTable('#tabla_reservas_vencidas')){
                $('#tabla_reservas_vencidas').DataTable().destroy();
            }
            $('#tabla_reservas_vencidas tbody').html("");
            for(let i=0; i <response.length; i++){
                let fila = '<tr>';
                fila += '<td>' + (i + 1) + '</td>';
                fila += '<td>' + response[i]["fields"]['libro'] + '</td>';
                fila += '<td>' + response[i]["fields"]['fecha_creacion'] + '</td>';
                fila += '</tr>';
                $('#tabla_reservas_vencidas tbody').append(fila);
            }
            $('#tabla_reservas_vencidas').DataTable({
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

$(document).ready(function(){
    listadoLibrosReservados();
});