'use strict'




document.addEventListener("DOMContentLoaded", function () {
    const navItems = document.querySelectorAll('.nav-item');
    const currentPath = window.location.pathname;

    navItems.forEach(function (item) {
        const link = item.querySelector('a');
        if (link && link.getAttribute('href') === currentPath) {
            // item.classList.add('active');
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



// select post photo and videos
let files = [],
    button = document.querySelector(".top button"),
    form = document.querySelector("#form"),
    container = document.querySelector(".con"),
    text = document.querySelector(".inner"),
    browse = document.querySelector(".select"),
    input = document.querySelector("#fileInput");


browse.addEventListener('click', () => input.click());



input.addEventListener('change', () => {
    let file = input.files;
    for (let i = 0; i < file.length; i++) {
        if (files.every(e => e.name != file[i].name)) files.push(file[i])


    }

    form.reset();
    showImages();

})

const showImages = () => {
    let images = '';
    files.forEach((e, i) => {
        images += `<div class="images">
        <img src="${URL.createObjectURL(e)}">
        <span onclick="delImage(${i})">&times</span>
     </div>`
    })
    container.innerHTML = images;
}
const delImage = index => {
    files.splice(index, 1)
    showImages()
}