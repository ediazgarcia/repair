$(document).ready(function() {
    // SideNav Button Initialization
  
    $(".button-collapse").sideNav2();
    // SideNav Scrollbar Initialization
  
    var sideNavScrollbar = document.querySelector('.custom-scrollbar');
    var ps = new PerfectScrollbar(sideNavScrollbar);
});

$(document).ready(function () {
    $('table').DataTable({
        language: {
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
        }
    });
});

// Material Select Initialization
$(document).ready(function() {
    $('.mdb-select').materialSelect();
    $('.select-wrapper.md-form.md-outline input.select-dropdown').bind('focus blur', function () {
      $(this).closest('.select-outline').find('label').toggleClass('active');
      $(this).closest('.select-outline').find('.caret').toggleClass('active');
    });
  });

  $(document).ready(function() {

    $('#lang').materialSelect({
    labels: {
      selectAll: 'Seleccionar Todo',
      optionsSelected: 'opciones seleccionadas',
    }
  });
});