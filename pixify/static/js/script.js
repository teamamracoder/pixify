'use strict'




document.addEventListener("DOMContentLoaded", function () {
    const navItems = document.querySelectorAll('.nav-item');
    const currentPath = window.location.pathname;

    navItems.forEach(function (item) {
        const link = item.querySelector('a');
        if (link && link.getAttribute('href') === currentPath) {
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



// Badhan
// Function to update time stamps

// function updateTimeStamps() {
//     document.getElementById('time1').innerText = '11h';
//     document.getElementById('time2').innerText = '1m';
//     document.getElementById('time3').innerText = '20m';
//     document.getElementById('time4').innerText = '5m';
//     document.getElementById('time5').innerText = '2h';
//     document.getElementById('time6').innerText = '9h';
// }

// updateTimeStamps();
// updateTimeStamps();
//End Badhan

// select post photo and videos--Priya
// let files = [],
//     button = document.querySelector(".top button"),
//     form = document.querySelector("#form"),
//     container = document.querySelector(".con"),
//     text = document.querySelector(".inner"),
//     browse = document.querySelector(".select"),
//     input = document.querySelector("#fileInput");


// browse.addEventListener('click', () => input.click());



// input.addEventListener('change', () => {
//     let file = input.files;
//     for (let i = 0; i < file.length; i++) {
//         if (files.every(e => e.name != file[i].name)) files.push(file[i])


//     }

//     form.reset();
//     showImages();

// })

// const showImages = () => {
//     let images = '';
//     files.forEach((e, i) => {
//         images += `<div class="images">
//         <img src="${URL.createObjectURL(e)}">
//         <span onclick="delImage(${i})">&times</span>
//      </div>`
//     })
//     container.innerHTML = images;
// }
// const delImage = index => {
//     files.splice(index, 1)
//     showImages()
// }


let files = [],
    container = document.querySelector(".con"),
    browse = document.querySelector(".select"),
    input = document.querySelector("#fileInput");
if (browse && input) {
    browse.addEventListener('click', () => input.click());

    input.addEventListener('change', () => {
        let file = input.files;
        for (let i = 0; i < file.length; i++) {
            if (files.every(e => e.name !== file[i].name)) files.push(file[i]);
        }

        //input.value = "";
        showImages();
    });
}


const showImages = () => {
    let images = '';
    files.forEach((e, i) => {
        images += `<div class="images">
            <img src="${URL.createObjectURL(e)}" alt="Uploaded Image Preview">
            <span onclick="delImage(${i})" style="cursor: pointer;">&times;</span>
        </div>`;
    });
    container.innerHTML = images;
};

const delImage = index => {
    files.splice(index, 1);
    showImages();
};


// select post photo and videos--Priya End
//For Comment

// comment reply section by priya mitra
document.querySelectorAll(".view-comment").forEach((viewComment) => {
    viewComment.addEventListener("click", () => {
        document.querySelectorAll(".reply-open").forEach(reply => {
            reply.style.display = "none";
        });
        document.querySelectorAll(".view-comment").forEach(comment => {
            comment.innerHTML = comment.innerHTML.replace("Hide reply", "View reply");
        });

        const replyOpen = viewComment.nextElementSibling;
        if (replyOpen.style.display === "none" || replyOpen.style.display === "") {
            replyOpen.style.display = "block";
            viewComment.innerHTML = viewComment.innerHTML.replace("View reply", "Hide reply");
        } else {
            replyOpen.style.display = "none";
            viewComment.innerHTML = viewComment.innerHTML.replace("Hide reply", "View reply");
        }
    });
});



//End Comment



//Share Modal--Rima
function toggleShareButton() {

    const checkboxes = document.querySelectorAll(".custom-checkbox input[type='checkbox']");
    const isAnyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);


    const shareButtonContainer = document.getElementById("shareButtonContainer");
    shareButtonContainer.style.display = isAnyChecked ? "flex" : "none";
}
//End Share Modal