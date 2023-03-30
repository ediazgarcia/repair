// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({language: {
    search: "Buscar registro",
    lengthMenu:"Mostrar _MENU_ registros",
    paginate: {
        "first":      "Primero",
        "last":       "Último",
        "next":       "Siguiente",
        "previous":   "Anterior"
    },
    emptyTable:     "No hay información en esta tabla",
    info:           "Mostrando de _START_ hasta _END_ de _TOTAL_ registros",
    infoEmpty:      "No hay registros",
    infoFiltered:   "(Filtrando de _MAX_ registros en total)",
    zeroRecords:    "No hay resultados en la búsqueda",
}});
});
