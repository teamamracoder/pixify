
const allStories = [
    {
        id: 0,
        author: "sribash sarkar",
        dp: "static/images/p3.jpg",
        imageUrl: "static/images/priya.jpg",
    },
    {
        id: 1,
        author: "PRIYA MITRA",
        dp: "static/images/priya.jpg",
        imageUrl: "static/images/priya.jpg",
    },
    {
        id: 2,
        dp: "static/images/p3.jpg",
        author: "Rima das",
        imageUrl: "static/images/p3.jpg",
    },
    {
        id: 3,
        dp: "static/images/p1.jpg",
        author: "sribash sarkar",
        imageUrl: "static/images/p1.jpg",
    },
    {
        id: 4,
        dp: "static/images/p2.jpg",
        author: "sribash sarkar",
        imageUrl: "static/images/p2.jpg",
    },
    {
        id: 5,
        dp: "static/images/p3.jpg",
        author: "sribash sarkar",
        imageUrl: "static/images/p3.jpg",
    },
    {
        id: 6,
        dp: "static/images/p4.jpg",
        author: "sribash sarkar",
        imageUrl: "static/images/p4.jpg",
    },
];
const storyImgsort = document.querySelector(".story #dp img");
const stories = document.querySelector(".stories");
const storiesFullView = document.querySelector(".stories-full-view");
const closeBtn = document.querySelector(".close-btn");
const storyImgFull = document.querySelector(".stories-full-view .story img");
const profileImgFull = document.querySelector(".stories-full-view #dp img");
const storyAuthorFull = document.querySelector(".stories-full-view .story .author");
const nextBtn = document.querySelector(".stories-container .next-btn");
const storiesContent = document.querySelector(".stories-container .content");
const previousBtn = document.querySelector(".stories-container .previous-btn");
const nextBtnFull = document.querySelector(".stories-full-view .next-btn");
const previousBtnFull = document.querySelector(".stories-full-view .previous-btn");
let currentActive = 0;

const createStories = () => {
    allStories.forEach((s, i) => {

        const story = document.createElement("div");
        story.classList.add("story");



        const img = document.createElement("img");
        img.src = s.imageUrl;


        const author = document.createElement("div");
        author.classList.add("author");
        author.innerHTML = s.author;

        const dp = document.createElement("div");
        dp.classList.add("dp");
        const dpimg = document.createElement("img");
        dpimg.src = s.dp;

        story.appendChild(img);
        story.appendChild(dp);
        dp.appendChild(dpimg);
        story.appendChild(author);
        stories.appendChild(story);
        // stories.appendChild(dp);

        story.addEventListener("click", () => {
            showFullView(i);
        })
    });
};

// const createStories2 = () => {
//     dpimg.forEach((s,j)=>{
//         const profile = document.createElement("div");
//         profile.classList.add("story");
//         const img = document.createElement("img");
//         img.src = s.imageUrl;

//         profile.appendChild(img);
//         stories.appendChild(profile);
//         story.addEventListener("click",() =>{
//             showFullView(j);
//         })
//     })

// }

createStories();
//  createStories2();
const showFullView = (index) => {
    currentActive = index;
    updateFullview();
    storiesFullView.classList.add("actived");
    // console.log("hello w")
};
closeBtn.addEventListener("click", () => {
    storiesFullView.classList.remove("actived");
});

const updateFullview = () => {
    storyImgFull.src = allStories[currentActive].imageUrl;
    profileImgFull.src = allStories[currentActive].dp;
    storyAuthorFull.innerHTML = allStories[currentActive].author;
    // profileImgFull.src = allStories[currentActive].imageUrl;

}

nextBtn.addEventListener("click", () => {
    storiesContent.scrollLeft += 300;
});
previousBtn.addEventListener("click", () => {
    storiesContent.scrollLeft -= 300;
});

