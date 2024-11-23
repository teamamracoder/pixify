$(document).ready(function () {
    $('#sidebar-toggler').on('click', function () {
        if ($('#sidebarMain').hasClass('d-lg-block')) {
            $('#sidebarMain').removeClass('d-lg-block');
            $('#main-container').removeClass('col-lg-10').addClass('col-lg-12');
        } else {
            $('#sidebarMain').addClass('d-lg-block');
            $('#main-container').removeClass('col-lg-12').addClass('col-lg-10');
        }
    });
    //navbar populate
    $('#navLinks').html($('#sidebarLinks').html());
});