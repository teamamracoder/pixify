
const  allStories =[
    {
        id:0, 
        author:"sribash sarkar",
        dp:"static/images/p3.jpg",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:1,
        author:"PRIYA MITRA",
        dp:"static/images/priya.jpg",
        imageUrl:"static/images/priya.jpg",
    },
    {
        id:2,
        dp:"static/images/p3.jpg",
        author:"Rima das",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:3,
        dp:"static/images/p1.jpg",
        author:"sribash sarkar",
        imageUrl:"static/images/p1.jpg",
    },
    {
        id:4,
        dp:"static/images/p2.jpg",
        author:"sribash sarkar",
        imageUrl:"static/images/p2.jpg",
    },
    {
        id:5,
        dp:"static/images/p3.jpg",
        author:"sribash sarkar",
        imageUrl:"static/images/p3.jpg",
    },
    {
        id:6,
        dp:"static/images/p4.jpg",
        author:"sribash sarkar",
        imageUrl:"static/images/p4.jpg",
    },
]; 
const storyImgsort =document.querySelector(".story #dp img");
const stories =document.querySelector(".stories");
const storiesFullView =document.querySelector(".stories-full-view");
const closeBtn =document.querySelector(".close-btn");
const storyImgFull =document.querySelector(".stories-full-view .story img");
const profileImgFull =document.querySelector(".stories-full-view #dp img");
const storyAuthorFull =document.querySelector(".stories-full-view .story .author");
const nextBtn = document.querySelector(".stories-container .next-btn");
const storiesContent = document.querySelector(".stories-container .content");
const previousBtn = document.querySelector(".stories-container .previous-btn");
const nextBtnFull = document.querySelector(".stories-full-view .next-btn");
const previousBtnFull = document.querySelector(".stories-full-view .previous-btn");
let currentActive =0;

const createStories = () => {
    allStories.forEach((s ,i )=> {
    
        const story = document.createElement("div");
        story.classList.add("story");



        const img = document.createElement("img");
        img.src = s.imageUrl;


        const  author = document.createElement("div");
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

        story.addEventListener("click",() =>{
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
 const showFullView = (index) =>{
    currentActive = index;
    updateFullview();
    storiesFullView.classList.add("actived"); 
    // console.log("hello w")
 };
 closeBtn.addEventListener("click", () => {
    storiesFullView.classList.remove("actived");
 });

 const updateFullview = () =>{
    storyImgFull.src = allStories[currentActive].imageUrl;
    profileImgFull.src = allStories[currentActive].dp;
    storyAuthorFull.innerHTML = allStories[currentActive].author;
    // profileImgFull.src = allStories[currentActive].imageUrl;

 }

 nextBtn.addEventListener("click",() =>{
    storiesContent.scrollLeft +=300;
 });
 previousBtn.addEventListener("click",() =>{
    storiesContent.scrollLeft -=300;
 });
  
 storiesContent.addEventListener("scroll",()=>{
    if(storiesContent.scrollLeft<= 24){
        previousBtn.classList.remove("actived");
    } else {
        previousBtn.classList.add("actived");
    }
    
    let maxScrollValue = storiesContent.scrollWidth -storiesContent.clientWidth -24;
    
    if(storiesContent.scrollLeft>= maxScrollValue){
        nextBtn.classList.remove("actived");
    } else {
        nextBtn.classList.add("actived");
    }

});

nextBtnFull.addEventListener("click",() =>{
    if(currentActive >=allStories.length -1){
        return;
    }
    currentActive++;
    updateFullview();
})
previousBtnFull.addEventListener("click",() =>{
    if(currentActive <=0){
        return;
    }
    currentActive--;
    updateFullview();
})