storiesContent.addEventListener("scroll", () => {
    if (storiesContent.scrollLeft <= 24) {
        previousBtn.classList.remove("actived");
    } else {
        previousBtn.classList.add("actived");
    }

    let maxScrollValue = storiesContent.scrollWidth - storiesContent.clientWidth - 24;

    if (storiesContent.scrollLeft >= maxScrollValue) {
        nextBtn.classList.remove("actived");
    } else {
        nextBtn.classList.add("actived");
    }

});

nextBtnFull.addEventListener("click", () => {
    if (currentActive >= allStories.length - 1) {
        return;
    }
    currentActive++;
    updateFullview();
})
previousBtnFull.addEventListener("click", () => {
    if (currentActive <= 0) {
        return;
    }
    currentActive--;
    updateFullview();
})


// stoty upload


// Get elements
const storyUploaded = document.querySelector(".story-uploaded");
const storyUpload = document.querySelector(".story-upload");
const previewSection = document.getElementById("previewSection");
const preview = document.getElementById("preview");
const fileInput = document.getElementById("fileInput");

// Event listener for 'story-uploaded' click
storyUploaded.addEventListener("click", () => {
fileInput.click(); // Open file input dialog
});

// Handle file selection
fileInput.addEventListener("change", (event) => {
const file = event.target.files[0];

if (file) {
    const fileURL = URL.createObjectURL(file); // Create URL for the selected file

    // Show preview
    preview.innerHTML = file.type.startsWith("image")
        ? `<img src="${fileURL}" style="max-width: 100%; max-height: 60vh; border-radius: 16px;">`
        : `<video src="${fileURL}" controls style="max-width: 100%; max-height: 60vh; border-radius: 16px;"></video>`;

    // Hide the upload sections
    storyUpload.style.display = "none";
    storyUploaded.style.display = "none";
    // Show the preview section
    previewSection.style.display = "block";
}
});





// Buttons functionality (you can expand these as needed)
document.getElementById("editBtn").addEventListener("click", () => {
alert("Edit functionality coming soon!");
});



document.getElementById("addTextBtn").addEventListener("click", () => {
alert("Add to Text functionality coming soon!");
});



// Get elements
const storyUploadedd = document.querySelector(".story-uploaded");
const storyUploadd = document.querySelector(".story-upload");
const previewSections = document.getElementById("previewSection");
const textInput = document.createElement("textarea"); // Create a textarea element for editing
const actionButtons = document.createElement("div"); // Container for action buttons

// Create buttons dynamically
actionButtons.innerHTML = `
<button id="editBtn" class="btn btn-secondary">Edit</button>
<button id="deleteBtn" class="btn btn-danger">Delete</button>
<button id="uploadBtn" class="btn btn-primary">Upload</button>
`;
actionButtons.style.marginTop = "10px";

// Hide story-upload and show the input area on click
storyUploadd.addEventListener("click", () => {
// Hide the upload sections
storyUploadd.style.display = "none";
storyUploadedd.style.display = "none";

// Configure the textarea
textInput.className = "form-control";
textInput.rows = 16;
textInput.placeholder = "Type your story here...";

// Add the textarea and buttons to the preview section
previewSections.innerHTML = ""; // Clear existing content
previewSections.appendChild(textInput);
previewSections.appendChild(actionButtons);
previewSections.style.display = "block";
});

// Handle edit button click
document.addEventListener("click", (event) => {
if (event.target.id === "editBtn") {
alert("You can edit the text now!");
textInput.focus();
}
});

// Handle delete button click
document.addEventListener("click", (event) => {
if (event.target.id === "deleteBtn") {
if (confirm("Are you sure you want to delete this story?")) {
    textInput.value = ""; // Clear the text area
}
}
});

// Handle upload button click
document.addEventListener("click", (event) => {
if (event.target.id === "uploadBtn") {
if (textInput.value.trim() === "") {
    alert("Cannot upload an empty story!");
} else {
    alert("Story uploaded successfully!");
    // You can add your upload functionality here
}
}
});


// Select the close button and the full view upload container
const closeBtnn = document.querySelector(".close-btn-u");
const storiesFullViewUpload = document.querySelector(".stories-full-view-uploadd");

