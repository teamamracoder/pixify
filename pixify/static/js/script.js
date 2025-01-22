"use strict";

console.log(
  "%cWelcome to Pixify",
  "color:white;background-color:white;font-weight:bold;font-size:25px;font-family:monospace;text-shadow:0px 0px 9px black;text-align:center;padding:8px 10px;border-radius:4px;"
);



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

    const userImages = document.querySelectorAll(".userImage");
    const userDropdowns = document.querySelectorAll(".userDropdown");

    if (userImages.length > 0 && userDropdowns.length > 0) {
        userImages.forEach((userImage, index) => {
            const userDropdown = userDropdowns[index];

            if (userDropdown) {
                userImage.addEventListener("click", function (event) {
                    console.log("Working");
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
//     container = document.querySelector(".con"),
//     browse = document.querySelector(".select"),
//     input = document.querySelector("#fileInput");
// if (browse && input) {
//     browse.addEventListener('click', () => input.click());

//     input.addEventListener('change', () => {
//         let file = input.files;
//         for (let i = 0; i < file.length; i++) {
//             if (files.every(e => e.name !== file[i].name)) files.push(file[i]);
//         }

//         //input.value = "";
//         showImages();
//     });
// }
// const showImages = () => {
//     let images = '';
//     files.forEach((e, i) => {
//         images += `<div class="images">
//             <img src="${URL.createObjectURL(e)}" alt="Uploaded Image Preview">
//             <span onclick="delImage(${i})" style="cursor: pointer;">&times;</span>
//         </div>`;
//     });
//     container.innerHTML = images;
// };
// const delImage = index => {
//     files.splice(index, 1);
//     showImages();
// };


// select post photo and videos--Priya

document.addEventListener("DOMContentLoaded", () => {
    let files = [];
    let container = document.querySelector(".con");
    //let browse = document.querySelector(".select");
    let input = document.querySelector("#fileInput");

    if (input) {
        input.addEventListener('change', () => {
            let file = input.files;
            for (let i = 0; i < file.length; i++) {
                if (files.every(e => e.name !== file[i].name)) files.push(file[i]);
            }

            showImages();
        });
    }

    const showImages = () => {
        let images = '';
        files.forEach((e, i) => {
            images += `<div class="images">
                <img src="${URL.createObjectURL(e)}" alt="Uploaded Image Preview">
                <span onclick="window.delImage(${i})" style="cursor: pointer;">&times;</span>
            </div>`;
        });
        container.innerHTML = images;
    };

    window.delImage = index => {
        files.splice(index, 1);
        showImages();
    };
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");

    //let files = [];

    // Highlight drop zone when dragging files over
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "blue"; // Highlight border color
        dropZone.style.backgroundColor = "#f0f8ff";
    });

    // Remove highlight when dragging out
    dropZone.addEventListener("dragleave", () => {
        dropZone.style.borderColor = "#ccc"; // Reset border color
        dropZone.style.backgroundColor = "transparent";
    });

    // Handle file drop
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.style.borderColor = "#ccc"; // Reset border color
        dropZone.style.backgroundColor = "transparent";

        const droppedFiles = Array.from(e.dataTransfer.files);
        handleFiles(droppedFiles);
    });

    // Handle file processing
    const handleFiles = (selectedFiles) => {
        selectedFiles.forEach((file) => {
            if (files.every((e) => e.name !== file.name)) {
                files.push(file);
            }
        });
        showImages();
    };


});



// select post photo and videos--Priya End









//For Comment
// comment reply section by priya mitra




document.addEventListener("DOMContentLoaded", () => {
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

});




const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))


//End Comment



//Share Modal--Rima
function toggleShareButton() {

    const checkboxes = document.querySelectorAll(".custom-checkbox input[type='checkbox']");
    const isAnyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);


    const shareButtonContainer = document.getElementById("shareButtonContainer");
    shareButtonContainer.style.display = isAnyChecked ? "flex" : "none";
}
//End Share Modal

//For Tooltip--Priya
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
});
//For Tooltip--Priya End



//create post for priya
