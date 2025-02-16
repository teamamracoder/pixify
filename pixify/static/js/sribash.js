
let storiesByUser = {}; // Store all user stories
let currentUserIndex = 0; // Track the current user's index
let currentStoryIndex = 0; // Track the current story index
let userIds = []; // Store user IDs
let storyTimer; // Timer for auto-changing stories

// Fetch and store stories when a story is clicked
function openStoryView(userId) {
fetch(`/stories/view/${userId}`)
    .then(response => response.json())
    .then(data => {
        console.log(data.userDetails.profile_photo_url)
        storiesByUser = data.stories;
        userIds = Object.keys(storiesByUser); // Get list of user IDs
        currentUserIndex = userIds.indexOf(userId.toString()); // Set current user index
        currentStoryIndex = 0; // Reset story index


            // userNameContainer.innerHTML = "sham sing"

            // ✅ Update user profile image (if available)
            let profileImg = document.querySelector(".profile-img img");
            let username=document.querySelector("#usernamecr");
            if (username && data.userDetails.first_name) {
              username.textContent = data.userDetails.first_name;
            }
            //profileImg.src = data.userDetails.profile_photo_url ? data.userDetails.profile_photo_url : "/static/images/avatar.jpg";
           profileImg.src = data.userDetails.profile_photo_url ? `/static${data.userDetails.profile_photo_url}` : "/static/images/avatar.jpg";



        document.getElementById("story-view").style.display = "flex";
        loadStory(currentUserIndex, currentStoryIndex);
    })
    .catch(error => console.error("Error loading stories:", error));
}

//
function loadStory(userIndex, storyIndex) {
    let userId = userIds[userIndex]; // Get user ID
    let userStories = storiesByUser[userId]; // Get stories of the selected user

    if (storyIndex < 0 || storyIndex >= userStories.length) {
        return;
    }
    currentUserIndex = userIndex;
    currentStoryIndex = storyIndex;

    let story = userStories[storyIndex];
    console.log(story)
    let storyContent = document.getElementById("storyContent");
   // let userNameContainer = document.querySelector(".username");// Select the username element
    let profileImg = document.querySelector(".profile-img img"); // Select the profile image element
    storyContent.innerHTML = "";

    // Set user's name dynamically

console.log('story.media_type',story.media_type);
    // Check for media type and render appropriately
    if (story.media_type === 3 && story.media_url) {
        let video = document.createElement("video");
        video.src = story.media_url.startsWith("/") ? `static${story.media_url}` : story.media_url;
        video.controls = true;
        video.autoplay = true;
        video.style.width = "100%";
        video.style.height = "100%";
        video.style.objectFit = "cover";
        storyContent.appendChild(video);
    } else if (story.media_type == 2 && story.media_url) {
        let img = document.createElement("img");
        img.src = story.media_url.startsWith("/") ? `static${story.media_url}` : story.media_url;
        img.style.width = "100%";
        img.style.height = "100%";
        img.style.objectFit = "cover";
        storyContent.appendChild(img);
    } else if (story.description) {
        let textContainer = document.createElement("div");
        textContainer.classList.add("story-text");
        textContainer.textContent = story.description;
        textContainer.style.fontSize = "20px";
        textContainer.style.color = "black";
        textContainer.style.textAlign = "center";
        textContainer.style.marginTop = "75%";
        textContainer.style.padding = "20px";
        storyContent.appendChild(textContainer);
    } else {
        // If no media or text is available
        let noContent = document.createElement("p");
        noContent.textContent = "No media or text available.";
        noContent.style.color = "#fff";
        storyContent.appendChild(noContent);
    }


    // let userNameContainer = document.getElementById("usernamecr");
    //        if (userNameContainer) {
    //            userNameContainer.textContent = story.first_name ,story.last_name ? story.first_name:"hejibi " ;
    //             console.log("dshgs",data.first_name)   // Set the fetched first_name
    //         }


    updateTimeline(userStories.length, storyIndex);
    startAutoChange(); // Start auto transition
}

// Update timeline progress
function updateTimeline(totalStories, currentStoryIndex) {
let timeline = document.querySelector(".timelinea");
timeline.innerHTML = "";
for (let i = 0; i < totalStories; i++) {
    let timelineItem = document.createElement("div");
    timelineItem.className = "timelinea-item";
    timelineItem.style.background = i <= currentStoryIndex ? "#fff" : "rgba(255, 255, 255, 0.3)";
    timeline.appendChild(timelineItem);
}
}

// Auto-change stories every 25 seconds
function startAutoChange() {
clearTimeout(storyTimer); // Reset timer
storyTimer = setTimeout(() => {
    let userId = userIds[currentUserIndex];
    let userStories = storiesByUser[userId];

    if (currentStoryIndex < userStories.length - 1) {
        currentStoryIndex++;
    } else if (currentUserIndex < userIds.length - 1) {
        currentUserIndex++;
        currentStoryIndex = 0;
    } else {
        document.getElementById("story-view").style.display = "none"; // Close if last story
        return;
    }
    loadStory(currentUserIndex, currentStoryIndex);
}, 25000); // 25 seconds auto switch
}

// Move to the next story manually
document.getElementById("nextIcon").addEventListener("click", () => {
clearTimeout(storyTimer); // Reset auto-change timer
let userId = userIds[currentUserIndex];
let userStories = storiesByUser[userId];

if (currentStoryIndex < userStories.length - 1) {
    currentStoryIndex++;
} else if (currentUserIndex < userIds.length - 1) {
    currentUserIndex++;
    currentStoryIndex = 0;
}
loadStory(currentUserIndex, currentStoryIndex);
});

// Move to the previous story manually
document.getElementById("prevIcon").addEventListener("click", () => {
clearTimeout(storyTimer); // Reset auto-change timer
if (currentStoryIndex > 0) {
    currentStoryIndex--;
} else if (currentUserIndex > 0) {
    currentUserIndex--;
    let previousUserId = userIds[currentUserIndex];
    currentStoryIndex = storiesByUser[previousUserId].length - 1;
}
loadStory(currentUserIndex, currentStoryIndex);
});

// Close Story View
document.getElementById("closeIcon").addEventListener("click", () => {
clearTimeout(storyTimer); // Stop auto change when closing
document.getElementById("story-view").style.display = "none";
});

// Close story view when clicking outside the content
document.getElementById("story-view").addEventListener("click", (event) => {
    let storyContainer = document.getElementById("storySection"); // The main content

    if (!storyContainer.contains(event.target)) {
        document.getElementById("story-view").style.display = "none";
        clearTimeout(storyTimer); // Stop auto-change
    }
});