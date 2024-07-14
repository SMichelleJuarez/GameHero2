document.addEventListener('DOMContentLoaded', function() {
    // Obtener el campo de fecha de registro
    var fechaRegistroInput = document.getElementById('fecha_registro');

    // Obtener la fecha actual
    var today = new Date();
    var day = String(today.getDate()).padStart(2, '0');
    var month = String(today.getMonth() + 1).padStart(2, '0'); 
    var year = today.getFullYear();

    // Formatear la fecha en YYYY-MM-DD
    var todayFormatted = year + '-' + month + '-' + day;

    // Establecer el valor y el máximo de fecha como la fecha actual
    fechaRegistroInput.value = todayFormatted;
    fechaRegistroInput.max = todayFormatted;
});
