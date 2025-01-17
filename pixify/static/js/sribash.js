
const storiesw = document.querySelectorAll(".stories .story img"); // Select all story images
const storyView = document.getElementById("story-view"); // Full view container
const storyImgw = document.getElementById("story-img"); // Full view image element
const prevStoryBtnnn = document.getElementById("prev-story"); // Previous button
const nextStoryBtnnm = document.getElementById("next-story"); // Next button
const closeStoryBtn = document.getElementById("close-story"); // Close button

let currentIndexww = 0; // To track the currently displayed story

// Function to show the full view with a specific story
function showStory(index) {
  currentIndexww = index;
  const selectedStory = storiesw[currentIndexww];
  storyImgw.src = selectedStory.src; // Update the full view image
  storyView.style.display = "flex"; // Show the full view container
}

// Event listener for each story image
storiesw.forEach((story, index) => {
  story.addEventListener("click", () => {
    showStory(index);
  });
});

// Navigate to the next story
function nextStory() {
  if (currentIndexww < storiesw.length - 1) {
    currentIndexww++;
    showStory(currentIndexww);
  } else {
    // If no more stories, close the full view
    storyView.style.display = "none";
  }
}

// Navigate to the previous story
function prevStory() {
  if (currentIndexww > 0) {
    currentIndexww--;
    showStory(currentIndexww);
  }
}

// Add event listeners for navigation buttons
nextStoryBtnnm.addEventListener("click", nextStory);
prevStoryBtnnn.addEventListener("click", prevStory);

// Close the full view
closeStoryBtn.addEventListener("click", () => {
  storyView.style.display = "none"; // Hide the full view container
});

// Handle click on full view container to navigate to next story
storyView.addEventListener("click", (event) => {
  if (!event.target.closest(".previous-btn") && !event.target.closest(".next-btn") && !event.target.closest(".close-btn")) {
    nextStory();
  }
});





// const allStories = [
//     {
//         id: 0,
//         author: "sribash sarkar",
//         dp: "static/images/p3.jpg",
//         imageUrl: "static/images/priya.jpg",
//     },
//     {
//         id: 1,
//         author: "PRIYA MITRA",
//         dp: "static/images/priya.jpg",
//         imageUrl: "static/images/priya.jpg",
//     },
//     {
//         id: 2,
//         dp: "static/images/p3.jpg",
//         author: "Rima das",
//         imageUrl: "static/images/p3.jpg",
//     },
//     {
//         id: 3,
//         dp: "static/images/p1.jpg",
//         author: "sribash sarkar",
//         imageUrl: "static/images/p1.jpg",
//     },
//     {
//         id: 4,
//         dp: "static/images/p2.jpg",
//         author: "sribash sarkar",
//         imageUrl: "static/images/p2.jpg",
//     },
//     {
//         id: 5,
//         dp: "static/images/p3.jpg",
//         author: "sribash sarkar",
//         imageUrl: "static/images/p3.jpg",
//     },
//     {
//         id: 6,
//         dp: "static/images/p4.jpg",
//         author: "sribash sarkar",
//         imageUrl: "static/images/p4.jpg",
//     },
// ];
// const storyImgsort = document.querySelector(".story #dp img");
// const stories = document.querySelector(".stories");
// const storiesFullView = document.querySelector(".stories-full-view");
// const closeBtn = document.querySelector(".close-btn");
// const storyImgFull = document.querySelector(".stories-full-view .story img");
// const profileImgFull = document.querySelector(".stories-full-view #dp img");
// const storyAuthorFull = document.querySelector(".stories-full-view .story .author");
// const nextBtn = document.querySelector(".stories-container .next-btn");
// const storiesContent = document.querySelector(".stories-container .content");
// const previousBtn = document.querySelector(".stories-container .previous-btn");
// const nextBtnFull = document.querySelector(".stories-full-view .next-btn");
// const previousBtnFull = document.querySelector(".stories-full-view .previous-btn");
// let currentActive = 0;

// const createStories = () => {
//     allStories.forEach((s, i) => {

//         const story = document.createElement("div");
//         story.classList.add("story");



//         const img = document.createElement("img");
//         img.src = s.imageUrl;


//         const author = document.createElement("div");
//         author.classList.add("author");
//         author.innerHTML = s.author;

//         const dp = document.createElement("div");
//         dp.classList.add("dp");
//         const dpimg = document.createElement("img");
//         dpimg.src = s.dp;

//         story.appendChild(img);
//         story.appendChild(dp);
//         dp.appendChild(dpimg);
//         story.appendChild(author);
//         stories.appendChild(story);
//         // stories.appendChild(dp);

//         story.addEventListener("click", () => {
//             showFullView(i);
//         })
//     });
// };

// createStories();
// //  createStories2();
// const showFullView = (index) => {
//     currentActive = index;
//     updateFullview();
//     storiesFullView.classList.add("actived");
//     // console.log("hello w")
// };
// closeBtn.addEventListener("click", () => {
//     storiesFullView.classList.remove("actived");
// });

// const updateFullview = () => {
//     storyImgFull.src = allStories[currentActive].imageUrl;
//     profileImgFull.src = allStories[currentActive].dp;
//     storyAuthorFull.innerHTML = allStories[currentActive].author;
//     // profileImgFull.src = allStories[currentActive].imageUrl;

// }

// nextBtn.addEventListener("click", () => {
//     storiesContent.scrollLeft += 300;
// });
// previousBtn.addEventListener("click", () => {
//     storiesContent.scrollLeft -= 300;
// });

// storiesContent.addEventListener("scroll", () => {
//     if (storiesContent.scrollLeft <= 24) {
//         previousBtn.classList.remove("actived");
//     } else {
//         previousBtn.classList.add("actived");
//     }

//     let maxScrollValue = storiesContent.scrollWidth - storiesContent.clientWidth - 24;

//     if (storiesContent.scrollLeft >= maxScrollValue) {
//         nextBtn.classList.remove("actived");
//     } else {
//         nextBtn.classList.add("actived");
//     }

// });

// nextBtnFull.addEventListener("click", () => {
//     if (currentActive >= allStories.length - 1) {
//         return;
//     }
//     currentActive++;
//     updateFullview();
// })
// previousBtnFull.addEventListener("click", () => {
//     if (currentActive <= 0) {
//         return;
//     }
//     currentActive--;
//     updateFullview();
// }) 