// Add click event listener to the close button
closeBtnn.addEventListener("click", () => {
storiesFullViewUpload.style.display = "none"; // Hide the full view upload container
});


// Select the image elements and the full view upload container
const storyImages = document.querySelectorAll(".card-img-top");
const storiesFullViewUploadd = document.querySelector(".stories-full-view-uploadd");

// Add click event listeners to all images with the 'card-img-top' class
// storyImages.forEach((image) => {
// image.addEventListener("click", () => {
// console.log("cli")

// storiesFullViewUploadd.style.display = "block";
// });
// });



//

const storiess = [
    {

    }
];  // Array to store story image URLs           1
let currentStoryIndex = 0;

const storyImg = document.getElementById("storyImg");
const timelinea = document.querySelector(".timelinea");
const fileInputInput = document.querySelector(".fileInpu");
const uploadButton = document.getElementById("uploadBtn");

let selectedImageUrl = "";  // Variable to hold selected image URL

// Handle file selection
fileInputInput.addEventListener("change", (event) => {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            selectedImageUrl = e.target.result;  // Store the selected image URL
        };

        reader.readAsDataURL(file);  // Read the file and generate a URL
    }
});

// Handle Upload button click
uploadButton.addEventListener("click", () => {
    if (selectedImageUrl) {
        storiess.push(selectedImageUrl);  // Add the selected image to the stories array

        // Create a new timeline item dynamically
        const newTimelineaItem = document.createElement("div");
        newTimelineaItem.className = "timelinea-item";
        timelinea.appendChild(newTimelineaItem);

        // Update the current story index to the newly added image
        currentStoryIndex = storiess.length - 1;
        loadStory(currentStoryIndex);
    } else {
        alert("Please wait.");
    }
});

// Load the current story
function loadStory(index) {
    if (index < 0 || index >= storiess.length) return;
    storyImg.src = storiess[index];
    updateTimelinea(index);
}

// Update the timeline progress
function updateTimelinea(index) {
    const timelineaItems = document.querySelectorAll(".timelinea-item");
    timelineaItems.forEach((item, i) => {
        item.style.background = i <= index ? "#fff" : "rgba(255, 255, 255, 0.3)";
    });
}


//

// start to multiple story store
   // Array to hold the story images
   const storyImagess = [
    'static/images/priya.jpg'
]; // Add as many images as needed

let currentIndex = 0;
const storyImgElement = document.getElementById("story-img");
const timeLineElement = document.querySelector(".time-line");

// Function to initialize the timeline segments
function createTimelineSegments() {
    timeLineElement.innerHTML = ''; // Clear existing segments
    storyImagess.forEach(() => {
        const segment = document.createElement("div");
        segment.className = "time-line-segment";
        timeLineElement.appendChild(segment);
    });
}

// Function to load the current story
function loadStory(index) {
    if (index < 0 || index >= storyImagess.length) return;

    // Update the story image
    storyImgElement.src = storyImagess[index];

    // Update the timeline segments
    updateTimeline(index);
}

// Function to update the timeline progress
function updateTimeline(index) {
    const segments = document.querySelectorAll(".time-line-segment");
    segments.forEach((segment, i) => {
        if (i <= index) {
            segment.classList.add("active");
        } else {
            segment.classList.remove("active");
        }
    });
}

// Handle previous and next story navigation
document.getElementById("prev-story").addEventListener("click", () => {
    if (currentIndex > 0) {
        currentIndex--;
        loadStory(currentIndex);
    }
});

document.getElementById("next-story").addEventListener("click", () => {
    if (currentIndex < storyImagess.length - 1) {
        currentIndex++;
        loadStory(currentIndex);
    }
});

// Initialize the timeline and load the first story
createTimelineSegments();
loadStory(currentIndex);
let autoPlayInterval = setInterval(() => {
    if (currentIndex < storyImagess.length - 1) {
        currentIndex++;
        loadStory(currentIndex);
    } else {
        clearInterval(autoPlayInterval); // Stop when the last story is reached
    }
}, 5000); // Change image every 5 seconds
