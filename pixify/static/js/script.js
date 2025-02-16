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


document.addEventListener("DOMContentLoaded", () => {
    let files = [];
    let container = document.querySelector(".con");
    let input = document.querySelector("#fileInput");
    let postForm = document.querySelector("#postForm");

    if (input) {
        input.addEventListener('change', (event) => {
            let fileList = Array.from(event.target.files);
            fileList.forEach(file => {
                if (!files.some(e => e.name === file.name)) {
                    files.push(file);
                }
            });
            showMedia();
            input.value = ''; // Reset input field to allow re-selection of the same files
        });
    }

    const showMedia = () => {
        let mediaContent = '';
        files.forEach((file, index) => {
            let mediaElement = '';
            if (file.type.startsWith("image")) {
                mediaElement = `<img src="${URL.createObjectURL(file)}" alt="Image Preview" style="width: 100%; height: 100%; object-fit: cover;">`;
            } else if (file.type.startsWith("video")) {
                mediaElement = `<video src="${URL.createObjectURL(file)}" muted loop style="width: 100%; height: 100%; object-fit: cover;"></video>`;
            }

            mediaContent += `
                <div class="media" style="position: relative; display: inline-block; width: 95px; height: 95px; margin: 5px; overflow: hidden; border-radius: 5px;">
                    ${mediaElement}
                    <span onclick="delMedia(${index})" style="position: absolute; top: 5px; left: 80%; cursor: pointer; font-size: 18px; color: red; font-weight: bold;">&times;</span>
                </div>`;
        });
        container.innerHTML = mediaContent;
    };

    window.delMedia = (index) => {
        files.splice(index, 1);
        showMedia();
    };

    // Ensure all selected files are included in form submission
    postForm.addEventListener("submit", () => {
        let fileInputField = document.createElement("input");
        fileInputField.type = "file";
        fileInputField.name = "postFiles";
        fileInputField.multiple = true;
        fileInputField.style.display = "none";

        let dataTransfer = new DataTransfer();
        files.forEach(file => dataTransfer.items.add(file));
        fileInputField.files = dataTransfer.files;

        postForm.appendChild(fileInputField);
    });

    // Prevent clearing files when modal closes
    let modal = document.getElementById("addPhotosVideosModal");
    modal.addEventListener("hidden.bs.modal", () => {
        showMedia();
    });
});


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
