$(document).ready(function () {
    $(':checkbox').radiocheck();
    $(':radio').radiocheck();
    $("select").select2({dropdownCssClass: 'dropdown-inverse'});
    $('#bootstrap-switch-square').bootstrapSwitch();

})