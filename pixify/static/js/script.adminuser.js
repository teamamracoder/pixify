document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById('menu-toggle');
    const sidebarMain = document.getElementById('sidebarMain');
    const mainContainer = document.querySelector('.col-10');

    menuToggle.addEventListener('click', function () {
        sidebarMain.classList.toggle('d-none'); // Show/hide sidebar
        sidebarMain.classList.toggle('d-lg-block'); // Ensure desktop behavior is not affected
        mainContainer.classList.toggle('col-12');
        mainContainer.classList.toggle('col-10');
    });
});
