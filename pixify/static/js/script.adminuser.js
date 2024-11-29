// $(document).ready(function () {
//     $('#sidebar-toggler').on('click', function () {
//         if ($('#sidebarMain').hasClass('d-lg-block')) {
//             $('#sidebarMain').removeClass('d-lg-block');
//             $('#main-container').removeClass('col-lg-10').addClass('col-lg-12');
//         } else {
//             $('#sidebarMain').addClass('d-lg-block');
//             $('#main-container').removeClass('col-lg-12').addClass('col-lg-10');
//         }
//     });
//     //navbar populate
//     $('#navLinks').html($('#sidebarLinks').html());
// });


const sidebar = document.getElementById("sidebar");
        
function updateSidebarWidth() {
    if (window.innerWidth > 992) {
        sidebar.classList.add("w-25");  
        sidebar.classList.remove("w-50");  
    } else {
        sidebar.classList.add("w-50");  
        sidebar.classList.remove("w-25");  
    }
}


window.addEventListener("resize", updateSidebarWidth);


updateSidebarWidth();