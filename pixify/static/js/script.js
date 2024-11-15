'use strict'




document.addEventListener("DOMContentLoaded", function () {
    const navItems = document.querySelectorAll('.nav-item');
    const currentPath = window.location.pathname;

    navItems.forEach(function (item) {
        const link = item.querySelector('a');
        console.log(link && link.getAttribute('href'), '+', currentPath);
        if (link && link.getAttribute('href') === currentPath) {
            console.log(currentPath, "yes");
            item.classList.add('active');
        }
    });


    const searchForm = document.getElementById("searchbarInput");

    if (searchForm) {
        searchForm.addEventListener("click", function () {
            event.stopPropagation();
            searchForm.style.width = "100%";
        });

        document.addEventListener("click", function (event) {
            if (!searchForm.contains(event.target)) {
                searchForm.style.width = "";
            }
        });
    }



    const searchbarBtn = document.getElementById("searchbarBtn");
    const navbarNavMiddle = document.getElementById("navbarNavMiddle");
    const searchbarInputMiddle = document.getElementById("searchbarInputMiddle");

    if (searchbarBtn && navbarNavMiddle && searchbarInputMiddle) {
        searchbarBtn.addEventListener("click", function () {
            event.stopPropagation();
            searchbarInputMiddle.style.display = "block";
            navbarNavMiddle.style.display = "none";
        });
    }
    document.addEventListener("click", function (event) {
        if (!searchbarInputMiddle.contains(event.target) && event.target !== searchbarBtn) {
            searchbarInputMiddle.style.display = "none";
            navbarNavMiddle.style.display = "flex";
        }
    });

    const userImage = document.getElementById("userImage");
    const userDropdown = document.getElementById("userDropdown");

    if (userImage && userDropdown) {
        userImage.addEventListener("click", function (event) {
            event.stopPropagation();
            if (userDropdown.style.display === "none" || userDropdown.style.display === "") {
                userDropdown.style.display = "block";
            } else {
                userDropdown.style.display = "none";
            }
        });

        document.addEventListener("click", function (event) {
            if (!userImage.contains(event.target) && !userDropdown.contains(event.target)) {
                userDropdown.style.display = "none";
            }
        });
    }
});


// 
// Function to update time stamps

function updateTimeStamps() {
    document.getElementById('time1').innerText = '11h';
    document.getElementById('time2').innerText = '1m';
    document.getElementById('time3').innerText = '20m';
    document.getElementById('time4').innerText = '5m';
    document.getElementById('time5').innerText = '2h';
    document.getElementById('time6').innerText = '9h';
}

// Call the function to update time stamps
updateTimeStamps();
updateTimeStamps();



// Work by Badhan

document.addEventListener("DOMContentLoaded", () => {
    const confirmButton = document.querySelector('.btn-primary');
    const deleteButton = document.querySelector('.btn-secondary');

    confirmButton.addEventListener('click', () => {
        alert('Friend request confirmed!');
    });

    deleteButton.addEventListener('click', () => {
        alert('Friend request deleted!');
    });
});
